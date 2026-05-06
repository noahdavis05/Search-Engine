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


SEARCH_PRINT_INDEX_CASES = [
    (
        # term present in multiple pages
        "python",
        [
            ("https://example.com/search", 2),
            ("https://example.com/about", 1),
            ("https://example.com/docs", 1),
        ],
    ),
    (
        # single-page term
        "noah",
        [("https://example.com/about", 1)],
    ),
    (
        # missing term should print a not-found message
        "nonexistentterm",
        [],
    ),
]


@pytest.mark.parametrize("keyword, expected_rows", SEARCH_PRINT_INDEX_CASES)
def test_print_index_table(keyword: str, expected_rows: list[tuple], capsys: "pytest.CaptureFixture[str]") -> None:
    """Testing the output table produced by the print_index function
    """
    s = Search()

    s.scraped_data = SEARCH_PLAIN_DATA
    s.indexed_data = SEARCH_INDEXED_DATA

    s.print_index(keyword)
    captured = capsys.readouterr()
    out = captured.out

    if not expected_rows:
        assert "not in index" in out
        return

    assert "Occurrences" in out

    for url, count in expected_rows:
        assert any((url in line and f"| {count}" in line) for line in out.splitlines())