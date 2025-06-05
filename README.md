# Redirect Checker

A Python/Tkinter application to validate URL redirects by comparing actual URLs to expected URLs and HTTP status codes. Features include CSV import, HTML report generation, and a GUI with logo, window icon, and console logging.

## Project Structure

```
project/
├── Controller.py
├── Model.py
├── View.py
├── Images/
│   └── GUI.png
│   └── logo.png
│   └── logo.ico
├── constants.py
├── main.py
├── README.md
```

## Author

- **Name**: Kaveri Sabareesh (sabareeshkaveri@bmo.com)
- **Role**: QA Analyst
- **Background**:
  - Proficient in Python and Tkinter, with experience in GUI development 
- **Contribution**: Designed, developed, and debugged the Redirect Checker application, implementing features like CSV import, redirect validation, and HTML reporting.
- **Contact**: [Insert preferred contact method, e.g., email or GitHub profile]

## Configurations

### Prerequisites

- Python 3.6+
- Dependencies:
  - `requests`: For making HTTP requests to check URL redirects.
  - `jinja2`: For generating HTML reports using templates.
  - `Pillow`: For handling logo and icon images in the GUI.

### Install Dependencies

```bash
pip install requests jinja2 Pillow requests tk
```

### Setup

1. **Copy Files**:
   - Place all files in `project/` as shown in the structure above.

## Execution

1. **Run the Application**:
   ```bash
   cd project
   python main.py
   ```
   - Console outputs: Show Author Details - `Kaveri Sabareesh`.
   - GUI opens maximized with logo and icon.
  ![GUI ](/Images/GUI.png)
2. **Features**:
   - **Load CSV**: Import `actual`, `expected`, `status` from CSV.
   - **Add Row**: Add URL entries manually.
   - **Run Check**: Validate redirects, generate `redirect_report.html`.
   - **Save Report**: Save HTML report to custom path.
   - **Open HTML Report**: View report in browser.
   - **Clear Console**: Clear logs.
   - **Exit**: Close app.

3. **Sample CSV (`test.csv`)**:
   ```csv
   actual,expected,status
   http://example.com,https://example.com,301
   http://google.com,https://www.google.com,200
   ```

## Report

- **Generation**:
  - Click **Run Check** to validate URLs.
  - Automatically generates `redirect_report.html` in the project directory (default path defined in `constants.py`).
  - Report includes:
    - Total URLs checked.
    - Passed/failed/error counts.
    - Detailed table with actual URL, expected URL, final URL, status code, redirect match, and status match.

- **Save Custom Report**:
  - Click **Save Report** to save the HTML report to a custom location via file dialog.

- **View Report**:
  - Click **Open HTML Report** to open `redirect_report.html` in the default browser.

- **Sample Report**:
  - Generated as `redirect_report.html` with a timestamp, e.g., "2025-06-05 11:20:00".

