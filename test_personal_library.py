# virtual environment
# multiple projects -> different versions of libraries
import pytest
from ASG02 import view_books, add_or_update_book, remove_book, search_books, show_author_statistics


def test_view_books_empty(capsys):
    """Test viewing an empty library shows the correct message."""
    library = {}
    view_books(library)
    captured = capsys.readouterr()
    assert "Your library is empty." in captured.out


def test_view_books_sorted_and_formatted(capsys):
    """Test books are formatted and displayed alphabetically by title from the dictionary."""
    library = {
        "The Hobbit": {"author": "J.R.R. Tolkien", "year": 1937},
        "Dune": {"author": "Frank Herbert", "year": 1965},
    }
    view_books(library)
    captured = capsys.readouterr()

    # Dune should appear before The Hobbit due to alphabetical sorting
    expected_dune = "1. Dune by Frank Herbert (1965)"
    expected_hobbit = "2. The Hobbit by J.R.R. Tolkien (1937)"

    assert expected_dune in captured.out
    assert expected_hobbit in captured.out
    assert captured.out.index(expected_dune) < captured.out.index(expected_hobbit)


def test_add_or_update_book_add_new(monkeypatch, capsys):
    """Test adding a new book inserts it into the dictionary and reports added."""
    library = {}

    inputs = iter(["Dune", "Frank Herbert", "1965"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    add_or_update_book(library)

    assert "Dune" in library
    assert library["Dune"] == {"author": "Frank Herbert", "year": 1965}

    captured = capsys.readouterr()
    assert '"Dune" was added.' in captured.out


def test_add_or_update_book_update_existing(monkeypatch, capsys):
    """Test entering an existing title updates its details and reports updated."""
    library = {"Dune": {"author": "Frank Herbert", "year": 1965}}

    # Provide updated author/year for the existing title
    inputs = iter(["Dune", "F. Herbert", "1966"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    add_or_update_book(library)

    assert len(library) == 1
    assert library["Dune"] == {"author": "F. Herbert", "year": 1966}

    captured = capsys.readouterr()
    assert '"Dune" was updated.' in captured.out


def test_add_or_update_book_invalid_year(monkeypatch, capsys):
    """Test entering non-numeric year rejects input without altering the dictionary."""
    library = {}

    inputs = iter(["1984", "George Orwell", "nineteen-eighty-four"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    add_or_update_book(library)

    assert len(library) == 0
    captured = capsys.readouterr()
    assert "Year must be a valid integer." in captured.out


def test_remove_book_success(monkeypatch, capsys):
    """Test removing a book deletes its key from the dictionary."""
    library = {"Dune": {"author": "Frank Herbert", "year": 1965}}

    monkeypatch.setattr("builtins.input", lambda _: "Dune")

    remove_book(library)

    assert "Dune" not in library
    assert len(library) == 0

    captured = capsys.readouterr()
    assert "'Dune' has been removed from your library." in captured.out


def test_remove_book_not_found(monkeypatch, capsys):
    """Test attempting to remove a non-existent title leaves the dictionary unchanged."""
    library = {"Dune": {"author": "Frank Herbert", "year": 1965}}

    monkeypatch.setattr("builtins.input", lambda _: "Foundation")

    remove_book(library)

    assert "Dune" in library
    assert len(library) == 1

    captured = capsys.readouterr()
    assert "'Foundation' was not found in the library." in captured.out


def test_remove_book_empty_library(capsys):
    """Test removing from an empty library alerts the user immediately without prompting."""
    library = {}

    remove_book(library)

    captured = capsys.readouterr()
    assert "Your library is empty. Nothing to remove." in captured.out


def test_search_books_partial_match(monkeypatch, capsys):
    """Test case-insensitive partial matching across dictionary keys."""
    library = {
        "Dune": {"author": "Frank Herbert", "year": 1965},
        "Dune Messiah": {"author": "Frank Herbert", "year": 1969},
        "The Hobbit": {"author": "J.R.R. Tolkien", "year": 1937},
    }

    monkeypatch.setattr("builtins.input", lambda _: "dune")

    search_books(library)

    captured = capsys.readouterr()
    assert "1. Dune by Frank Herbert (1965)" in captured.out
    assert "2. Dune Messiah by Frank Herbert (1969)" in captured.out
    assert "The Hobbit" not in captured.out


def test_search_books_not_found(monkeypatch, capsys):
    """Test search with no matching titles displays clear notification."""
    library = {"Dune": {"author": "Frank Herbert", "year": 1965}}

    monkeypatch.setattr("builtins.input", lambda _: "Foundation")

    search_books(library)

    captured = capsys.readouterr()
    assert "No books found matching 'foundation'." in captured.out


def test_search_books_empty_library(capsys):
    """Test searching an empty library alerts the user immediately."""
    library = {}

    search_books(library)

    captured = capsys.readouterr()
    assert "Your library is empty." in captured.out


def test_show_author_statistics_empty(capsys):
    """Test showing author statistics on an empty library outputs the empty message."""
    library = {}
    show_author_statistics(library)
    captured = capsys.readouterr()
    assert "Your library is empty." in captured.out


def test_show_author_statistics_counts_and_sorting(capsys):
    """Test authors are counted accurately and sorted alphabetically with proper pluralization."""
    library = {
        "Dune": {"author": "Frank Herbert", "year": 1965},
        "Dune Messiah": {"author": "Frank Herbert", "year": 1969},
        "The Hobbit": {"author": "J.R.R. Tolkien", "year": 1937},
    }
    show_author_statistics(library)
    captured = capsys.readouterr()

    expected_herbert = "Frank Herbert: 2 books"
    expected_tolkien = "J.R.R. Tolkien: 1 book"

    assert expected_herbert in captured.out
    assert expected_tolkien in captured.out
    # Frank Herbert should appear before J.R.R. Tolkien alphabetically
    assert captured.out.index(expected_herbert) < captured.out.index(
        expected_tolkien
    )