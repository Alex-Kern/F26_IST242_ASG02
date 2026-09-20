# virtual environment
# multiple projects -> different versions of libraries
import pytest
from ASG02 import LibraryManager


def test_add_book_new(tmp_path):
    """Test adding a brand new book returns 'added' and stores correct attributes."""
    manager = LibraryManager(filename=str(tmp_path / "test.json"))
    status = manager.add_or_update_book("Dune", "Frank Herbert", 1965)

    assert status == "added"
    assert "Dune" in manager.books
    assert manager.books["Dune"] == {"author": "Frank Herbert", "year": 1965}


def test_add_book_update_existing(tmp_path):
    """Test re-adding an existing title updates attributes and returns 'updated'."""
    manager = LibraryManager(filename=str(tmp_path / "test.json"))
    manager.add_or_update_book("Dune", "Frank Herbert", 1965)
    status = manager.add_or_update_book("Dune", "F. Herbert", 1966)

    assert status == "updated"
    assert len(manager.books) == 1
    assert manager.books["Dune"] == {"author": "F. Herbert", "year": 1966}


def test_remove_book_success(tmp_path):
    """Test removing an existing book returns True and deletes entry."""
    manager = LibraryManager(filename=str(tmp_path / "test.json"))
    manager.add_or_update_book("Dune", "Frank Herbert", 1965)

    assert manager.remove_book("Dune") is True
    assert "Dune" not in manager.books


def test_remove_book_case_insensitive(tmp_path):
    """Test removing a book with mismatched casing still deletes entry."""
    manager = LibraryManager(filename=str(tmp_path / "test.json"))
    manager.add_or_update_book("Dune Messiah", "Frank Herbert", 1969)

    assert manager.remove_book("dune messiah") is True
    assert "Dune Messiah" not in manager.books


def test_remove_book_not_found(tmp_path):
    """Test attempting to remove a missing title returns False without modifying data."""
    manager = LibraryManager(filename=str(tmp_path / "test.json"))
    manager.add_or_update_book("Dune", "Frank Herbert", 1965)

    assert manager.remove_book("Foundation") is False
    assert len(manager.books) == 1


def test_get_all_books_empty(tmp_path):
    """Test get_all_books returns an empty list when library has no entries."""
    manager = LibraryManager(filename=str(tmp_path / "test.json"))
    assert manager.get_all_books() == []


def test_get_all_books_sorted_tuples(tmp_path):
    """Test get_all_books returns alphabetical (title, author, year) tuples."""
    manager = LibraryManager(filename=str(tmp_path / "test.json"))
    manager.add_or_update_book("The Hobbit", "J.R.R. Tolkien", 1937)
    manager.add_or_update_book("Dune", "Frank Herbert", 1965)
    manager.add_or_update_book("Dune Messiah", "Frank Herbert", 1969)

    books = manager.get_all_books()
    expected = [
        ("Dune", "Frank Herbert", 1965),
        ("Dune Messiah", "Frank Herbert", 1969),
        ("The Hobbit", "J.R.R. Tolkien", 1937),
    ]
    assert books == expected


def test_search_books_partial_match(tmp_path):
    """Test search_books performs case-insensitive substring matching."""
    manager = LibraryManager(filename=str(tmp_path / "test.json"))
    manager.add_or_update_book("Dune", "Frank Herbert", 1965)
    manager.add_or_update_book("Dune Messiah", "Frank Herbert", 1969)
    manager.add_or_update_book("The Hobbit", "J.R.R. Tolkien", 1937)

    matches = manager.search_books("dune")
    expected = [
        ("Dune", "Frank Herbert", 1965),
        ("Dune Messiah", "Frank Herbert", 1969),
    ]
    assert matches == expected


def test_search_books_no_match(tmp_path):
    """Test search_books returns empty list when no matches exist."""
    manager = LibraryManager(filename=str(tmp_path / "test.json"))
    manager.add_or_update_book("Dune", "Frank Herbert", 1965)
    assert manager.search_books("xyz") == []


def test_get_author_statistics_empty(tmp_path):
    """Test author statistics on empty library returns empty list."""
    manager = LibraryManager(filename=str(tmp_path / "test.json"))
    assert manager.get_author_statistics() == []


def test_get_author_statistics_dynamic_count(tmp_path):
    """Test author statistics returns correct counts sorted by author name."""
    manager = LibraryManager(filename=str(tmp_path / "test.json"))
    manager.add_or_update_book("Dune", "Frank Herbert", 1965)
    manager.add_or_update_book("Dune Messiah", "Frank Herbert", 1969)
    manager.add_or_update_book("The Hobbit", "J.R.R. Tolkien", 1937)

    stats = manager.get_author_statistics()
    expected = [
        ("Frank Herbert", 2),
        ("J.R.R. Tolkien", 1),
    ]
    assert stats == expected


def test_load_nonexistent_file(tmp_path):
    """Test initializing manager with missing file starts with empty dict without crashing."""
    fake_path = tmp_path / "missing.json"
    manager = LibraryManager(filename=str(fake_path))
    assert manager.books == {}


def test_load_corrupted_json(tmp_path):
    """Test initializing with malformed JSON degrades gracefully to empty library."""
    bad_file = tmp_path / "corrupt.json"
    bad_file.write_text("{invalid_json: true", encoding="utf-8")

    manager = LibraryManager(filename=str(bad_file))
    assert manager.books == {}


def test_load_non_dictionary_json(tmp_path):
    """Test loading valid JSON that is a list instead of a dict falls back to empty dict."""
    list_file = tmp_path / "list_data.json"
    list_file.write_text('["Dune", "Frank Herbert", 1965]', encoding="utf-8")

    manager = LibraryManager(filename=str(list_file))
    assert manager.books == {}


def test_save_and_reload_persistence(tmp_path):
    """Test round-trip save and reload preserves book attributes."""
    file_path = str(tmp_path / "shelf.json")
    manager = LibraryManager(filename=file_path)
    manager.add_or_update_book("1984", "George Orwell", 1949)
    manager.save_library()

    new_manager = LibraryManager(filename=file_path)
    assert "1984" in new_manager.books
    assert new_manager.books["1984"]["year"] == 1949