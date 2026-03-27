import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading

# 용량을 보기 좋게 변환
def format_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0

# 재귀적으로 폴더 용량 계산
def get_size(path):
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file(follow_symlinks=False):
                total += entry.stat(follow_symlinks=False).st_size
            elif entry.is_dir(follow_symlinks=False):
                total += get_size(entry.path)
    except (PermissionError, FileNotFoundError):
        pass
    return total

class DiskAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("디스크 용량 분석기")
        self.root.geometry("650x450")

        # 상단 프레임 (버튼 및 상태 표시)
        top_frame = tk.Frame(root)
        top_frame.pack(pady=10, fill=tk.X, padx=10)

        self.btn_scan = tk.Button(top_frame, text="폴더 선택 및 스캔", command=self.start_scan)
        self.btn_scan.pack(side=tk.LEFT)

        # 🚀 추가된 복사 버튼
        self.btn_copy = tk.Button(top_frame, text="상위 결과 복사", command=self.copy_to_clipboard, state=tk.DISABLED)
        self.btn_copy.pack(side=tk.LEFT, padx=10)

        self.lbl_status = tk.Label(top_frame, text="대기 중...")
        self.lbl_status.pack(side=tk.LEFT, padx=10)

        # 트리뷰 (표 형태의 데이터 출력)
        columns = ("name", "type", "size_str", "size_bytes")
        self.tree = ttk.Treeview(root, columns=columns, show="headings")
        
        self.tree.heading("name", text="이름")
        self.tree.heading("type", text="유형")
        self.tree.heading("size_str", text="크기")
        self.tree.heading("size_bytes", text="바이트(숨김)")
        
        self.tree.column("name", width=350)
        self.tree.column("type", width=80, anchor=tk.CENTER)
        # 너비를 100에서 150으로 늘리고, 창 크기를 줄여도 120 이하로 좁아지지 않게 minwidth 추가
        self.tree.column("size_str", width=150, minwidth=120, anchor=tk.CENTER)
        self.tree.column("size_bytes", width=0, stretch=tk.NO)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 스크롤바
        scrollbar = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def start_scan(self):
        folder_selected = filedialog.askdirectory()
        if not folder_selected:
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.btn_scan.config(state=tk.DISABLED)
        self.btn_copy.config(state=tk.DISABLED) # 스캔 중 복사 버튼 비활성화
        self.lbl_status.config(text=f"스캔 중... ({folder_selected})")
        
        threading.Thread(target=self.scan_directory, args=(folder_selected,), daemon=True).start()

    def scan_directory(self, path):
        results = []
        try:
            for entry in os.scandir(path):
                if entry.is_dir(follow_symlinks=False):
                    size = get_size(entry.path)
                    results.append((entry.name, "폴더", size))
                elif entry.is_file(follow_symlinks=False):
                    size = entry.stat(follow_symlinks=False).st_size
                    results.append((entry.name, "파일", size))
        except PermissionError:
            pass

        results.sort(key=lambda x: x[2], reverse=True)
        self.root.after(0, self.update_tree, results)

    def update_tree(self, results):
        for name, item_type, size in results:
            self.tree.insert("", tk.END, values=(name, item_type, format_size(size), size))
            
        self.lbl_status.config(text="스캔 완료!")
        self.btn_scan.config(state=tk.NORMAL)
        if results:
            self.btn_copy.config(state=tk.NORMAL) # 스캔 완료 후 결과가 있으면 활성화

    # 🚀 추가된 클립보드 복사 로직
    def copy_to_clipboard(self):
        items = self.tree.get_children()
        if not items:
            return

        # 상위 20개까지만 텍스트로 구성 (필요시 숫자 변경 가능)
        top_items = items[:20]
        
        text_to_copy = "순위\t크기\t\t유형\t이름\n"
        text_to_copy += "-" * 60 + "\n"
        
        for index, item in enumerate(top_items, start=1):
            values = self.tree.item(item, 'values')
            name, item_type, size_str, _ = values
            text_to_copy += f"{index}위\t{size_str:<10}\t{item_type}\t{name}\n"

        # 클립보드에 복사
        self.root.clipboard_clear()
        self.root.clipboard_append(text_to_copy)
        
        messagebox.showinfo("복사 완료", "상위 용량 결과가 클립보드에 텍스트로 복사되었습니다.\n(메모장이나 엑셀에 붙여넣기 해보세요)")

if __name__ == "__main__":
    root = tk.Tk()
    app = DiskAnalyzerApp(root)
    root.mainloop()