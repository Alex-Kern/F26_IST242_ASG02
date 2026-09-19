# virtual environment
# multiple projects -> different versions of libraries
import pytest
from ASG02 import add_book


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