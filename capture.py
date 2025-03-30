import pandas as pd
from scraper import SeleniumScraper

def capture_campaign_snapshot(csv_files):
    print("csv_files", csv_files)
    for csv in csv_files[:4]:
        csv_path = f"csv/{csv}"
        df_campaign = pd.read_csv(csv_path, delimiter=',')
        links = df_campaign['link'].dropna().tolist()
        print("links", links, type(links))
        for link in links[:2]:
            scraper = SeleniumScraper().crawl_and_snapshot(link)
        
files = ['marketing_13dfee4f963e4742a152064cc41c06f2_competitor_analysis_20250330_200913.csv', 'marketing_ae45f64ae6ec41019f1cb84b5ab21210_competitor_analysis_20250330_200913.csv']
capture_campaign_snapshot(files)