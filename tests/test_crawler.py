import pytest 
import json
from src.crawler import Crawler, BASE_URL
from globals import HTML_CONTENT1, HTML_CONTENT2, HTML_CONTENT3, HTML_CONTENT4, HTML_CONTENT5, HTML_CONTENT6
from globals import FULL_SITE_HOME, FULL_SITE_AUTHOR, FULL_SITE_TAG_TAG




EXTRACT_TEST_CASES = [
    (
        # normal scenario where a page has a title and a quote to scrape
        HTML_CONTENT1,
        ["page", "title", "this", "is", "a", "quote", "noah", "davis", "tag"]
    ),
    (
        # normal scenario where there is a title and two quotes
        HTML_CONTENT2,
        ["page", "title", "this", "is", "a", "quote", "noah", "davis", "tag", "this", "is", "another", "quote", "noah", "davis", "tag"]
    ),
    (
        # scenario where there is no title but quotes - common on the homepage
        HTML_CONTENT3,
        ["this", "is", "a", "quote", "noah", "davis", "tag"]
    ),
    ## EDGE CASES
    ## In the case of malformed quotes - all quotes on the page are skipped
    ## Missing tags isn't considered malformed as quotes may not be tagged
    (
        # scenario where the quote is missing - haven't seen these on the website
        HTML_CONTENT4,
        ["page", "title"]
    ),
    (
        # scenario where the author is missing
        HTML_CONTENT5,
        ["page", "title"]
    ),
    (
        # scenario where tags are missing
        HTML_CONTENT6,
        ["page", "title", "this", "is", "a", "quote", "noah", "davis"]
    )
]

@pytest.mark.parametrize("html_input, expected_output", EXTRACT_TEST_CASES)
def test_extract_text_from_html(html_input, expected_output):
    """
    Run tests on the `extract_text_from_html` function
    """
    c = Crawler(BASE_URL)
    result = c.extract_text_from_html(html_input)
    assert result == expected_output


# This test mocks the request to fetch the html, and mocks the saving of the
# data to the file.
REQUEST_PAGE_TEST_CASES = [
    (
        "https://quotes.toscrape.com/",
        HTML_CONTENT1,
        ["page", "title", "this", "is", "a", "quote", "noah", "davis", "tag"]
    ),
    (
        "https://quotes.toscrape.com/",
        HTML_CONTENT2,
        ["page", "title", "this", "is", "a", "quote", "noah", "davis", "tag", "this", "is", "another", "quote", "noah", "davis", "tag"]
    )
]
@pytest.mark.parametrize("mock_url, html_content, expected_words",REQUEST_PAGE_TEST_CASES)
def test_request_page_end_to_end(requests_mock, tmp_path, mock_url, html_content, expected_words):
    temp_results_file = tmp_path / "test_raw_pages.json"
    
    c = Crawler(BASE_URL)
    c.results_file_path = temp_results_file
    
    # mock the request to return the given html
    requests_mock.get(mock_url, text=html_content)

    # execute the function
    returned_html = c.request_page(mock_url)

    # assert the function returns the correct url
    assert returned_html == html_content
    assert requests_mock.called
    assert requests_mock.call_count == 1

    # verify the content saved to the file was correct
    assert temp_results_file.exists()
    with open(temp_results_file, "r", encoding="utf-8") as f:
        saved_data = json.load(f)
    
    # The keys in the JSON should be the URL, and values the cleaned word list
    assert mock_url in saved_data
    assert saved_data[mock_url] == expected_words


## Full test with a full mock site to crawl
def test_crawl_full_site(tmp_path, requests_mock, monkeypatch):
    temp_results_file = tmp_path / "test_raw_pages.json"
    
    c = Crawler(BASE_URL)
    c.results_file_path = temp_results_file

    # mock the 3 pages on the website
    requests_mock.get(BASE_URL, text=FULL_SITE_HOME)
    requests_mock.get(BASE_URL + "/author/Noah-Davis", text=FULL_SITE_AUTHOR)
    requests_mock.get(BASE_URL + "/tag", text=FULL_SITE_TAG_TAG)

    # mock the 6 second politeness window to nothing
    monkeypatch.setattr("time.sleep", lambda x: None)

    c.crawl_site()

    assert temp_results_file.exists()
    with open(temp_results_file, "r", encoding="utf-8") as f:
        saved_data = json.load(f)

    ## assert all the URLs are in saved data
    assert BASE_URL in saved_data
    assert BASE_URL + "/author/Noah-Davis" in saved_data
    assert BASE_URL + "/tag" in saved_data

    ## assert the correct words have been added
    assert saved_data[BASE_URL] == ["page", "title", "this", "is", "a", "quote", "noah", "davis", "tag"]
    assert saved_data[BASE_URL + "/author/Noah-Davis"] == ["noah", "davis"]
    ## Note lemmatization and stop-word removal removed some 'a's from the output compared to the original HTML. But this is expected behaviour
    assert saved_data[BASE_URL + "/tag"] == ["tag", "quotes", "this", "is", "a", "quote", "about", "tag", "noah", "davis", "tag", "this", "is", "another", "quote", "about", "tag", "noah", "davis", "tag"]