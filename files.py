import os
from markdown import markdown
from weasyprint import HTML
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

def combine_md_files(input_folder, output_folder):
    # Open the output file in write mode
    # Ensure the directory exists
    os.makedirs(output_folder, exist_ok=True)
    output_md = f"{output_folder}/report_{timestamp}.md"
    with open(output_md, "w", encoding="utf-8") as outfile:
        # Iterate through all .md files in the input folder
        for filename in sorted(os.listdir(input_folder)):
            if filename.endswith(".md"):
                file_path = os.path.join(input_folder, filename)
                with open(file_path, "r", encoding="utf-8") as infile:
                    # Write the content of the current .md file
                    outfile.write(infile.read())
                    # Add a separator (optional)
                    outfile.write("\n\n---\n\n")
                    
    return output_md

def md_files_to_pdf(input_folder, output_folder):
    # List to store combined HTML content
    combined_html = ""

    # Iterate through all .md files in the input folder
    for filename in sorted(os.listdir(input_folder)):
        if filename.endswith(".md"):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, "r", encoding="utf-8") as md_file:
                # Read Markdown content and convert to HTML
                md_content = md_file.read()
                html_content = markdown(md_content)
                # Add filename as a header and the content
                combined_html += f"<div>{html_content}</div><hr>"

    # Add basic HTML structure and CSS for formatting
    full_html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ color: #2c3e50; font-size: 24px; }}
            hr {{ border: 0; border-top: 1px solid #ddd; margin: 20px 0; }}
            p {{ line-height: 1.6; }}
        </style>
    </head>
    <body>{combined_html}</body>
    </html>
    """

    os.makedirs(output_folder, exist_ok=True)
    # Convert HTML string to PDF using WeasyPrint
    HTML(string=full_html).write_pdf(f"{output_folder}/report_{timestamp}.pdf")
    
def read_md_file(file_path):
    with open(file_path, "r", encoding="utf-8") as md_file:
        content = md_file.read()
    return content