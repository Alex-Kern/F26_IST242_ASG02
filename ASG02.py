import json
import os

class LibraryManager:
    """Manages the book collection and business logic."""

    def __init__(self, filename="library_data.json"):
        self.filename = filename
        self.books = {}
        self.load_library()

    def add_or_update_book(self, title: str, author: str, year: int) -> str:
        """Adds or updates a book entry. Returns 'added' or 'updated'."""
        status = "updated" if title in self.books else "added"
        self.books[title] = {"author": author, "year": int(year)}
        return status

    def remove_book(self, title: str) -> bool:
        """Removes a book by title (case-insensitive). Returns True if removed, False otherwise."""
        target_key = None
        for key in self.books:
            if key.lower() == title.lower():
                target_key = key
                break

        if target_key:
            del self.books[target_key]
            return True
        return False

    def get_all_books(self):
        """Returns all books as (title, author, year) tuples sorted alphabetically by title."""
        sorted_keys = sorted(self.books.keys(), key=lambda t: t.lower())
        return [
            (title, self.books[title]["author"], self.books[title]["year"])
            for title in sorted_keys
        ]

    def search_books(self, keyword: str):
        """Returns matching books as (title, author, year) tuples by partial title match."""
        keyword = keyword.lower()
        matches = [
            (title, info["author"], info["year"])
            for title, info in self.books.items()
            if keyword in title.lower()
        ]
        return sorted(matches, key=lambda item: item[0].lower())

    def get_author_statistics(self):
        """Calculates book count per author, sorted alphabetically."""
        counts = {}
        for info in self.books.values():
            author = info["author"]
            counts[author] = counts.get(author, 0) + 1
        return sorted(counts.items())

    def load_library(self):
        """Loads data from JSON file into self.books."""
        if not os.path.exists(self.filename):
            self.books = {}
            return

        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                self.books = json.load(f)
        except (json.JSONDecodeError, OSError):
            print(f"Warning: Could not read '{self.filename}'. Starting with an empty library.")
            self.books = {}

    def save_library(self):
        """Saves current collection to JSON file."""
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(self.books, f, indent=4)
            print(f"Library successfully saved to '{self.filename}'.")
        except OSError as e:
            print(f"Error: Failed to save library data: {e}")


def render_book_list(books):
    """Displays a list of (title, author, year) tuples with 1-based indexing."""
    for index, (title, author, year) in enumerate(books, start=1):
        print(f"{index}. {title} by {author} ({year})")


# --- CLI Presentation Layer ---

def display_menu():
    """Displays the main menu options for the Personal Library Manager."""
    print("=== Personal Library Manager ===")
    print("1. View all books")
    print("2. Add or update a book")
    print("3. Remove a book")
    print("4. Search for a book")
    print("5. Show author statistics")
    print("6. Save and exit")


def main():
    manager = LibraryManager("library_data.json")

    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            books = manager.get_all_books()
            if not books:
                print("Your library is empty.")
            else:
                print("--- Books in Library ---")
                render_book_list(books)

        elif choice == "2":
            title = input("Title: ").strip()
            if not title:
                print("Title cannot be empty.")
                continue

            author = input("Author: ").strip()
            if not author:
                print("Author cannot be empty.")
                continue

            year_str = input("Year: ").strip()
            if not year_str.isdigit():
                print("Year must be a valid integer.")
                continue

            action = manager.add_or_update_book(title, author, int(year_str))
            print(f'"{title}" was {action}.')

        elif choice == "3":
            if not manager.books:
                print("Your library is empty. Nothing to remove.")
                continue

            title = input("Enter the title of the book to remove: ").strip()
            if manager.remove_book(title):
                print(f"'{title}' has been removed from your library.")
            else:
                print(f"'{title}' was not found in the library.")

        elif choice == "4":
            if not manager.books:
                print("Your library is empty.")
                continue

            keyword = input("Enter search term: ").strip()
            if not keyword:
                print("Search term cannot be empty.")
                continue

            matches = manager.search_books(keyword)
            if matches:
                print("--- Matching Books ---")
                render_book_list(matches)
            else:
                print(f"No books found matching '{keyword}'.")

            keyword = input("Enter search term: ").strip()
            if not keyword:
                print("Search term cannot be empty.")
                continue

            matches = manager.search_books(keyword)
            if matches:
                print("--- Matching Books ---")
                for index, (title, info) in enumerate(matches, start=1):
                    print(f"{index}. {title} by {info['author']} ({info['year']})")
            else:
                print(f"No books found matching '{keyword}'.")

        elif choice == "5":
            stats = manager.get_author_statistics()
            if not stats:
                print("Your library is empty.")
            else:
                print("--- Author Statistics ---")
                for author, count in stats:
                    unit = "book" if count == 1 else "books"
                    print(f"{author}: {count} {unit}")

        elif choice == "6":
            manager.save_library()
            print("Exiting Personal Library Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a number between 1 and 6.")


if __name__ == "__main__":
    main()