#!/usr/bin/env python3
import sys
import os
import subprocess
import shutil
import zipfile
from pathlib import Path

# StepCode 루트 및 DoingCoding 기준 루트 디렉토리 설정
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
DOINGCODING_ROOT = ROOT_DIR / "practice" / "data" / "content" / "programming" / "doingcoding"


def find_unit_directory(problem_id: str) -> Path:
    """
    DoingCoding 루트 하위에서 03_solutions/{problem_id}.cpp 파일이 존재하는 단원 디렉토리를 재귀적으로 찾습니다.
    """
    if not DOINGCODING_ROOT.exists():
        print(f"Error: DoingCoding root directory not found at {DOINGCODING_ROOT}")
        sys.exit(1)

    for p in DOINGCODING_ROOT.rglob(f"03_solutions/{problem_id}.cpp"):
        # p는 .../Lv6_조건/03_solutions/problem_id.cpp 와 같은 경로를 가집니다.
        # 부모의 부모 디렉토리가 단원 루트(Lv6_조건)가 됩니다.
        return p.parent.parent

    print(f"Error: Solution file for '{problem_id}' not found under {DOINGCODING_ROOT}/**/03_solutions/")
    sys.exit(1)


def find_compiler() -> str:
    """
    시스템 PATH에 g++이 있는지 확인하고, 없으면 winget 설치 경로 및 C:\\MinGW\\bin\\g++.exe 를 시도합니다.
    """
    # 1. 시스템 PATH에서 g++ 시도
    gxx_path = shutil.which("g++")
    if gxx_path:
        return gxx_path

    # 2. winget 설치 경로 (WinLibs 등) 시도
    user_profile = os.environ.get("USERPROFILE")
    if user_profile:
        winget_dir = Path(user_profile) / "AppData" / "Local" / "Microsoft" / "WinGet" / "Packages"
        if winget_dir.exists():
            for gxx in winget_dir.rglob("**/g++.exe"):
                if gxx.exists():
                    return str(gxx)

    # 3. fallback 경로 시도
    fallback = Path("C:/MinGW/bin/g++.exe")
    if fallback.exists():
        return str(fallback)

    print("Error: g++ compiler not found in system PATH, winget packages, or at 'C:\\MinGW\\bin\\g++.exe'")
    print("Please install g++ or add it to your system PATH.")
    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/manager.py {problem_id} [num_cases]")
        print("Example: python scripts/manager.py P101v0612_1756 15")
        sys.exit(1)

    problem_id = sys.argv[1]
    num_cases = 15
    if len(sys.argv) >= 3:
        try:
            num_cases = int(sys.argv[2])
        except ValueError:
            print(f"Warning: Invalid number of cases '{sys.argv[2]}'. Using default (15).")

    # 1. 단원 디렉토리 탐색
    print(f"[*] Locating directories for problem '{problem_id}'...")
    unit_dir = find_unit_directory(problem_id)
    print(f"[+] Found unit directory: {unit_dir.name}")

    solutions_dir = unit_dir / "03_solutions"
    temp_dir = unit_dir / "temp" / problem_id
    testcases_dir = unit_dir / "04_testcases"

    cpp_path = solutions_dir / f"{problem_id}.cpp"
    input_gen_path = temp_dir / "input_gen.py"
    exe_path = temp_dir / "solution.exe"
    zip_path = testcases_dir / f"{problem_id}.zip"

    # 2. 임시 폴더 및 input_gen.py 존재 확인
    if not temp_dir.exists():
        temp_dir.mkdir(parents=True, exist_ok=True)

    if not input_gen_path.exists():
        print(f"Error: 'input_gen.py' not found at {input_gen_path}")
        print("You must create the input generator script in the temp folder before running manager.py.")
        sys.exit(1)

    # 3. 컴파일러 설정 및 C++ 컴파일
    compiler = find_compiler()
    print(f"[*] Compiling solution using: {compiler}")
    
    # 컴파일 명령 수행
    compile_cmd = [compiler, "-O2", "-std=c++17", str(cpp_path), "-o", str(exe_path)]
    result = subprocess.run(compile_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    
    if result.returncode != 0:
        print("Error: Compilation failed!")
        print("g++ compiler output:")
        print(result.stderr)
        sys.exit(1)
    print("[+] Compilation succeeded.")

    # 4. 테스트케이스 생성 루프
    print(f"[*] Generating {num_cases} testcases...")
    generated_files = []

    for i in range(1, num_cases + 1):
        in_file = temp_dir / f"{i}.in"
        out_file = temp_dir / f"{i}.out"

        # 4a. input_gen.py 실행하여 .in 파일 생성
        gen_cmd = [sys.executable, str(input_gen_path), str(i)]
        gen_result = subprocess.run(gen_cmd, capture_output=True, text=True, encoding="utf-8")
        if gen_result.returncode != 0:
            print(f"Error: input_gen.py failed on case {i}")
            print(gen_result.stderr)
            sys.exit(1)
        
        in_content = gen_result.stdout
        in_file.write_text(in_content, encoding="utf-8", newline="\n")

        # 4b. solution.exe 실행하여 .out 파일 생성
        try:
            sol_result = subprocess.run(
                [str(exe_path)],
                input=in_content,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=5.0  # 무한루프 방지 5초 제한
            )
        except subprocess.TimeoutExpired:
            print(f"Error: Time limit expired (5.0s) for solution.exe on case {i}")
            sys.exit(1)

        if sol_result.returncode != 0:
            print(f"Error: solution.exe crashed or returned non-zero code on case {i}")
            print(sol_result.stderr)
            sys.exit(1)

        out_content = sol_result.stdout
        out_file.write_text(out_content, encoding="utf-8", newline="\n")

        generated_files.append((in_file, f"{i}.in"))
        generated_files.append((out_file, f"{i}.out"))
        print(f"    - Case {i:02d}: Created .in and .out")

    # 5. ZIP 패키징 (Flat 구조)
    print(f"[*] Packaging test cases to: {zip_path.name}")
    testcases_dir.mkdir(parents=True, exist_ok=True)
    
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path, arcname in generated_files:
            zf.write(file_path, arcname=arcname)

    print(f"[+] ZIP packaging completed. Total files: {len(generated_files)} (15 in + 15 out)")
    print(f"[+] Location: {zip_path}")


if __name__ == "__main__":
    main()
