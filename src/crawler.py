from bs4 import BeautifulSoup
import requests
import string
from pathlib import Path
import json
import time

BASE_URL = "https://quotes.toscrape.com"
POLITENESS_WINDOW = 6

class Crawler:
    def __init__(self, base_url: str = BASE_URL):
        self.visited_urls: dict[str, dict] = {
            base_url: {"status": "unvisited", "order": 0}
        }

        # set the path for where data will be saved
        src_dir = Path(__file__).resolve().parent
        self.data_dir = src_dir.parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.results_file_path = self.data_dir / "raw_pages.json"
        # ensure the results file exists
        if not self.results_file_path.exists():
            self.results_file_path.write_text("{}", encoding="utf-8")

    def request_page(self, url: str) -> str:
        """Requests the content of a given URL, extracts the text and saves it to JSON file

        Args:
            url (str): URL of the given page to be scraped.

        Returns:
            str: The HTML content of the page is returned to pass to another function.
        """
        try:
            response = requests.get(url, timeout=10) 
            response.raise_for_status() 

            html_content = response.text
            extracted_text = self.extract_text_from_html(html_content)
            self.save_page_to_json(extracted_text, url)
            return html_content
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}") 
        except Exception as err:
            print(f"An unexpected error occurred: {err}")

        return ""

    def extract_text_from_html(self, html_content:str) -> list[str]:
        """Given the pure HTML content of a webpage this function extracts only
        the important text content

        Args:
            html_content (str): HTML content of a webpage as one string.
        
        Returns:
            list[str]: A list of every important word from the html, stripped of punctuation.
        """
        soup = BeautifulSoup(html_content, "html.parser")

        all_words = []

        # get the page title (if there is one)
        try:
            page_title = soup.find("h3").get_text(strip=False)
            title_words = page_title.split()
            all_words += self.clean_list_of_strings(title_words)
        except AttributeError:
            print("No Page Title Found")
        
        # scrape just each quote, its author, and tags
        try:
            quote_elements = soup.find_all("div", class_="quote")
            for quote in quote_elements:
                text = quote.find("span", class_="text").get_text(strip=True)
                author = quote.find("small", class_="author").get_text(strip=True)
                tags = quote.find_all("a", class_="tag")

                temp_tags = []
                for tag in tags:
                    tag_text = tag.get_text()
                    temp_tags.append(tag_text)
                
                # split text, and author into lists of strings and append to all_words in correct order
                split_text = text.split()
                cleaned_text = self.clean_list_of_strings(split_text)
                split_author = author.split()
                cleaned_author = self.clean_list_of_strings(split_author)
                cleaned_tags = self.clean_list_of_strings(temp_tags)

                all_words += cleaned_text
                all_words += cleaned_author
                all_words += cleaned_tags
                
        except Exception as e:
            print(f"Error scraping quotes: {e}")

        #print(all_words)

        return all_words
                
    def clean_list_of_strings(self, strings: list[str]) -> list[str]:
        """Takes a list of strings and strips all punctuation at the beginning or end of string
        It also ensures all text is in lower case.

        Args:
            strings (list[str]): list of words with punctuation

        Returns:
            list[str]: list of words without punctuation
        """
        extended_punctuation = string.punctuation + "“”‘’—–…"
        cleaned_list = []
        for word in strings:
            if word == " ":
                continue
            cleaned_word = word.lower().strip(extended_punctuation)
            if cleaned_word != "":
                cleaned_list.append(cleaned_word)
        return cleaned_list
    
    def save_page_to_json(self, extracted_text: list[str], url: str):
        """Takes the URL and text content for a page and saves the results to our
        raw data file.

        Args:
            extracted_text (list[str]): Cleaned text from the webpage in form of a list
            url (str): url of the page
        """
        file_path = Path(self.results_file_path)
        data: dict[str, list[str]] = {}

        # load the data
        if file_path.exists() and file_path.stat().st_size > 0:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    # ensure the loaded data is actually a dictionary
                    if isinstance(loaded_data, dict):
                        data = loaded_data
                    else:
                        data = {}
            except json.JSONDecodeError:
                data = {}

        # add the new data
        data[url] = extracted_text

        # write back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)


    def crawl_site(self) -> None:
        """Crawls the whole website using breadth first, visiting every single link within the website
        Crawled pages are saved to the JSON file.
        """
        while len([k for k, v in self.visited_urls.items() if v['status'] == "unvisited"]) > 0:
            url = min(
                (k for k, v in self.visited_urls.items() if v['status'] == "unvisited"),
                key=lambda k: self.visited_urls[k]['order']
            )

            # scrape the given url
            html_content = self.request_page(url) 

            # get all links from the page
            self.extract_all_links(html_content)

            self.visited_urls[url]["status"] = "visited"

            print(f"Visiting page {url}, page number {len(self.visited_urls)}")

            time.sleep(POLITENESS_WINDOW)

    
    def extract_all_links(self, html_content: str) -> None:
        """Extracts all links for a given page, and adds all unvisited links to the dictionary
        used in breadth first search.

        Args:
            html_content (str): Raw HTML content of the current page.
        """
        soup = BeautifulSoup(html_content, "html.parser")

        try:
            links = soup.find_all("a", href=True)
            
            urls = []
            for link in links:
                # ensure we never scrape links which leave this website
                if "https://" in link.get("href") or "www." in link.get("href"):
                    continue
                temp_url = BASE_URL + link.get("href")
                urls.append(temp_url)
                
            
            # now check if these URLs are already in our list
            for url in urls:
                if url not in self.visited_urls.keys():
                    self.visited_urls[url] = {"status": "unvisited", "order": len(self.visited_urls) + 1}
        except Exception as e:
            print(f"Error extracting links: {e}")

               