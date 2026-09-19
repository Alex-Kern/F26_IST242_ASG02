# virtual environment
# multiple projects -> different versions of libraries
import pytest
from ASG02 import view_books, add_book, remove_book



def test_view_books_empty(capsys):
    """Test viewing an empty library shows the correct message."""
    library = []
    view_books(library)
    captured = capsys.readouterr()
    assert "Your library is empty." in captured.out


def test_view_books_sorted_and_formatted(capsys):
    """Test books are unpacked and displayed alphabetically by title."""
    library = [
        ("The Hobbit", "J.R.R. Tolkien", 1937),
        ("Dune", "Frank Herbert", 1965),
    ]
    view_books(library)
    captured = capsys.readouterr()

    # Dune should come first because of alphabetical sorting
    expected_dune = "1. Dune by Frank Herbert (1965)"
    expected_hobbit = "2. The Hobbit by J.R.R. Tolkien (1937)"

    assert expected_dune in captured.out
    assert expected_hobbit in captured.out
    assert captured.out.index(expected_dune) < captured.out.index(expected_hobbit)


def test_add_book_success(monkeypatch, capsys):
    """Test adding a valid book creates a tuple and registers with the set."""
    library = []
    title_set = set()

    # Provide all 3 inputs: Title, Author, Year
    inputs = iter(["Dune", "Frank Herbert", "1965"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    add_book(library, title_set)

    assert len(library) == 1
    assert library[0] == ("Dune", "Frank Herbert", 1965)
    assert "dune" in title_set

    captured = capsys.readouterr()
    assert (
        "'Dune' by Frank Herbert (1965) has been added to your library."
        in captured.out
    )


def test_add_book_duplicate_prevented(monkeypatch, capsys):
    """Test that duplicate titles are rejected via the set in O(1) time."""
    library = [("Dune", "Frank Herbert", 1965)]
    title_set = {"dune"}

    monkeypatch.setattr("builtins.input", lambda _: "dune")

    add_book(library, title_set)

    assert len(library) == 1
    assert len(title_set) == 1
    captured = capsys.readouterr()
    assert "'dune' is already in your library." in captured.out


def test_add_book_invalid_year(monkeypatch, capsys):
    """Test entering non-numeric year rejects book addition."""
    library = []
    title_set = set()

    inputs = iter(["1984", "George Orwell", "nineteen-eighty-four"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    add_book(library, title_set)

    assert len(library) == 0
    assert len(title_set) == 0
    captured = capsys.readouterr()
    assert "Year must be a valid integer." in captured.out


def test_remove_book_success(monkeypatch, capsys):
    """Test removing a book deletes its tuple and clears it from title_set."""
    library = [("Dune", "Frank Herbert", 1965)]
    title_set = {"dune"}

    monkeypatch.setattr("builtins.input", lambda _: "Dune")

    remove_book(library, title_set)

    assert len(library) == 0
    assert "dune" not in title_set

    captured = capsys.readouterr()
    assert "'Dune' has been removed from your library." in captured.out


def test_remove_book_not_found(monkeypatch, capsys):
    """Test attempting to remove a non-existent title leaves collections unchanged."""
    library = [("Dune", "Frank Herbert", 1965)]
    title_set = {"dune"}

    monkeypatch.setattr("builtins.input", lambda _: "Foundation")

    remove_book(library, title_set)

    assert len(library) == 1
    assert "dune" in title_set

    captured = capsys.readouterr()
    assert "'Foundation' was not found in the library." in captured.out


def test_remove_book_empty_library(capsys):
    """Test removing from an empty library alerts the user immediately without prompting."""
    library = []
    title_set = set()

    remove_book(library, title_set)

    captured = capsys.readouterr()
    assert "Your library is empty. Nothing to remove." in captured.out