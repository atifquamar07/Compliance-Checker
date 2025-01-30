import trafilatura
from bs4 import BeautifulSoup
import requests
from typing import Dict, List, Tuple
from termcolor import colored

class WebScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Compliance-Checker-Bot/1.0"
        }

    async def fetch_content(self, url: str) -> Dict[str, str]:
        """
        Fetches and processes webpage content, returning both raw HTML and cleaned text.
        Also extracts meta information and important page sections.
        """
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            html = response.text
            
            # Extract clean text using trafilatura
            cleaned_text = trafilatura.extract(html)
            
            # Parse HTML for structured content
            soup = BeautifulSoup(html, 'html.parser')
            
            output = {
                "clean_text": cleaned_text,
                "meta_info": self._extract_meta_info(soup)
            }
            
            # print("Content fetched: ")
            # print(colored(output['clean_text'], "black", "on_white"))
            # # print(colored(output['sections'], "white", "on_red"))
            # print(colored(output['meta_info'], "black", "on_cyan"))
            
            return output
        except Exception as e:
            raise Exception(f"Failed to fetch content: {str(e)}")

    def _extract_meta_info(self, soup: BeautifulSoup) -> Dict[str, str]:
        """
        Extracts metadata from the webpage.
        """
        return {
            "title": soup.title.string if soup.title else "",
            "meta_description": soup.find("meta", {"name": "description"})["content"] if soup.find("meta", {"name": "description"}) else "",
            "og_title": soup.find("meta", {"property": "og:title"})["content"] if soup.find("meta", {"property": "og:title"}) else ""
        }
