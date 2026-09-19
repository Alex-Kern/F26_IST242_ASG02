

def display_menu():
    """Displays the main menu options for the Personal Library Manager."""
    print("=== Personal Library Manager ===")
    print("1. View all books")
    print("2. Add a book")
    print("3. Remove a book")
    print("4. Search for a book")
    print("5. Exit")


def view_books(library):
    """Displays all books formatted as 'Title by Author (Year)' sorted alphabetically by title."""
    if not library:
        print("Your library is empty.")
        return

    # Layer 2: Sort books alphabetically by title (book[0])
    sorted_books = sorted(library, key=lambda book: book[0].lower())

    print("--- Books in Library ---")
    for index, (title, author, year) in enumerate(sorted_books, start=1):
        print(f"{index}. {title} by {author} ({year})")


def add_book(library, title_set):
    """Prompts for title, author, and year, stores book as a tuple, and prevents duplicates via a set."""
    title = input("Enter book title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return

    # Layer 2: Constant time O(1) duplicate check
    if title.lower() in title_set:
        print(f"'{title}' is already in your library.")
        return

    author = input("Enter author: ").strip()
    if not author:
        print("Author cannot be empty.")
        return

    year_str = input("Enter publication year: ").strip()
    if not year_str.isdigit():
        print("Year must be a valid integer.")
        return
    year = int(year_str)

    # Layer 2: Store record as immutable tuple
    book = (title, author, year)
    library.append(book)
    title_set.add(title.lower())

    print(f"'{title}' by {author} ({year}) has been added to your library.")


def remove_book(library, title_set):
    """Prompts for title and removes matching tuple from library list and title_set."""
    if not library:
        print("Your library is empty. Nothing to remove.")
        return

    title_to_remove = input("Enter the title of the book to remove: ").strip()

    # Find the matching tuple by title
    found_book = None
    for book in library:
        if book[0].lower() == title_to_remove.lower():
            found_book = book
            break

    if found_book:
        library.remove(found_book)
        title_set.remove(found_book[0].lower())
        print(f"'{found_book[0]}' has been removed from your library.")
    else:
        print(f"'{title_to_remove}' was not found in the library.")


def search_books(library):
    """Searches for books by partial, case-insensitive title match using a list comprehension."""
    if not library:
        print("Your library is empty.")
        return

    keyword = input("Enter search term: ").strip().lower()
    if not keyword:
        print("Search term cannot be empty.")
        return

    # Layer 2: Comprehension inspecting index 0 (title) of each tuple
    matches = [book for book in library if keyword in book[0].lower()]

    if matches:
        print("--- Matching Books ---")
        for index, (title, author, year) in enumerate(matches, start=1):
            print(f"{index}. {title} by {author} ({year})")
    else:
        print(f"No books found matching '{keyword}'.")


def main():
    """Orchestrates the interactive menu loop for Layer 2."""
    library = []
    title_set = set()

    while True:
        display_menu()
        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            view_books(library)
        elif choice == "2":
            add_book(library, title_set)
        elif choice == "3":
            remove_book(library, title_set)
        elif choice == "4":
            search_books(library)
        elif choice == "5":
            print("Exiting Personal Library Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a number between 1 and 5.")


if __name__ == "__main__":
    main()