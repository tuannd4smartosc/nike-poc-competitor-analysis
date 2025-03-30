import pandas as pd
from scraper import SerperScraper
from utils import markdown_to_pdf, csv_to_pdf
import uuid
import os

def capture_campaign_snapshot(csv_files) -> list[str]:
    paths = []
    for csv in csv_files:
        csv_path = f"csv/{csv}"
        os.makedirs("snapshots", exist_ok=True)
        target_link = f"snapshots/snap-{uuid.uuid4().hex}.pdf"
        csv_to_pdf(csv_path,  target_link)
        paths.append(target_link)
    return paths
        
        
        