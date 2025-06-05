import threading
import requests
import webbrowser
from datetime import datetime
from tkinter import filedialog, messagebox
from jinja2 import Environment, FileSystemLoader
from Model import RedirectModel
from View import RedirectView
from constants import DEFAULT_REPORT_PATH, HTML_FILE_FILTER, DEFAULT_REPORT_FILENAME, FILE_DIALOG_TITLE_SAVE,author,authorEmail,headers,ssl_verify,time_out,allow_redirects,PROXY
import os
class RedirectCheckerController:
    def __init__(self, root):
        self.model = RedirectModel()
        self.root = root
        try:
            self.view = RedirectView(root, controller=self)
        except Exception as e:
            print(f"Error initializing RedirectView: {e}")
            raise
        self.results_data = []
        self.report_path = None

    def load_csv(self):
        from constants import CSV_FILE_FILTER
        file_path = filedialog.askopenfilename(filetypes=CSV_FILE_FILTER)
        if not file_path:
            return
        self.view.clear_all_rows()
        data = self.model.load_csv(file_path)
        for row in data:
            status = row["status"]
            print(f"Loading row: actual={row['actual']}, expected={row['expected']}, status={status}")  # Debug
            self.view.add_row(row["actual"], row["expected"], status)

    def add_row(self):
        self.view.add_row()

    def delete_row(self, index):
        widgets = self.view.entries.pop(index)
        for widget in widgets:
            widget.destroy()
        self.view.rebuild_table()

    def clear_console(self):
        self.view.clear_console()

    def run_check_thread(self):
        thread = threading.Thread(target=self.run_check)
        thread.start()
    def run_authorConsole(self):
        try:
            self.view.console.tag_config("author", foreground="blue")
            self.view.console.insert("end", f"Author: {author}\n", "author")
            if authorEmail:
                self.view.console.insert("end", f"Email: {authorEmail}\n", "author")
        except AttributeError as e:
            print(f"Error accessing view.console: {e}")
    def run_check(self):
        
        try:
            self.view.console.tag_config("success", foreground="green")
            self.view.console.tag_config("fail", foreground="red")
            self.view.console.tag_config("error", foreground="orange")
            self.view.console.tag_config("bold", font=("Arial", 10, "bold"))
        except AttributeError as e:
            print(f"Error accessing view.console: {e}")
            return

        self.results_data = []
        header = f"{'Actual URL'.ljust(40)} {'Expected URL'.ljust(40)} {'Final URL'.ljust(40)} {'Status'.ljust(10)} {'RedirectMatch'.ljust(15)} {'StatusMatch'.ljust(15)}"
        self.view.log(header, "bold")

        has_run = False
        for actual_entry, expected_entry, status_dropdown, _ in self.view.entries:
            actual = actual_entry.get().strip()
            expected = expected_entry.get().strip()
            selected_status = status_dropdown.get().strip()
            if not actual or not expected:
                continue
            has_run = True
            try:
                if not actual.startswith(("http://", "https://")):
                    actual = "https://" + actual  # Default to HTTP if no scheme is provided
                response = requests.head(url=actual,verify=ssl_verify, allow_redirects=allow_redirects, timeout=time_out,headers=headers,proxies=PROXY)
                if response.next :
                    final_url = response.next.url
                else:
                    final_url = response.url
                status_code = response.status_code
                redirect_match = final_url == expected
                status_match = selected_status and str(status_code) == selected_status
                tag = "success" if redirect_match and (status_match or not selected_status) else "fail"
                self.results_data.append({
                    "actual": actual,
                    "expected": expected,
                    "final_url": final_url,
                    "status_code": status_code,
                    "expected_status": selected_status if selected_status else "Skipped",
                    "redirect_match": "Yes" if redirect_match else "No",
                    "status_match": "Yes" if status_match else "No" if selected_status else "Skipped"
                })
                self.view.log(
                    f"{actual.ljust(40)} {expected.ljust(40)} {final_url.ljust(40)} {str(status_code).ljust(10)} {'Yes' if redirect_match else 'No'.ljust(15)} {'Yes' if status_match else 'No' if selected_status else 'Skipped'.ljust(15)}",
                    tag
                )
            except requests.RequestException as e:
                self.results_data.append({
                    "actual": actual,
                    "expected": expected,
                    "final_url": "N/A",
                    "status_code": "N/A",
                    "expected_status": selected_status if selected_status else "Skipped",
                    "redirect_match": "Error",
                    "status_match": "Error"
                })
                self.view.log(
                    f"{actual.ljust(40)} {expected.ljust(40)} {'N/A'.ljust(40)} {'N/A'.ljust(10)} {'Error'.ljust(15)} {'Error'.ljust(15)}",
                    "error"
                )
        if not has_run:
            self.view.log("No valid URLs to check.", "error")
            self.root.after(0, lambda: messagebox.showinfo("Check Complete", "No valid URLs to check."))
            return

        self.export_html(use_default_path=True)
        self.root.after(0, lambda: messagebox.showinfo("Check Complete", "Redirect check completed successfully!"))
        self.view.log("\n\U0001F4C8 Redirect check completed successfully!", "success")
    def export_html(self, use_default_path=False):
        if not self.results_data:
            self.root.after(0, lambda: messagebox.showinfo("No Data", "No results to export. Run the check first."))
            return

        if use_default_path:
            output_path = DEFAULT_REPORT_PATH
        else:
            output_path = filedialog.asksaveasfilename(
                defaultextension=".html",
                filetypes=HTML_FILE_FILTER,
                initialfile=DEFAULT_REPORT_FILENAME,
                title=FILE_DIALOG_TITLE_SAVE
            )
            if not output_path:
                self.view.log("HTML report save cancelled.", "error")
                self.root.after(0, lambda: messagebox.showinfo("Save Cancelled", "HTML report save was cancelled."))
                return

        env = Environment(loader=FileSystemLoader('.'))
        template_str = self.model.get_html_template()
        total = len(self.results_data)
        passed = sum(1 for r in self.results_data if r["redirect_match"] == "Yes" and (r["status_match"] == "Yes" or r["status_match"] == "Skipped"))
        failed = sum(1 for r in self.results_data if r["redirect_match"] == "No" or r["status_match"] == "No")
        errors = sum(1 for r in self.results_data if r["redirect_match"] == "Error")

        template = env.from_string(template_str)
        html_content = template.render(
            results=self.results_data,
            total=total,
            passed=passed,
            failed=failed,
            errors=errors,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),author=author,
            author_email=authorEmail if authorEmail else ""
        )
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            self.report_path = output_path
            self.view.log(f"\n\U0001F4C4 HTML Report saved at: {output_path}", "success")
        except Exception as e:
            self.view.log(f"Error saving HTML report: {e}", "error")
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to save HTML report: {e}"))

    def open_html_report(self):
        import pathlib
        if self.report_path and os.path.exists(self.report_path):
            file_url = pathlib.Path(self.report_path).absolute().as_uri()
            try:
                opened = webbrowser.open(file_url)
                if not opened:
                    self.root.after(0, lambda: messagebox.showerror("Error", "Failed to open the report in the browser."))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Could not open report: {e}"))
        else:
            self.root.after(0, lambda: messagebox.showinfo("No Report", "No HTML report found. Please run the check first."))