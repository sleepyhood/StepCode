import argparse
import os
import sys
import tempfile
import threading
from pathlib import Path

import markdown
import tkinter as tk
from tkinter import filedialog, messagebox
from playwright.sync_api import sync_playwright


MARKDOWN_EXTENSIONS = [
    "extra",
    "fenced_code",
    "tables",
    "sane_lists",
    "toc",
]


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def build_html(md_path: Path) -> str:
    basedir = Path(__file__).resolve().parent
    template_path = basedir / "template.html"
    css_path = basedir / "style.css"

    md_text = load_text(md_path)
    html_content = markdown.markdown(md_text, extensions=MARKDOWN_EXTENSIONS)
    title = md_path.stem

    template = load_text(template_path)
    css_content = load_text(css_path)

    final_html = template.replace("/* CSS_CONTENT_PLACEHOLDER */", css_content)
    final_html = final_html.replace("{{ DOCUMENT_TITLE }}", escape_html(title))
    final_html = final_html.replace("{{ BASE_HREF }}", md_path.parent.as_uri() + "/")
    final_html = final_html.replace("<!-- CONTENT_PLACEHOLDER -->", html_content)
    return final_html


def escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def convert_md_to_pdf(
    md_path: str,
    output_pdf: str | None = None,
    status_callback=None,
    auto_open: bool = True,
):
    md_file = Path(md_path).resolve()
    if not md_file.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {md_file}")

    if output_pdf is None:
        output_path = md_file.with_suffix(".pdf")
    else:
        output_path = Path(output_pdf).resolve()

    if status_callback:
        status_callback("마크다운을 HTML로 변환하는 중...")
    final_html = build_html(md_file)

    tmp_html = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", suffix=".html", delete=False
        ) as handle:
            handle.write(final_html)
            tmp_html = Path(handle.name)

        if status_callback:
            status_callback("브라우저 렌더링 중...")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(tmp_html.as_uri(), wait_until="networkidle")
            page.emulate_media(media="screen")
            page.pdf(
                path=str(output_path),
                format="A4",
                print_background=True,
                margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            )
            browser.close()
    finally:
        if tmp_html and tmp_html.exists():
            tmp_html.unlink()

    if status_callback:
        status_callback(f"완료: {output_path.name}")

    if auto_open and sys.platform == "win32":
        os.startfile(output_path)  # type: ignore[attr-defined]

    return str(output_path)


class PDFConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pygame Markdown PDF 변환기")
        self.root.geometry("520x320")

        self.selected_file = None

        title = tk.Label(
            root,
            text="마크다운 문서를 깔끔한 PDF로 변환합니다.",
            pady=18,
            font=("Malgun Gothic", 12, "bold"),
        )
        title.pack()

        desc = tk.Label(
            root,
            text="제목, 코드 블록, 인용문, 이미지, 목차가 읽기 쉬운 형태로 정리됩니다.",
            wraplength=460,
            justify="center",
            fg="#475569",
            font=("Malgun Gothic", 9),
        )
        desc.pack()

        self.file_label = tk.Label(
            root,
            text="선택된 파일: 없음",
            fg="#2563eb",
            wraplength=460,
            pady=16,
            font=("Malgun Gothic", 9),
        )
        self.file_label.pack()

        self.select_btn = tk.Button(
            root,
            text="파일 찾기",
            command=self.select_file,
            width=18,
            font=("Malgun Gothic", 10),
        )
        self.select_btn.pack(pady=6)

        self.convert_btn = tk.Button(
            root,
            text="PDF로 변환하고 열기",
            command=self.start_conversion,
            width=24,
            pady=8,
            bg="#0f172a",
            fg="white",
            font=("Malgun Gothic", 11, "bold"),
        )
        self.convert_btn.pack(pady=14)

        self.status_label = tk.Label(
            root, text="대기 중...", fg="#64748b", font=("Malgun Gothic", 9)
        )
        self.status_label.pack(side="bottom", pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="마크다운 파일 선택",
            initialdir=str(Path(__file__).resolve().parent.parent),
            filetypes=[("Markdown Files", "*.md"), ("All Files", "*.*")],
        )
        if file_path:
            self.selected_file = file_path
            self.file_label.config(text=f"선택된 파일: {Path(file_path).name}")
            self.status_label.config(text="대기 중...")

    def update_status(self, text):
        self.status_label.config(text=text)
        self.root.update_idletasks()

    def start_conversion(self):
        if not self.selected_file:
            messagebox.showwarning("경고", "먼저 변환할 마크다운 파일을 선택해주세요.")
            return

        self.convert_btn.config(state="disabled")
        self.select_btn.config(state="disabled")

        def run():
            try:
                convert_md_to_pdf(
                    self.selected_file,
                    status_callback=self.update_status,
                    auto_open=True,
                )
            except Exception as exc:  # pragma: no cover - GUI fallback
                self.update_status("오류 발생")
                messagebox.showerror("변환 오류", str(exc))
            finally:
                self.convert_btn.config(state="normal")
                self.select_btn.config(state="normal")

        threading.Thread(target=run, daemon=True).start()


def main():
    parser = argparse.ArgumentParser(description="Markdown 문서를 PDF로 변환합니다.")
    parser.add_argument("markdown", nargs="?", help="변환할 마크다운 파일 경로")
    parser.add_argument("-o", "--output", help="출력 PDF 경로")
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="변환 후 PDF를 자동으로 열지 않습니다.",
    )
    args = parser.parse_args()

    if args.markdown:
        return convert_md_to_pdf(
            args.markdown,
            args.output,
            print,
            auto_open=not args.no_open,
        )

    root = tk.Tk()
    PDFConverterApp(root)
    root.mainloop()
    return None


if __name__ == "__main__":
    main()
