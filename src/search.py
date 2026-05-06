from pathlib import Path
import spacy
import json
import math

class Search:

    def __init__(self) -> None:
        try:
            src_dir = Path(__file__).resolve().parent
            self.data_dir = src_dir.parent / "data"
            self.scraped_data_path = self.data_dir / "raw_pages.json"
            self.indexed_data_path = self.data_dir / "indexed_data.json"

            with open(self.scraped_data_path, "r", encoding="utf-8") as f:
                self.scraped_data = json.load(f)

            with open(self.indexed_data_path, "r", encoding="utf-8") as f:
                self.indexed_data = json.load(f)

            self.nlp = spacy.load("en_core_web_sm")
        except (FileNotFoundError, ValueError) as e:
            raise RuntimeError(f"Initialization Failed: {e}") from e


    def search(self, term: str) -> list[tuple]:
        """Search for a word or multiple words

        Args:
            term (str): input word

        Returns:
            str: outpur URL of best match
        """

        total_docs = len(self.scraped_data)
        cleaned_query = self.process_query(term)

        final_results = {}

        for query in cleaned_query:
            if query not in self.indexed_data:
                return []
            
            docs_with_word = len(self.indexed_data[query])
            idf = math.log(total_docs / docs_with_word)

            results = {}

            for url, positions in self.indexed_data[query].items():
                tf = len(positions) / max(len(self.scraped_data[url]),100)
                score = tf * idf
                results[url] = score
        
            for temp_url, score in results.items():
                if temp_url in final_results.keys():
                    final_results[temp_url]["score"] += score 
                    final_results[temp_url]["appeared"] += 1
                else:
                    final_results[temp_url] = {"score": score, "appeared": 1}

        required_count = len(cleaned_query)
        filtered_results = [
            (url, data["score"]) 
            for url, data in final_results.items() 
            if data["appeared"] == required_count
        ]

        sorted_output = sorted(filtered_results, key=lambda x: x[1], reverse=True)

        return sorted_output
    
    def process_query(self, query_text) -> list[str]:
        """Pre-processes the query using the same method as the indexer.
        Stop words are removed and lemmatization takes place

        Args:
            query_text (_type_): The user's input query

        Returns:
            list[str]: A filtered output query. Each word is an element of the list
        """
        doc = self.nlp(query_text)
        
        clean_query = [
            token.lemma_.lower() 
            for token in doc 
            if not token.is_stop and not token.is_punct and not token.is_space
        ]
        
        return clean_query
    
    def print_index(self, keyword: str):
        """Print the inverted index for a given term

        Args:
            keyword (str): the given word we want the index for
        """
        cleaned_keyword = self.process_query(keyword)
        
        # Check if the keyword exists after processing
        if not cleaned_keyword or cleaned_keyword[0] not in self.indexed_data:
            print(f"Term '{keyword}' not in index")
            return
        
        target_word = cleaned_keyword[0]
        
        # create a hard copy so we don't edit the old in making number of occurrences instead of indexes of poisionts
        occurrences_map = {
            page_id: len(locations) 
            for page_id, locations in self.indexed_data[target_word].items()
        }

        index = 0
        print(f"{'#':<5} | {'Page URL':<70} | {'Occurrences':<5}")
        print("-" * 95)
        for page, count in occurrences_map.items():
            index += 1
            print(f"{index:<5} | {page:<70} | {count:<5}")


        


if __name__ == "__main__":
    s = Search()
    print(s.search("gibraltar"))