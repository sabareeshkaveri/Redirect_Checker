import os
from urllib.parse import quote
# Constants for the Redirect Checker application
author = "Sabareesh Kaveri"
authorEmail    = "sabareeshkaveri@gmail.com"

# File paths
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_REPORT_PATH = os.path.join(PROJECT_DIR, "redirect_report.html")
LOGO_PATH = os.path.join(PROJECT_DIR,"Images", "logo.png")
ICON_PATH = os.path.join(PROJECT_DIR,"Images", "logo.ico")  # Use .ico for Windows, fallback to logo.png for Mac

# Default values for redirect checking
valid_statuses = ["", "200", "301", "302", "400", "403", "404", "500"]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Connection': 'keep-alive',
                           }
ssl_verify = True  # Set to False if you want to disable SSL verification
time_out = 10  # Default timeout for requests in seconds
allow_redirects = True  # Allow redirects by default
is_proxy_required = False  # Default to no proxy required
# Proxy settings
proxy_url = "your_proxy"     # Replace with your actual proxy host
proxy_port = "port"  # Replace with your actual proxy port
proxy_userid = "your_username"  # Optional: Replace with your proxy username
proxy_pass = "your_password"        # Optional: Replace with your proxy password

if is_proxy_required:
    proxy_url = quote(proxy_url) 
    proxy_port = quote(proxy_port)
    proxy_userid = quote(proxy_userid)
    proxy_pass = quote(proxy_pass)  
    proxy_encoded = f"http://{proxy_userid}:{proxy_pass}@{proxy_url}:{proxy_port}" if proxy_userid and proxy_pass else f"http://{proxy_url}:{proxy_port}"
    PROXY = {
        "http": proxy_encoded,
        "https": proxy_encoded
}
else:
    # If no proxy is required, set empty strings
     PROXY = None

# File dialog constants
DEFAULT_REPORT_FILENAME = "redirect_report.html"
CSV_FILE_FILTER = [("CSV Files", "*.csv")]
HTML_FILE_FILTER = [("HTML Files", "*.html")]
FILE_DIALOG_TITLE_SAVE = "Save HTML Report"

# Logo dimensions
LOGO_WIDTH = 200