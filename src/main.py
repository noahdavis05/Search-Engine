import sys


# try except statement is used for imports as pytest runs from the parent dir
# therefore the import routes are different to just running main.py
try:
    from src.crawler import Crawler
    from src.indexer import Indexer
    from src.search import Search
except Exception:
    from crawler import Crawler
    from indexer import Indexer
    from search import Search

def main():
    """
    Main command line argument function, takes the user function and runs correct code
    """
    s = None
    while True:
        try:
            user_input = input("> ").strip()

            arguments = user_input.split()

            if len(arguments) == 0:
                print("Must enter a command")
                help()
                continue

            # check arguments[0]
            if arguments[0].lower() == "help":
                help()
            elif arguments[0].lower() == "build":
                build()
            elif arguments[0].lower() == "load":
                s = load(s)
            elif arguments[0].lower() == "print":
                print_index(arguments, s)
            elif arguments[0].lower() == "find":
                find(arguments, s)
            elif arguments[0].lower() == "exit":
                break
            else:
                print("Invalid Command")
                continue
        except EOFError:
            break
        except KeyboardInterrupt:
            print("Exiting ...")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break
        

def help():
    """
    Prints a formatted guide of available commands for the interactive shell.
    """
    print("\n" + "="*45)
    print("           SEARCH ENGINE COMMANDS")
    print("="*45)
    
    # Using a list of tuples to keep things organized
    commands = [
        ("build", "Crawl the website and save the index to disk."),
        ("load",  "Load the existing index from the file system."),
        ("print <word>", "Display the inverted index for a specific word."),
        ("find <query>", "Search for pages containing the phrase/words."),
        ("help",  "Show this help menu."),
        ("exit",  "Close the search tool.")
    ]
    
    for cmd, desc in commands:
        # Left-align the command in 15 spaces, then print the description
        print(f" {cmd:<15} : {desc}")
    
    print("="*45 + "\n")


def find(arguments: list[str], s: Search | None):
    """Use the search engine to get a list of sites printed which matches the arguments

    Args:
        arguments (list[str]): list of the search terms
        s (Search | None): Search class, if it exists the search is done, otherwise it fails
    """
    if s == None:
        print("Index must be loaded to memory, run the 'load' command first.")
        return 
    
    search_phrase = " ".join(arguments[1:])
    if search_phrase == "":
        print("You must enter a search term, enter 'help' for more information.")
        return 
    search_results = s.search(search_phrase)

    for i, search_result in enumerate(search_results):
        print(f"{i:<5} | {search_result[0]}")

    return 


def print_index(arguments: list[str], s: Search | None):
    """Print the inverted index for a given word

    Args:
        arguments (list[str]): list of arguments, but we only use arguments[1] for search if exists
        s (Search | None): Search class, if it exists the search is done, otherwise it fails
    """
    if s == None:
        print("Index must be loaded to memory, run the 'load' command first.")
        return 
    
    if len(arguments) < 2:
        print("Specify the term you want the index for.")
        return

    s.print_index(arguments[1])

    return 

def load(s: Search | None) -> Search | None:
    """Load the inverted index into memory

    Args:
        s (Search | None): Search class, likely doesn't exist but will be created

    Returns:
        Search | None: Search class will be returned if no issues making it
    """
    if s == None:
        try:
            s = Search()
        except RuntimeError:
            print("The search index doesn't exist. Build it with the build command")
            return None
    print("Index loaded to memory")

    return s

def build():
    """Crawl the website and create the inverted index
    """
    c = Crawler()
    c.crawl_site()
    i = Indexer()
    i.index()

if __name__ == "__main__":
    main()