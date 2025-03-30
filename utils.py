import re
import os
import json
from datetime import datetime
import csv
import streamlit as st
from markdown import markdown
from weasyprint import HTML, CSS
import uuid
import pandas as pd
from config import REPORT_DIR
import html
import urllib.parse

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

def generate_campaign_csv(search_results: list[dict], prefix: str):
    data = []
    dict_with_most_keys = max(search_results, key=len)
    keys = list(dict_with_most_keys.keys()) if search_results else []
    data.append([sanitize_text(key_item) for key_item in keys])
    for result in search_results:
        record = []
        for value in result.values():
            record.append(sanitize_text(value))
        data.append(record)
    id = uuid.uuid4().hex
    directory = "csv"
    file_path = os.path.join(directory, f"{prefix}_{id}_competitor_analysis_{timestamp}.csv")

    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    # Create CSV file
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print("CSV file created successfully!")
    
def show_confetti():
    st.balloons() 
    
def markdown_to_pdf(markdown_text, output_path):
    html_text = markdown(markdown_text, extensions=['markdown.extensions.tables', 'markdown.extensions.extra', 'markdown.extensions.nl2br'])
    styled_html = f"""
    <body>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; margin: 0; padding: 20px;}}
            .report-container {{ max-width: 800px; margin: 0 auto; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); }}
            h1, h2, h3 {{ color: #2c3e50; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
            th {{ background-color: #f4f4f4; color: #2c3e50; font-weight: bold; }}
            td {{ background-color: #fff; }}
            tr:nth-child(odd) td {{ background-color: #f9f9f9; }}
            p, li {{ line-height: 1.6; margin: 10px 0; }}
            ol {{ padding-left: 20px; }}
        </style>
        <div class="report-container">
            {html_text}
        </div>
    </body>
    </html>
    """

    # def get_options():
    #     return {
    #         'page-size': 'Letter',
    #         'margin-top': '0.75in',
    #         'margin-right': '0.75in',
    #         'margin-bottom': '0.75in',
    #         'margin-left': '0.75in',
    #         'encoding': "UTF-8",
    #         'custom-header': [
    #             ('Accept-Encoding', 'gzip')
    #         ],
    #         'no-outline': None
    #     }
    HTML(string=styled_html).write_pdf(output_path)

def get_pdf_download_link(pdf_path, filename):
    with open(pdf_path, "rb") as f:
        pdf_data = f.read()
    return st.download_button(
        label="Download PDF",
        data=pdf_data,
        file_name=filename,
        mime="application/pdf",
    )

def generate_file_name(id, prefix, extension):
    return  f"reports/{prefix}_{id}_competitor_analysis.{extension}"

def find_files_in_dir(directory, search_string):
    return [f for f in os.listdir(directory) if search_string in f]

def create_pdf_from_md(md_path):
    with open(os.path.join(md_path), "r") as f:
        report_content = f.read()

    pdf_path = os.path.join(md_path.replace(".md", ".pdf"))
    markdown_to_pdf(report_content, pdf_path)
    return md_path.replace(".md", ".pdf")

def sanitize_text(text: str, 
    strip_whitespace: bool = True,
    remove_quotes: bool = True,
    lowercase: bool = False,
    remove_special_chars: bool = False,
    escape_html: bool = False,
    remove_html: bool = False,
    custom_regex: str | None = None) -> str:
   
    if not isinstance(text, str):
        return "None"  # Return empty string for non-string inputs

    result = text

    # Step 1: Strip whitespace and collapse multiple spaces
    if strip_whitespace:
        result = re.sub(r'\s+', ' ', result.strip())

    # Step 2: Remove quotes
    if remove_quotes:
        result = result.strip('"').strip("'")

    # Step 3: Convert to lowercase
    if lowercase:
        result = result.lower()

    # Step 4: Remove special characters (keep letters, numbers, and spaces)
    if remove_special_chars:
        result = re.sub(r'[^a-zA-Z0-9 ]', '', result)

    # Step 5: Escape HTML characters
    if escape_html:
        result = html.escape(result)

    # Step 6: Remove HTML tags
    if remove_html:
        result = re.sub(r'<[^>]+>', '', result)

    # Step 7: Apply custom regex if provided
    if custom_regex:
        try:
            result = re.sub(custom_regex, '', result)
        except re.error:
            pass  # Ignore invalid regex patterns

    if len(result) == 0:
        return "None"
    
    return urllib.parse.quote(result, safe=':/?&= !?.@*()')

