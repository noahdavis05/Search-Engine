"""Unit tests for `src.main` CLI glue code.

These tests focus on ensuring the command dispatch, input validation
and high-level orchestration around `Crawler`, `Indexer` and `Search`
behave correctly. The actual implementations of those classes are
mocked because they are covered by separate unit tests.
"""

from unittest.mock import MagicMock, patch
import pytest

from src import main


def test_help_prints_menu(capsys: "pytest.CaptureFixture[str]") -> None:
    """Tests that the help menu prints the available CLI commands."""
    main.help()
    captured = capsys.readouterr()
    assert "SEARCH ENGINE COMMANDS" in captured.out
    assert "build" in captured.out
    assert "load" in captured.out


def test_find_no_index_loaded(capsys: "pytest.CaptureFixture[str]") -> None:
    """Tests that `find` refuses to run before the index is loaded."""
    main.find(["find", "term"], None)
    captured = capsys.readouterr()
    assert "Index must be loaded to memory" in captured.out


def test_find_empty_search_term(capsys: "pytest.CaptureFixture[str]") -> None:
    """Tests that `find` rejects an empty query without calling search."""
    s = MagicMock()
    main.find(["find"], s)
    captured = capsys.readouterr()
    assert "You must enter a search term" in captured.out
    assert not s.search.called


def test_find_prints_results(capsys: "pytest.CaptureFixture[str]") -> None:
    """Tests that `find` prints each search result returned by `Search.search`.

    `Search.search` is mocked so only the CLI formatting and iteration logic are
    being checked.
    """
    s = MagicMock()
    s.search.return_value = [("https://a.example", 1), ("https://b.example", 2)]
    main.find(["find", "a"], s)
    captured = capsys.readouterr()
    out = captured.out.strip().splitlines()
    # ensure both urls printed
    assert any("https://a.example" in line for line in out)
    assert any("https://b.example" in line for line in out)


def test_print_index_no_index_loaded(capsys: "pytest.CaptureFixture[str]") -> None:
    """Tests that `print_index` refuses to run before loading the index."""
    main.print_index(["print", "term"], None)
    captured = capsys.readouterr()
    assert "Index must be loaded to memory" in captured.out


def test_print_index_no_term_specified(capsys: "pytest.CaptureFixture[str]") -> None:
    """Tests that `print_index` requires a term before delegating to search."""
    s = MagicMock()
    main.print_index(["print"], s)
    captured = capsys.readouterr()
    assert "Specify the term you want the index for." in captured.out
    assert not s.print_index.called


def test_print_index_calls_search_print_index(capsys: "pytest.CaptureFixture[str]") -> None:
    """Tests that `print_index` delegates to `Search.print_index` with the term."""
    s = MagicMock()
    main.print_index(["print", "hello"], s)
    s.print_index.assert_called_once_with("hello")


def test_load_search_not_exists(capsys: "pytest.CaptureFixture[str]") -> None:
    """Tests that `load` reports a missing index when `Search()` fails.

    `Search()` is mocked to raise `RuntimeError` so the error path can be
    checked without needing real index files on disk.
    """
    with patch.object(main, "Search", side_effect=RuntimeError):
        res = main.load(None)
    captured = capsys.readouterr()
    assert res is None
    assert "The search index doesn't exist" in captured.out


def test_load_success_creates_search(capsys: "pytest.CaptureFixture[str]") -> None:
    """Tests that `load` creates a `Search` object and confirms success."""
    fake_search = MagicMock()
    with patch.object(main, "Search", return_value=fake_search):
        res = main.load(None)
    captured = capsys.readouterr()
    assert res is fake_search
    assert "Index loaded to memory" in captured.out


def test_load_returns_existing(capsys: "pytest.CaptureFixture[str]") -> None:
    """Tests that `load` reuses an existing `Search` instance."""
    s = MagicMock()
    res = main.load(s)
    captured = capsys.readouterr()
    assert res is s
    assert "Index loaded to memory" in captured.out


def test_build_calls_crawler_and_indexer() -> None:
    """Tests that `build` creates the crawler and indexer and runs both steps.

    `Crawler` and `Indexer` are mocked because their own behavior is covered by
    dedicated tests; this test only checks the orchestration in `main`.
    """
    fake_crawler = MagicMock()
    fake_indexer = MagicMock()
    with patch.object(main, "Crawler", return_value=fake_crawler) as pc, \
         patch.object(main, "Indexer", return_value=fake_indexer) as pi:
        main.build()
    fake_crawler.crawl_site.assert_called_once()
    fake_indexer.index.assert_called_once()


def test_main_flow_handles_empty_and_invalid_and_exit(
    monkeypatch: "pytest.MonkeyPatch",
    capsys: "pytest.CaptureFixture[str]",
) -> None:
    """Tests the interactive command loop for empty, invalid, and exit input."""
    # supply inputs: empty -> invalid -> exit
    inputs = ["", "badcommand", "exit"]
    monkeypatch.setattr("builtins.input", lambda prompt=None, it=iter(inputs): next(it))

    # patch help to avoid long output
    with patch.object(main, "help", return_value=None):
        main.main()

    captured = capsys.readouterr()
    assert "Must enter a command" in captured.out
    assert "Invalid Command" in captured.out
