from crewai.tools import tool
import json
import os
import requests
from typing import Type
from utils import generate_campaign_csv
import urllib.parse

from dotenv import load_dotenv
load_dotenv()

@tool("Search the internet for ad campaigns")
def search_tool(query: str) -> str:
    """Useful to search the internet about ad campaigns of big companies in sportwear."""
    
    print(">>>>>>>>>>> argument", query)
    # Implementation goes here
    top_result_to_return = 4
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': os.environ.get('SERPER_API_KEY', ''),
        'content-type': 'application/json'
    }
    
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        if 'organic' not in data:
            return "Sorry, I couldn't find anything about that. There might be an error with your Serper API key."
        
        results = data['organic']
        string = []
        for result in results[:top_result_to_return]:
            try:
                string.append('\n'.join([
                    f"Title: {result['title']}",
                    f"Link: {result['link']}",
                    f"Snippet: {result['snippet']}",
                    "\n-----------------"
                ]))
            except KeyError:
                continue  # Skip malformed results

        generate_campaign_csv([{"title": result["title"], "link": urllib.parse.quote(result["link"], safe=':/?&=')} for result in results], "marketing")
        return '\n'.join(string) if string else "No valid results found."
    
    except requests.RequestException as e:
        return f"Search failed due to a network error: {str(e)}"
    
    
@tool("Search the internet for price, discounts and ratings of large sportwear companies.")
def shopping_tool(query: str) -> str:
    """Useful to search the internet about price, discounts and ratings of large sportwear companies."""
    print(">>>>>>>>>>> query", query)
    # Implementation goes here
    url = "https://google.serper.dev/shopping"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': os.environ['SERPER_API_KEY'],
        'content-type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if 'shopping' not in response.json():
        return "Sorry, I couldn't find anything about that. There might be an error with your Serper API key."
    string = []
    search_results = response.json()['shopping']
    if not len(search_results):
        return "Couldn't find any data"
    if len(search_results):
        for result in search_results:
            title = str(result.get('title', 'N/A'))
            link = str(result.get('link', 'N/A'))
            price = str(result.get('price', 'N/A'))
            rating = str(result.get('rating', 'N/A'))
            rating_count = str(result.get('ratingCount', 'N/A'))
            source = str(result.get('source', 'N/A'))
            
            string.append('\n'.join([
                f"Title: {title}", f"Link: {link}",
                f"Price: {price}", "\n-----------------",
                f"Rating: {rating}",
                f"Rating count: {rating_count}",
                f"Source: {source}"
            ]))
    generate_campaign_csv(search_results, "pricing")
                
    return '\n'.join(string)