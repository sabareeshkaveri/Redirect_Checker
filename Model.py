import csv
class RedirectModel:
    HTML_TEMPLATE = """
        <html>
        <head>
            <title>Redirect Validation Report</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; background-color: #fafafa; }
                h1 { color: #333; }
                table { border-collapse: collapse; width: 100%; margin-top: 20px; }
                th, td { border: 1px solid #ccc; padding: 8px; text-align: left; font-size: 14px; }
                th { background-color: #eee; }
                .success { background-color: #d4edda; }
                .fail { background-color: #f8d7da; }
                .error { background-color: #fff3cd; }
                .summary { margin-top: 10px; font-size: 16px; font-weight: bold; }
            </style>
        </head>
        <body>
            <h1>Redirect Validation Report</h1>
            <p>Author: {{ author }}{% if author_email %} ({{ author_email }}){% endif %}</p>
            <div class="summary">
                Generated on: {{ timestamp }}<br>
                Total Entries: {{ total }} |
                ✅ Passed: {{ passed }} |
                ❌ Failed: {{ failed }} |
                ⚠️ Errors: {{ errors }}
            </div>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Actual URL</th>
                        <th>Expected URL</th>
                        <th>Final URL</th>
                        <th>Status Code</th>
                        <th>Expected Status</th>
                        <th>Redirect Match</th>
                        <th>Status Match</th>
                    </tr>
                </thead>
                <tbody>
                {% for row in results %}
                    <tr class="{% if row.redirect_match == 'Yes' and (row.status_match == 'Yes' or row.status_match == 'Skipped') %}success{% elif row.redirect_match == 'No' or row.status_match == 'No' %}fail{% else %}error{% endif %}">
                        <td>{{ loop.index }}</td>
                        <td>{{ row.actual }}</td>
                        <td>{{ row.expected }}</td>
                        <td>{{ row.final_url }}</td>
                        <td>{{ row.status_code }}</td>
                        <td>{{ row.expected_status }}</td>
                        <td>{{ row.redirect_match }}</td>
                        <td>{{ row.status_match }}</td>
                    </tr>
                {% endfor %}
                </tbody>
            </table>
        </body>
        </html>
    """

    def __init__(self):
        self.data = []

    def load_csv(self, filepath):
        self.data.clear()
        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.data.append({
                    "actual": row.get("actual", ""),
                    "expected": row.get("expected", ""),
                    "status": row.get("status", "")
                })
        return self.data

    def get_html_template(self):
        return self.HTML_TEMPLATE