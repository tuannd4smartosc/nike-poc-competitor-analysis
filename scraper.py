import json
import os
import requests
from dotenv import load_dotenv
load_dotenv()

class SerperScraper:
    def scrape(self, link: str):
        url = "https://scrape.serper.dev/"
        payload = json.dumps({"url": link, "includeMarkdown": True})
        headers = {
            'X-API-KEY': os.environ['SERPER_API_KEY'],
            'content-type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()