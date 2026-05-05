import pytest 
import json
from src.indexer import Indexer
from src.crawler import BASE_URL
from unittest.mock import MagicMock, mock_open, patch



CLEANING_TEST_CASES = [
    (
        ["Running", "faster", "the", "cats"], 
        ["run", "fast", "cat"]
    )
]
@pytest.mark.parametrize("unclean_list, cleaned_list", CLEANING_TEST_CASES)
def test_clean_scraped_data_alt(unclean_list, cleaned_list):
    input_data = {BASE_URL: unclean_list}
    
    idx = Indexer()
    
    # mock json.loads within the indexer module to return the input data
    with patch("src.indexer.json.load", return_value=input_data):
        # stop it from trying to open non-existent file
        with patch("pathlib.Path.open", mock_open()):
            result = idx.clean_scraped_data()

    assert result[BASE_URL] == cleaned_list