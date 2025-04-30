import pandas as pd
from scraper import SerperScraper
from utils import markdown_to_pdf, csv_to_pdf, get_csv_html_content
import uuid
import os

def capture_campaign_snapshot(csv_files) -> str:
    html_contents = []
    for csv in csv_files:
        csv_path = f"csv/{csv}"
        csv_content = get_csv_html_content(csv_path)
        html_contents.append(csv_content)
    snapshot_path = f"snapshots/appendix-{uuid.uuid4().hex}.pdf"
    combined_contents = f"<br><br><br>".join(html_contents)
    markdown_to_pdf( combined_contents, f"snapshots/appendix-{uuid.uuid4().hex}.pdf")
    return snapshot_path
        
        
        