import pytest 
import json
from src.indexer import Indexer
from src.crawler import BASE_URL
from unittest.mock import MagicMock, mock_open, patch



CLEANING_TEST_CASES = [
    (
        ["Running", "faster", "the", "cats"], 
        ["run", "fast", "cat"]
    ),
    (
        ["I", "am", "Noah"],
        ["noah"]
    ),
    (
        ["Tuesday", "Wednesday", "Friday"],
        ["tuesday", "wednesday", "friday"]
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



INDEXING_TEST_CASES = [
    (
        {BASE_URL: ["tuesday", "wednesday", "friday"]},
        {
            "tuesday": {BASE_URL: [0]},
            "wednesday": {BASE_URL: [1]},
            "friday": {BASE_URL: [2]}
        }
    ),
    (
        {
            BASE_URL: ["tuesday", "wednesday", "friday"],
            BASE_URL + "/page": ["monday", "tuesday", "saturday"]
        },
        {
            "monday": {BASE_URL+"/page": [0]},
            "tuesday": {BASE_URL: [0], BASE_URL+"/page":[1]},
            "wednesday": {BASE_URL:[1]},
            "friday": {BASE_URL:[2]},
            "saturday": {BASE_URL+"/page": [2]}
        }
    )

]
@pytest.mark.parametrize("input_dict, indexed_dict", INDEXING_TEST_CASES)
def test_indexing(input_dict, indexed_dict):
    idx = Indexer()

    result = idx.create_inverted_index(input_dict)

    assert result == indexed_dict

FULL_INDEXING_TEST_CASES = [
    (
        {BASE_URL: ["tuesday", "wednesday", "friday"]},
        {
            "tuesday": {BASE_URL: [0]},
            "wednesday": {BASE_URL: [1]},
            "friday": {BASE_URL: [2]}
        }
    ),
    (
        {
            BASE_URL: ["Tuesday", "Wednesday", "Friday", "I"],
            BASE_URL + "/page": ["monday", "tuesday", "saturday"]
        },
        {
            "monday": {BASE_URL+"/page": [0]},
            "tuesday": {BASE_URL: [0], BASE_URL+"/page":[1]},
            "wednesday": {BASE_URL:[1]},
            "friday": {BASE_URL:[2]},
            "saturday": {BASE_URL+"/page": [2]}
        }
    )

]
@pytest.mark.parametrize("input_dict, indexed_dict", FULL_INDEXING_TEST_CASES)
def test_full_indexing_pipeline(input_dict, indexed_dict, tmp_path):
    idx = Indexer()
    temp_results_file = tmp_path / "results.json"
    idx.indexed_data_path = temp_results_file

    # mock json.loads within the indexer module to return the input data
    with patch("src.indexer.json.load", return_value=input_dict):
        # stop it from trying to open non-existent file
        with patch("pathlib.Path.open", mock_open()):
            idx.index()

    
    assert temp_results_file.exists()
    with open(temp_results_file, "r", encoding="utf-8") as f:
        saved_data = json.load(f)

    assert saved_data == indexed_dict