"""
Module: http_client.py
Description: Handles HTTP requests for the campervan web scraper. Utilizes 
             curl_cffi to spoof TLS fingerprints and bypass WAFs.
"""

from curl_cffi import requests
from typing import Optional

class WebScraperClient:
    """
    A client to handle HTTP GET requests securely and efficiently, bypassing basic anti-bot protections.
    """

    def __init__(self):
        # 'impersonate' automatically configures headers and TLS fingerprints to match Chrome
        self.session = requests.Session(impersonate="chrome110")

    def fetch_html(self, url: str) -> Optional[str]:
        """
        Sends a GET request to the specified URL and returns the HTML content.

        Args:
            url (str): The target URL to scrape.

        Returns:
            Optional[str]: The HTML content as a string if successful, None otherwise.
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
            
        except Exception as e:
            print(f"[ERROR] Failed to fetch data from {url}. Reason: {e}")
            return None
