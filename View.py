import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import platform
from constants import LOGO_PATH, LOGO_WIDTH, ICON_PATH,valid_statuses

class RedirectView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.entries = []

        self.root.title("Redirect Checker")
        self.root.state('zoomed')
        self.root.focus_force()  # Ensure window is focused
        try:
            if os.path.exists(ICON_PATH):
                if platform.system() == "Windows":
                    self.root.iconbitmap(ICON_PATH)  # Use .ico on Windows
                else:  # Mac or others
                    icon_image = Image.open(ICON_PATH if os.path.exists(ICON_PATH) else LOGO_PATH)
                    icon_image = icon_image.resize((32, 32), Image.LANCZOS)  # Small size for icon
                    self.icon_photo = ImageTk.PhotoImage(icon_image)
                    self.root.iconphoto(True, self.icon_photo)
            else:
                print(f"Icon file not found at: {ICON_PATH}")
        except Exception as e:
            print(f"Error setting window icon: {e}")

        self.root.configure(bg="#f0f0f0")
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.canvas = tk.Canvas(self.canvas_frame)
        self.scrollbar = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.frame = self.scrollable_frame
        self.frame.configure(bg="#f0f0f0")
        self.row_start_index = 2
        self.add_row()
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Load CSV", command=self.controller.load_csv).pack(side="left", padx=5)
        tk.Button(button_frame, text="Add Row", command=self.controller.add_row).pack(side="left", padx=5)
        tk.Button(button_frame, text="Run Check", command=self.controller.run_check_thread).pack(side="left", padx=5)
        tk.Button(button_frame, text="Save Report", command=self.controller.export_html).pack(side="left", padx=5)
        tk.Button(button_frame, text="Open HTML Report", command=self.controller.open_html_report).pack(side="left", padx=5)
        tk.Button(button_frame, text="Exit", command=self.root.quit).pack(side="left", padx=5)

        console_frame = tk.Frame(root)
        console_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.console = tk.Text(console_frame, height=15, wrap='word', bg="#f0f0f0")
        self.console.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar = tk.Scrollbar(console_frame, command=self.console.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.console.config(yscrollcommand=scrollbar.set)

        clear_button = tk.Button(root, text="Clear Console", command=self.controller.clear_console)
        clear_button.pack(pady=5)

    def add_row(self, actual_url="", expected_url="", status_code=""):
        print(f"Adding row: actual={actual_url}, expected={expected_url}, status={status_code}")  # Debug
        actual_entry = tk.Entry(self.frame, width=60)
        actual_entry.insert(0, actual_url)
        expected_entry = tk.Entry(self.frame, width=60)
        expected_entry.insert(0, expected_url)
        status_var = tk.StringVar()
        status_dropdown = ttk.Combobox(self.frame, textvariable=status_var,
                                       values=valid_statuses,
                                       width=7, state="normal", justify="center")
        status_var.set(status_code if status_code else "")
        status_dropdown.configure(state="readonly")
        print(f"Set status_var to: {status_var.get()}")  # Debug
        delete_button = tk.Button(self.frame, text="Delete")
        self.entries.append([actual_entry, expected_entry, status_dropdown, delete_button])
        self.rebuild_table()
        self.root.after(0, self.root.update)  # Defer GUI refresh
        self.root.after(100, lambda: self.canvas.yview_moveto(1.0))
        self.root.after(150, lambda: actual_entry.focus_set())
        self.root.after(200, lambda: actual_entry.icursor(tk.END))

    def rebuild_table(self):
        for i, (actual, expected, status, delete_btn) in enumerate(self.entries):
            row_index = self.row_start_index + i
            actual.grid(row=row_index, column=0)
            expected.grid(row=row_index, column=1)
            status.grid(row=row_index, column=2)
            delete_btn.configure(text="Delete", command=lambda idx=i: self.controller.delete_row(idx))
            delete_btn.grid(row=row_index, column=3)

    def clear_all_rows(self):
        for widgets in self.entries:
            for widget in widgets:
                widget.destroy()
        self.entries.clear()

    def log(self, message, tag=""):
        self.console.insert(tk.END, message + "\n", tag)
        self.console.see(tk.END)

    def clear_console(self):
        self.console.delete("1.0", tk.END)