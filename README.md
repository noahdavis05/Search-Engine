# Search Engine for quotes.toscrape.com

[![codecov](https://codecov.io/github/noahdavis05/Search-Engine/graph/badge.svg?token=TE1B468MLI)](https://codecov.io/github/noahdavis05/Search-Engine)
![Build Status](https://github.com/noahdavis05/Search-Engine/actions/workflows/tests.yaml/badge.svg)

A command line search engine tool which scrapes and indexes all pages on quotes.toscrape.com.
Gives the user options to view the inverted page index, and search for specific web pages containing certain terms. 

## Features

- Uses **TF-IDF** ranking to return the most relevant pages.
- Uses **spaCy** to remove common stop words (e.g., "and").
- Uses **spaCy** lemmatization (e.g., "running" → "run"); preprocessing runs during scraping and searching so queries match normalized, important terms.

## Prerequisites 
- Python 3.12 +

## Getting Started
1. Clone the repo
```
git clone https://github.com/noahdavis05/Search-Engine
cd Search-Engine
```

2. Create Python virtual environment and install dependencies
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

3. Ensure the spaCy language model is downloaded
```
python -m spacy download en_core_web_sm
```

4. Run the main.py file
```
cd src
python3 main.py
```

## Usage

Start the interactive shell by running the main script from your terminal.

Once the shell is active (indicated by the `>` prompt), you can use the following commands:

### Build
Crawls the source website, constructs the inverted index, and saves it to the file system.
```
> build
```
**Note** - The crawler uses a 6 second politeness window between requests. This makes the process very slow (about 20 minutes). This repo includes the pre-built JSON files in the `/data` directory.

**Output** - A continual stream of the current page being scraped.


### Load
Loads the previously saved index from the file system into the current session.
```
> load
Index loaded to memory
>
```

### Print
Displays the inverted index data and the total occurrence count for a specific word.
```
> print nonsense
#     | Page URL                                                               | Occurrences
-----------------------------------------------------------------------------------------------
1     | https://quotes.toscrape.com/tag/life/page/1/                           | 1    
2     | https://quotes.toscrape.com/page/2/                                    | 1    
3     | https://quotes.toscrape.com/tag/life/                                  | 1    
4     | https://quotes.toscrape.com/tag/regrets/page/1/                        | 1    
5     | https://quotes.toscrape.com/tag/fantasy/page/1/                        | 1    
6     | https://quotes.toscrape.com/page/7/                                    | 1    
> 
```

### Find
Searches for a single word or a phrase and returns a list of all pages containing the terms.
```
> find indifference
0     | https://quotes.toscrape.com/tag/indifference/page/1/
1     | https://quotes.toscrape.com/tag/activism/page/1/
2     | https://quotes.toscrape.com/tag/apathy/page/1/
3     | https://quotes.toscrape.com/tag/hate/page/1/
4     | https://quotes.toscrape.com/tag/opposite/page/1/
5     | https://quotes.toscrape.com/tag/philosophy/page/1/
6     | https://quotes.toscrape.com/tag/inspirational/page/1/
7     | https://quotes.toscrape.com/tag/inspirational/
8     | https://quotes.toscrape.com/page/2/
9     | https://quotes.toscrape.com/tag/love/page/1/
10    | https://quotes.toscrape.com/tag/love/
> 
```
```
> find sisters friends good love
0     | https://quotes.toscrape.com/tag/friends/
1     | https://quotes.toscrape.com/tag/friends/page/1/
2     | https://quotes.toscrape.com/tag/sisters/page/1/
3     | https://quotes.toscrape.com/tag/heartbreak/page/1/
4     | https://quotes.toscrape.com/tag/love/page/1/
5     | https://quotes.toscrape.com/tag/love/
6     | https://quotes.toscrape.com/page/2/
7     | https://quotes.toscrape.com/tag/life/page/1/
8     | https://quotes.toscrape.com/tag/life/
9     | https://quotes.toscrape.com/tag/inspirational/page/1/
10    | https://quotes.toscrape.com/tag/inspirational/
> 
```

### Exit
Safely closes the interactive search tool and returns to the system shell.
```
> exit
```

### Help
Displays a help message explaining the commands.
```
> help

=============================================
           SEARCH ENGINE COMMANDS
=============================================
 build           : Crawl the website and save the index to disk.
 load            : Load the existing index from the file system.
 print <word>    : Display the inverted index for a specific word.
 find <query>    : Search for pages containing the phrase/words.
 help            : Show this help menu.
 exit            : Close the search tool.
=============================================

> 
```

## Testing
This project uses `pytest` for unit testing and quality assurance. To ensure reliability, the test suite is automatically executed via **GitHub Actions** on every commit and pull request.

### Running Tests Locally
To execute the tests manually, run the following command from the **root directory** of the repository:
```
pytest
```

### Code Coverage
To measure how much of the source code is covered by the test suite, use the `pytest-cov` plugin by running:
```
pytest --cov=src
```

This will generate a report in the terminal showing the percentage of lines executed during the tests. A professional standard of 80% or higher is recommended for all core logic.




