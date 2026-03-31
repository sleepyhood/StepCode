"""
python -m pip install --upgrade pip setuptools wheel
pip install "huggingface_hub[hf_xet]"
pip install "opendataloader-pdf[hybrid]" --no-cache-dir

opendataloader-pdf-hybrid --port 5002 --force-ocr
"""

import os
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

import requests


class OpenDataLoaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF to Markdown/JSON Extractor")
        self.root.geometry("680x620")

        self.input_files = []
        self.output_dir = tk.StringVar()
        self.page_ranges = tk.StringVar()

        frame_input = tk.LabelFrame(
            root, text="1. Select PDF files", padx=10, pady=10
        )
        frame_input.pack(fill=tk.X, padx=15, pady=10)

        self.listbox_files = tk.Listbox(frame_input, height=5, selectmode=tk.EXTENDED)
        self.listbox_files.pack(fill=tk.X, side=tk.TOP, pady=(0, 5))

        btn_frame = tk.Frame(frame_input)
        btn_frame.pack(fill=tk.X)
        tk.Button(btn_frame, text="+ Add PDF", command=self.add_files).pack(
            side=tk.LEFT, padx=2
        )
        tk.Button(btn_frame, text="+ Add Folder", command=self.add_folder).pack(
            side=tk.LEFT, padx=2
        )
        tk.Button(btn_frame, text="- Remove Selected", command=self.remove_selected).pack(
            side=tk.LEFT, padx=2
        )
        tk.Button(btn_frame, text="Clear", command=self.clear_files).pack(
            side=tk.RIGHT, padx=2
        )

        frame_output = tk.LabelFrame(root, text="2. Output folder", padx=10, pady=10)
        frame_output.pack(fill=tk.X, padx=15, pady=5)

        tk.Entry(
            frame_output, textvariable=self.output_dir, state="readonly", width=50
        ).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        tk.Button(frame_output, text="Browse", command=self.select_output_dir).pack(
            side=tk.RIGHT
        )

        frame_format = tk.LabelFrame(root, text="3. Output options", padx=10, pady=10)
        frame_format.pack(fill=tk.X, padx=15, pady=5)

        self.var_md = tk.BooleanVar(value=True)
        self.var_json = tk.BooleanVar(value=True)
        self.var_scan_mode = tk.BooleanVar(value=True)

        tk.Checkbutton(frame_format, text="Markdown (.md)", variable=self.var_md).pack(
            side=tk.LEFT, padx=10
        )
        tk.Checkbutton(frame_format, text="JSON (.json)", variable=self.var_json).pack(
            side=tk.LEFT, padx=10
        )
        tk.Checkbutton(frame_format, text="Scan document mode", variable=self.var_scan_mode).pack(
            side=tk.LEFT, padx=10
        )

        frame_pages = tk.LabelFrame(
            root, text="4. Page ranges (optional)", padx=10, pady=10
        )
        frame_pages.pack(fill=tk.X, padx=15, pady=5)

        tk.Entry(frame_pages, textvariable=self.page_ranges).pack(
            side=tk.LEFT, padx=5, fill=tk.X, expand=True
        )
        tk.Label(frame_pages, text="Example: 1-15,16-30,45").pack(
            side=tk.RIGHT, padx=5
        )

        self.btn_run = tk.Button(
            root,
            text="Start Batch Convert",
            command=self.start_conversion,
            bg="#2196F3",
            fg="white",
            font=("Arial", 11, "bold"),
            pady=10,
        )
        self.btn_run.pack(fill=tk.X, padx=15, pady=15)

        tk.Label(root, text="Work log:").pack(anchor=tk.W, padx=15)
        self.log_area = scrolledtext.ScrolledText(
            root, height=10, bg="#f4f4f4", state=tk.DISABLED
        )
        self.log_area.pack(fill=tk.BOTH, padx=15, pady=(0, 15), expand=True)

    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Select PDF files", filetypes=[("PDF Files", "*.pdf")]
        )
        added_count = 0
        for file_path in files:
            if file_path not in self.input_files:
                self.input_files.append(file_path)
                self.listbox_files.insert(tk.END, os.path.basename(file_path))
                added_count += 1
        self.log(f"Added {added_count} PDF file(s).")

    def add_folder(self):
        folder = filedialog.askdirectory(title="Select folder with PDFs")
        if not folder:
            return

        count = 0
        for root_dir, _, files in os.walk(folder):
            for file_name in files:
                if file_name.lower().endswith(".pdf"):
                    full_path = os.path.join(root_dir, file_name)
                    if full_path not in self.input_files:
                        self.input_files.append(full_path)
                        self.listbox_files.insert(tk.END, file_name)
                        count += 1

        self.log(f"Added {count} PDF file(s) from the folder.")

    def remove_selected(self):
        selected_indices = self.listbox_files.curselection()
        for index in reversed(selected_indices):
            del self.input_files[index]
            self.listbox_files.delete(index)

    def clear_files(self):
        self.input_files.clear()
        self.listbox_files.delete(0, tk.END)
        self.log("Cleared the file list.")

    def select_output_dir(self):
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_dir.set(folder)
            self.log(f"Output folder: {folder}")

    def log(self, message):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)

    def queue_log(self, message):
        self.root.after(0, lambda msg=message: self.log(msg))

    def parse_page_ranges(self, raw_value):
        raw_value = raw_value.strip()
        if not raw_value:
            return []

        ranges = []
        for chunk in raw_value.split(","):
            token = chunk.strip()
            if not token:
                continue

            if "-" in token:
                start_str, end_str = token.split("-", 1)
                if not start_str.isdigit() or not end_str.isdigit():
                    raise ValueError(f"Invalid page range: {token}")
                start = int(start_str)
                end = int(end_str)
                if start < 1 or end < 1 or start > end:
                    raise ValueError(f"Invalid page range: {token}")
            else:
                if not token.isdigit():
                    raise ValueError(f"Invalid page number: {token}")
                page_num = int(token)
                if page_num < 1:
                    raise ValueError(f"Invalid page number: {token}")

            ranges.append(token)

        if not ranges:
            raise ValueError("Page ranges are empty.")
        return ranges

    def build_range_output_dir(self, out_dir, input_path, page_range):
        stem = os.path.splitext(os.path.basename(input_path))[0]
        safe_range = page_range.replace("-", "_").replace(",", "_")
        return os.path.join(out_dir, stem, f"pages_{safe_range}")

    def run_convert_command(self, input_path, output_dir, fmt, use_scan_mode, page_range):
        command = [
            "opendataloader-pdf",
            input_path,
            "--output-dir",
            output_dir,
            "--format",
            fmt,
        ]

        if page_range:
            command.extend(["--pages", page_range])
        if use_scan_mode:
            command.extend(["--hybrid", "docling-fast"])

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            details = (result.stderr or result.stdout or "").strip()
            if not details:
                details = f"Process exited with code {result.returncode}"
            raise RuntimeError(details)

    def start_conversion(self):
        if not self.input_files:
            messagebox.showwarning("Warning", "Add at least one PDF file.")
            return
        if not self.output_dir.get():
            messagebox.showwarning("Warning", "Select an output folder.")
            return

        formats = []
        if self.var_md.get():
            formats.append("markdown")
        if self.var_json.get():
            formats.append("json")

        if not formats:
            messagebox.showwarning("Warning", "Select at least one output format.")
            return

        try:
            page_ranges = self.parse_page_ranges(self.page_ranges.get())
        except ValueError as exc:
            messagebox.showwarning("Page range error", str(exc))
            return

        format_str = ",".join(formats)

        self.btn_run.config(state=tk.DISABLED, text="Converting...")
        self.log("=== Conversion started ===")
        self.log(f"Processing {len(self.input_files)} PDF file(s).")
        if page_ranges:
            self.log(f"Page ranges: {', '.join(page_ranges)}")
        else:
            self.log("Page ranges: all pages")

        threading.Thread(
            target=self.run_conversion_task,
            args=(
                self.input_files.copy(),
                self.output_dir.get(),
                format_str,
                self.var_scan_mode.get(),
                page_ranges,
            ),
            daemon=True,
        ).start()

    def run_conversion_task(self, inputs, out_dir, fmt, use_scan_mode, page_ranges):
        if use_scan_mode:
            try:
                requests.get("http://localhost:5002/health", timeout=2)
            except Exception:
                self.root.after(
                    0,
                    lambda: messagebox.showerror(
                        "Server error",
                        "Scan document mode requires the 'opendataloader-pdf-hybrid' server to be running first.",
                    ),
                )
                self.root.after(
                    0,
                    lambda: self.btn_run.config(
                        state=tk.NORMAL, text="Start Batch Convert"
                    ),
                )
                return

        try:
            ranges_to_process = page_ranges or [None]
            failures = []

            for input_path in inputs:
                for page_range in ranges_to_process:
                    if page_range:
                        target_output_dir = self.build_range_output_dir(
                            out_dir, input_path, page_range
                        )
                        os.makedirs(target_output_dir, exist_ok=True)
                        self.queue_log(
                            f"{os.path.basename(input_path)} -> pages {page_range}"
                        )
                    else:
                        target_output_dir = out_dir
                        self.queue_log(
                            f"{os.path.basename(input_path)} -> all pages"
                        )

                    try:
                        self.run_convert_command(
                            input_path=input_path,
                            output_dir=target_output_dir,
                            fmt=fmt,
                            use_scan_mode=use_scan_mode,
                            page_range=page_range,
                        )
                    except Exception as exc:
                        label = page_range or "all pages"
                        failures.append(
                            f"{os.path.basename(input_path)} [{label}] -> {exc}"
                        )
                        self.queue_log(
                            f"FAILED: {os.path.basename(input_path)} [{label}]"
                        )

            if failures:
                self.root.after(0, self.conversion_partial_success, failures)
            else:
                self.root.after(0, self.conversion_success)
        except Exception as exc:
            self.root.after(0, self.conversion_error, str(exc))

    def conversion_success(self):
        self.log("All conversions completed.")
        messagebox.showinfo("Done", "PDF extraction completed successfully.")
        self.btn_run.config(state=tk.NORMAL, text="Start Batch Convert")

    def conversion_partial_success(self, failures):
        self.log("Conversion finished with some failures.")
        for failure in failures:
            self.log(failure)
        messagebox.showwarning(
            "Partial success",
            "Some page ranges failed. Check the work log for details.",
        )
        self.btn_run.config(state=tk.NORMAL, text="Start Batch Convert")

    def conversion_error(self, err_msg):
        self.log(f"Error: {err_msg}")
        messagebox.showerror("Error", f"A problem occurred during conversion.\n{err_msg}")
        self.btn_run.config(state=tk.NORMAL, text="Start Batch Convert")


if __name__ == "__main__":
    root = tk.Tk()
    app = OpenDataLoaderGUI(root)
    root.mainloop()