def csv_to_pdf(csv_file, pdf_file):
    df = pd.read_csv(csv_file)

    # Store all row tables
    html_tables = []

    # Loop through each row to generate individual tables
    for _, row in df.iterrows():
        df_transposed = row.to_frame().reset_index()  # Convert row to DataFrame
        df_transposed.columns = ["Label", "Value"]  # Rename columns
        
        # Apply inline styling inside the Value column
        df_transposed["Value"] = df_transposed["Value"].apply(
            lambda x: f'<div style="min-width: 400px; max-width: 400px; word-wrap: break-word;">{x}</div>'
        )

        # Define CSS for clean layout
        css = """
        <style>
            h1.title { font-weight: bold; font-size: 32px; margin-bottom: 24px; }
            table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
            th, td { border: 1px solid black; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            td:nth-child(1) { width: 30%; font-weight: bold; } /* Label column */
        </style>
        """

        # Append each row table as HTML
        html_tables.append(f"{css}{df_transposed.to_html(index=False, escape=False)}")

    # Combine all row tables into a single HTML document
    title = ""
    if "marketing" in csv_file:
        title = "Marketing promotion campaign snapshots"
    elif "pricing" in csv_file:
        title = "Competitors' pricing analysis snapshots"
    html_content = f"<br>".join(html_tables)
    html_content_with_title = f"<h1 class='title'>{title}</h1>{html_content}"

    # Convert HTML to PDF
    HTML(string=html_content_with_title).write_pdf(pdf_file)
    print(f"PDF saved as: {pdf_file}")
    
def empty_directory(directory_path: str) -> None:
    def remove_dir_contents(path: str) -> None:
        """Helper function to recursively delete director contents."""
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)  # Delete file
            elif os.path.isdir(item_path):
                remove_dir_contents(item_path)  # Recurse into subdirectory
                os.rmdir(item_path)  # Remove empty subdirectory

    try:
        # Check if directory exists
        if not os.path.exists(directory_path):
            print(f"Directory '{directory_path}' does not exist.")
            return
        
        # Remove all contents
        remove_dir_contents(directory_path)
        print(f"Directory '{directory_path}' has been emptied.")
    except Exception as e:
        print(f"Error emptying directory: {e}")
    
