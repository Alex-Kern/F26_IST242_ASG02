# virtual environment
# multiple projects -> different versions of libraries
import pytest
from ASG02 import view_books


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
