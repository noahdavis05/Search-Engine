from pathlib import Path
import spacy
import json

class Indexer:
    def __init__(self):
        src_dir = Path(__file__).resolve().parent
        self.data_dir = src_dir.parent / "data"
        self.scraped_data_path = self.data_dir / "raw_pages.json"

        self.indexed_data_path = self.data_dir / "indexed_data.json"

        self.nlp = spacy.load("en_core_web_sm")
        self.stop_words = self.nlp.Defaults.stop_words

    def clean_scraped_data(self) -> dict:
        """Reads the already scraped website data and cleans it using scrapy library.
        This lemmatizes words and removes common terms.

        Returns:
            dict: Dictionary of clean data mapping websites to all words on it (in order of occurrence)
        """
        # read in the scraped JSON data
        with self.scraped_data_path.open("r", encoding="utf-8") as f:
            scraped_data = json.load(f)


        # filter out stop words from each list of words and lemmatize words to bring it 
        # to its simplest form. E.g. "running" -> "run". This is useful for search terms
        # if someone searches up "running", but only "run" is in the webpage it won't match
        for key, value in scraped_data.items():
            if isinstance(value, list):
                raw_string = " ".join(value)  
                doc = self.nlp(raw_string)

                scraped_data[key] = [
                    token.lemma_.lower() 
                    for token in doc 
                    if not token.is_stop and not token.is_punct and not token.is_space
                ]

        return scraped_data
    
    def create_inverted_index(self, scraped_data: dict) -> dict:
        """Takes the cleaned scraped data as a dictionary and inverts it.
        Meaning it maps words to the websites they appear on, and what index within
        each page they appear on.

        Args:
            scraped_data (dict): Scraped and cleaned input dicitonary

        Returns:
            dict: dictionary mapping words to websites
        """
        inverted_index = {}

        # iterate over all words for each webpage
        for url, words in scraped_data.items():
            # iterate over each word from this page
            for index, word in enumerate(words):
                if word in inverted_index.keys():
                    # word exists - now need to check if the website is already a key for this word
                    if url in inverted_index[word].keys():
                        # the word has already appeared for this website
                        inverted_index[word][url].append(index)
                    else:
                        # word has not appeared for this website - therefore add new sub dictionary
                        inverted_index[word][url] = [index]
                else:
                    # word doesn't exist yet so make a new record
                    inverted_index[word] = {
                        url: [index]
                    }
        
        return inverted_index

    
    def save_inverted_index(self, inverted_index: dict) -> None:
        """Saves the inverted index to its file.
        The file is completely overwritten by this function

        Args:
            inverted_index (dict): the full dictionary to be written to the file
        """
        with open(self.indexed_data_path, "w", encoding="utf-8") as f:
            json.dump(inverted_index, f, indent=4)


    def index(self) -> None:
        """The full indexing pipeline of cleaning, inverting, and saving
        """
        scraped_data = self.clean_scraped_data()
        inverted_index = self.create_inverted_index(scraped_data)
        self.save_inverted_index(inverted_index)



if __name__ == "__main__":
    i = Indexer()
    i.index()
    