class StreamToExpander:
    def __init__(self, expander, st):
        self.expander = expander
        self.st = st
        self.buffer = []
        self.logs = []
        self.processed_entries = set() 
        self.log_container = self.expander.empty()
        self.colors = {'task': '#388E3C', 'agent': '#1565C0', 'tool': '#FF8F00', 'completion': '#2E7D32'}

    def write(self, data):
        cleaned_data = re.sub(r'\x1B\[[0-9;]*[mK]', '', data)

        task_match = re.search(r'Task:\s*(.*)', cleaned_data)
        if task_match:
            task_value = task_match.group(1).strip()
            self.st.toast(":robot_face: " + task_value)

        # Buffer the data
        self.buffer.append(cleaned_data)
        if "\n" in data:
            log_entry = ''.join(self.buffer).strip()
            if not re.search(r'[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}', log_entry):
                if log_entry not in self.processed_entries:
                    self.processed_entries.add(log_entry)
                    formatted_log = self.format_log(log_entry)
                    if formatted_log:
                        self.logs.append(formatted_log)
                        self.log_container.markdown(
                            '<div class="log-container">' + ''.join(self.logs) + '</div>',
                            unsafe_allow_html=True
                        )
            self.buffer = []

    def flush(self):
        pass 

    def get_logs(self):
        return '<div class="log-container">' + ''.join(self.logs) + '</div>'

    def format_log(self, log_entry):
        log_entry_normalized = log_entry.title()
        
        if "[📋 TASK STARTED:" in log_entry:
            task = log_entry_normalized.split("Task Started:")[1].split("]")[0].strip()
            return f'<div class="log-entry slideFadeIn" style="color: {self.colors["task"]};">📋 {self.wrap_text(task)}</div>'
        elif "[🤖 AGENT" in log_entry and "STARTED TASK" in log_entry:
            agent = log_entry_normalized.split("'")[1]
            return f'<div class="log-entry slideFadeIn" style="color: {self.colors["agent"]};">🤖 {agent} Started</div>'
        elif "Task:" in log_entry:
            task = log_entry_normalized.replace("Task:", "").strip()
            return f'<div class="log-entry slideFadeIn" style="color: {self.colors["task"]};">📋 {self.wrap_text(task)}</div>'
        elif "[🛠️ TOOL USAGE STARTED:" in log_entry:
            tool = log_entry_normalized.split("'")[1]
            return f'<div class="log-entry slideFadeIn" style="color: {self.colors["tool"]};">🛠️ {tool} Started</div>'
        elif "[✅ TOOL USAGE FINISHED:" in log_entry:
            tool = log_entry_normalized.split("'")[1]
            return f'<div class="log-entry slideFadeIn" style="color: {self.colors["tool"]};">✅ {tool} Finished</div>'
        elif "Tool Input:" in log_entry:
            input_data = log_entry_normalized.replace("Tool Input:", "").strip()
            formatted_input = self.prettify_json(input_data)
            return f'<div class="log-entry slideFadeIn" style="color: {self.colors["tool"]};">🔍 Input: {formatted_input}</div>'
        elif "Tool Output:" in log_entry:
            output = log_entry_normalized.replace("Tool Output:", "").strip()
            formatted_output = self.prettify_json(output)
            return f'<div class="log-entry slideFadeIn" style="color: {self.colors["tool"]};">📦 Output: {formatted_output}</div>'
        elif "Final Answer:" in log_entry:
            answer = log_entry_normalized.replace("Final Answer:", "").strip()
            formatted_answer = self.prettify_json(answer)
            return f'<div class="log-entry slideFadeIn" style="color: {self.colors["completion"]};">🎯 {formatted_answer}</div>'
        elif "[✅ TASK COMPLETED:" in log_entry:
            task = log_entry_normalized.split("Completed:")[1].split("]")[0].strip()
            return f'<div class="log-entry slideFadeIn" style="color: {self.colors["completion"]};">✅ {self.wrap_text(task)}</div>'
        elif "[✅ CREW 'CREW' COMPLETED" in log_entry:
            return f'<div class="log-entry slideFadeIn" style="color: {self.colors["completion"]};">✅ Process Completed</div>'
        return None 

    def wrap_text(self, text, max_length=50):
        """Wrap long text into multiple lines for readability."""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0

        for word in words:
            if current_length + len(word) + 1 <= max_length:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_length = len(word) + 1
        if current_line:
            lines.append(" ".join(current_line))
        return " ".join(lines)

    def prettify_json(self, text):
        try:
            if text.strip().replace("## ", "").startswith(('{', '[')):
                json_data = json.loads(text)
                pretty_json = json.dumps(json_data, indent=2, ensure_ascii=False)
                return f'<pre style="margin: 0; padding: 5px; background-color: #f5f5f5; border-radius: 4px;">{pretty_json}</pre>'
            return 'All data fetched!'
        except json.JSONDecodeError:
            return 'All data fetched!'