import pytest 
from globals import SEARCH_PLAIN_DATA, SEARCH_INDEXED_DATA
from unittest.mock import MagicMock, mock_open, patch
from src.search import Search


SEARCH_TEST_CASES = [
    (
        # single term
        "noah",
        ["https://example.com/about"]
    ),
    (
        # multiple terms
        "noah engine",
        ["https://example.com/about"]
    ),
    (
        # multiple terms but never on same webpage
        "noah crawler",
        []
    ),
    (
        # word appears in all webpages, but more in /search
        "python",
        ["https://example.com/search", "https://example.com/about", "https://example.com/docs"]
    ),
    (
        # python appears in all 3 pages, but code in only 2
        "python code",
        ["https://example.com/search", "https://example.com/docs"]
    )
]
@pytest.mark.parametrize("search_terms, webPages", SEARCH_TEST_CASES)
def test_search_clean_way(search_terms, webPages):
    s = Search()

    # mock the json data
    s.scraped_data = SEARCH_PLAIN_DATA
    s.indexed_data = SEARCH_INDEXED_DATA

    results = s.search(search_terms)

    results = [i[0] for i in results]
    assert results == webPages