from bs4 import BeautifulSoup
import requests
import string

class Crawler:
    def __init__(self, base_url: str, data_file: str):
        self.url: str = base_url
        self.results_file_path: str = data_file
        self.visited_urls: set[str] = set()

    def request_page(self, url: str) -> None:
        """
        Fetches the content of the given URL and returns all words in a list
        """
        response = requests.get(url)

        if response.status_code == 200:
            html_content = response.text
            self.extract_text_from_html(html_content)
        else:
            print(f"Failed to fetch page: {response.status_code}")

    
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
        except:
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
            list[str]: list of words without puntuation
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


c = Crawler("temp", "temp")

c.request_page("https://quotes.toscrape.com/tag/love/")