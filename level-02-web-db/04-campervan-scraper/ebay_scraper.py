"""
Module: ebay_scraper.py
Description: Coordinates localized automation tasks, commanding Selenium to pull
             HTML sources before parsing through BeautifulSoup text nodes.
"""

import argparse
import subprocess
from bs4 import BeautifulSoup
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Import the modified headful downloader class
from html_downloader import AutomatedHtmlDownloader

class EbayScraper:
    def __init__(self):
        self.console = Console()
        self.base_url = "https://www.ebay.co.uk/sch/i.html?_nkw="

    def run_automation_pipeline(self, search_query: str, max_price: float) -> None:
        """
        Coordinates the end-to-end flow: orders the browser to save the HTML
        snapshot locally, then triggers the BeautifulSoup node evaluation.
        """
        local_cache_file = "ebay_temp_search.html"
        formatted_query = search_query.replace(" ", "+")
        target_url = f"{self.base_url}{formatted_query}"
        
        self.console.print(f"[bold yellow][*] Initializing automated live pipeline for: '{search_query}'[/bold yellow]")
        
        # Instantiate and execute the visible browser downloader
        downloader = AutomatedHtmlDownloader()
        download_success = downloader.save_page_to_local(target_url, local_cache_file)
        
        if not download_success:
            self.console.print("[bold red][!] Pipeline execution stopped: Browser extraction failed.[/bold red]")
            return

        self.console.print("[bold green][*] HTML secure dump saved. Initializing BeautifulSoup parser...[/bold green]\n")
        self.process_local_file(local_cache_file, max_price)

    def process_local_file(self, file_path: str, max_price: float) -> None:
        """Reads the downloaded HTML snapshot file from disk."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
            self._parse_items(html_content, max_price)
        except FileNotFoundError:
            self.console.print(f"[bold red][!] File error: '{file_path}' does not exist.[/bold red]")

    def _parse_items(self, html: str, max_price: float) -> None:
        """Extracts DOM nodes, applies keyword matching constraints, and prints Rich panels."""
        soup = BeautifulSoup(html, 'html.parser')
        listings = soup.select("li.s-card")
        
        self.console.print(f"[bold cyan][*] Processing {len(listings)} listings from snapshot against limit: £{max_price}[/bold cyan]\n")

        for item in listings:
            title_node = item.select_one(".s-card__title")
            price_node = item.select_one(".s-card__price")
            link_node = item.select_one(".s-card__link")

            if title_node and price_node and link_node:
                title = title_node.get_text(strip=True)
                price_str = price_node.get_text(strip=True)
                listing_url = link_node.get('href', '').split('?')[0]
                
                if "Shop on eBay" in title:
                    continue

                prefixes_to_clear = ["New listing", "Opens in a new window or tab"]
                for prefix in prefixes_to_clear:
                    title = title.replace(prefix, "").strip()

                title_lower = title.lower()
                required_keywords = ["bongo", "camper"]
                if not any(keyword in title_lower for keyword in required_keywords):
                    continue

                clean_price_str = price_str.replace("£", "").replace("$", "").replace(",", "")
                try:
                    price = float(clean_price_str)
                except ValueError:
                    continue

                if price <= max_price:
                    # Optional background ping system notification
                    try:
                        subprocess.run(['notify-send', 'Match!', f'£{price} - {title}'], check=False)
                    except Exception:
                        pass

                    # Construct text element with embedded terminal hyperlinking specs
                    card_content = Text()
                    card_content.append(f"Price: £{price}\n", style="bold green")
                    card_content.append("🔗 Ctrl+Click to open listing details in browser", style=f"bold blue link {listing_url}")

                    panel = Panel(
                        card_content,
                        title=f"🚐 [bold white]{title}[/bold white]",
                        expand=False,
                        border_style="cyan"
                    )
                    self.console.print(panel)

if __name__ == "__main__":
    # Configure the command-line argument interface
    parser = argparse.ArgumentParser(description="Automated eBay Real-Time Snapshot CLI Tool")
    parser.add_argument("--query", type=str, help="Search parameters to execute live on eBay")
    parser.add_argument("--max-price", type=float, help="Maximum cost threshold criteria")
    
    args = parser.parse_args()
    scraper = EbayScraper()

    # Check if the user bypassed the flags and execute the interactive wizard
    if args.query is None:
        try:
            print("=" * 60)
            print("         EBAY CAMPERVAN MONITOR - INTERACTIVE WIZARD        ")
            print("=" * 60)
            
            # Step 1: Prompt interactively for the search query
            user_query = input("[?] Enter the vehicle to search (e.g., 'VW T5 campervan'): ").strip()
            while not user_query:
                user_query = input("[!] Query cannot be empty. Try again: ").strip()
            
            # Step 2: Prompt interactively for the budget limit
            raw_price = input("[?] Enter your maximum budget threshold (e.g., 5000): ").strip()
            while True:
                try:
                    user_max_price = float(raw_price.replace(",", ""))
                    break
                except ValueError:
                    raw_price = input("[!] Invalid number. Enter a numeric budget limit: ").strip()
            
            print("=" * 60)
            # Trigger the automation pipeline using user interactive inputs
            scraper.run_automation_pipeline(user_query, user_max_price)
            
        except KeyboardInterrupt:
            print("\n\n[!] Operation cancelled by user. Exiting safely.")
    else:
        # If flags were provided, enforce default value if max_price is missing
        final_max_price = args.max_price if args.max_price is not None else 5000.0
        scraper.run_automation_pipeline(args.query, final_max_price)