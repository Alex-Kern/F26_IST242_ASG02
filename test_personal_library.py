# virtual environment
# multiple projects -> different versions of libraries
import pytest
from ASG02 import view_books, add_book, remove_book, search_books


def test_view_books_empty(capsys):
    """Test viewing an empty library shows the correct message."""
    library = []
    view_books(library)
    captured = capsys.readouterr()
    assert "Your library is empty." in captured.out


def test_view_books_with_items(capsys):
    """Test viewing a populated library displays 1-based index and titles."""
    library = ["1984", "The Hobbit"]
    view_books(library)
    captured = capsys.readouterr()
    assert "1. 1984" in captured.out
    assert "2. The Hobbit" in captured.out


def test_add_book_success(monkeypatch, capsys):
    """Test adding a valid book title appends it to the list."""
    library = []
    # Simulate the user typing "The Hobbit" and pressing Enter
    monkeypatch.setattr("builtins.input", lambda _: "The Hobbit")

    add_book(library)

    assert "The Hobbit" in library
    assert len(library) == 1
    captured = capsys.readouterr()
    assert "'The Hobbit' has been added to your library." in captured.out


def test_add_book_empty_input(monkeypatch, capsys):
    """Test entering an empty title rejects input and does not alter library."""
    library = []
    # Simulate user pressing Enter without typing anything
    monkeypatch.setattr("builtins.input", lambda _: "   ")

    add_book(library)

    assert len(library) == 0
    captured = capsys.readouterr()
    assert "Title cannot be empty." in captured.out



def test_remove_book_success(monkeypatch, capsys):
    """Test removing an existing book deletes it from the library."""
    library = ["The Hobbit", "1984"]
    monkeypatch.setattr("builtins.input", lambda _: "1984")

    remove_book(library)

    assert "1984" not in library
    assert library == ["The Hobbit"]
    captured = capsys.readouterr()
    assert "'1984' has been removed from your library." in captured.out


def test_remove_book_not_found(monkeypatch, capsys):
    """Test removing a book that doesn't exist leaves the library unchanged."""
    library = ["The Hobbit"]
    monkeypatch.setattr("builtins.input", lambda _: "Dune")

    remove_book(library)

    assert library == ["The Hobbit"]
    captured = capsys.readouterr()
    assert "'Dune' was not found in the library." in captured.out


def test_remove_book_empty_library(capsys):
    """Test removing from an empty library alerts the user immediately without prompting."""
    library = []
    remove_book(library)

    captured = capsys.readouterr()
    assert "Your library is empty. Nothing to remove." in captured.out


def test_search_books_found(monkeypatch, capsys):
    """Test case-insensitive partial title matching."""
    library = ["The Hobbit", "Dune", "Dune Messiah"]
    # Search with lowercase partial word "dune"
    monkeypatch.setattr("builtins.input", lambda _: "dune")

    search_books(library)

    captured = capsys.readouterr()
    assert "1. Dune" in captured.out
    assert "2. Dune Messiah" in captured.out
    assert "The Hobbit" not in captured.out


def test_search_books_not_found(monkeypatch, capsys):
    """Test search with no matching titles displays clear message."""
    library = ["The Hobbit", "1984"]
    monkeypatch.setattr("builtins.input", lambda _: "Foundation")

    search_books(library)

    captured = capsys.readouterr()
    assert "No books found matching 'foundation'." in captured.out


def test_search_books_empty_library(capsys):
    """Test searching an empty library alerts the user immediately."""
    library = []
    search_books(library)

    captured = capsys.readouterr()
    assert "Your library is empty." in captured.out