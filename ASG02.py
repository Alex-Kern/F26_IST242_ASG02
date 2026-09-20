import json
import os

def display_menu():
    """Displays the main menu options for the Personal Library Manager."""
    print("=== Personal Library Manager ===")
    print("1. View all books")
    print("2. Add or update a book")
    print("3. Remove a book")
    print("4. Search for a book")
    print("5. Show author statistics")
    print("6. Save and exit")


def view_books(library):
    """Displays all books formatted as 'Title by Author (Year)' sorted alphabetically by title."""
    if not library:
        print("Your library is empty.")
        return

    sorted_books = sorted(library.items(), key=lambda item: item[0].lower())

    print("--- Books in Library ---")
    for index, (title, info) in enumerate(sorted_books, start=1):
        print(f"{index}. {title} by {info['author']} ({info['year']})")

def add_or_update_book(library):
    """Prompts for book details and adds or updates the entry in the dictionary."""
    title = input("Title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return

    author = input("Author: ").strip()
    if not author:
        print("Author cannot be empty.")
        return

    year_str = input("Year: ").strip()
    if not year_str.isdigit():
        print("Year must be a valid integer.")
        return
    year = int(year_str)

    # Check existence BEFORE assigning so we know if it was added or updated
    status = "updated" if title in library else "added"

    # Store in nested dictionary
    library[title] = {"author": author, "year": year}

    print(f'"{title}" was {status}.')

def remove_book(library):
    """Prompts for title and removes the book from the dictionary."""
    if not library:
        print("Your library is empty. Nothing to remove.")
        return

    title_to_remove = input("Enter the title of the book to remove: ").strip()

    # Find the matching key in the dictionary (case-insensitive)
    target_key = None
    for title in library:
        if title.lower() == title_to_remove.lower():
            target_key = title
            break

    if target_key:
        del library[target_key]
        print(f"'{target_key}' has been removed from your library.")
    else:
        print(f"'{title_to_remove}' was not found in the library.")


def search_books(library):
    """Searches for books by partial, case-insensitive title match."""
    if not library:
        print("Your library is empty.")
        return

    keyword = input("Enter search term: ").strip().lower()
    if not keyword:
        print("Search term cannot be empty.")
        return

    matches = [
        (title, info)
        for title, info in library.items()
        if keyword in title.lower()
    ]

    if matches:
        print("--- Matching Books ---")
        for index, (title, info) in enumerate(matches, start=1):
            print(f"{index}. {title} by {info['author']} ({info['year']})")
    else:
        print(f"No books found matching '{keyword}'.")


def show_author_statistics(library):
    """Displays the count of books written by each author, sorted alphabetically."""
    if not library:
        print("Your library is empty.")
        return

    # Count books per author
    author_counts = {}
    for info in library.values():
        author = info["author"]
        author_counts[author] = author_counts.get(author, 0) + 1

    print("--- Author Statistics ---")
    for author, count in sorted(author_counts.items()):
        unit = "book" if count == 1 else "books"
        print(f"{author}: {count} {unit}")


def load_library(filename="library_data.json"):
    """Loads library data from a JSON file.
    Returns an empty dict if the file is missing or corrupted.
    """
    if not os.path.exists(filename):
        return {}

    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        print(f"Warning: Could not read '{filename}'. Starting with an empty library.")
        return {}


def save_library(library, filename="library_data.json"):
    """Saves library dictionary to a JSON file."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(library, f, indent=4)
        print(f"Library successfully saved to '{filename}'.")
    except OSError as e:
        print(f"Error: Failed to save library data: {e}")


def main():
    """Orchestrates the interactive menu loop for Layer 3."""
    filename = "library_data.json"
    library = load_library(filename)

    while True:
        display_menu()
        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "1":
            view_books(library)
        elif choice == "2":
            add_or_update_book(library)
        elif choice == "3":
            remove_book(library)
        elif choice == "4":
            search_books(library)
        elif choice == "5":
            show_author_statistics(library)
        elif choice == "6":
            save_library(library, filename)
            print("Exiting Personal Library Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a number between 1 and 6.")

if __name__ == "__main__":
    main()