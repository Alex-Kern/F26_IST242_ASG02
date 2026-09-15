def display_menu():
    """"Displays the main menu options for the Personal Library Manager."""
    print("=== Personal Library Manager ===")
    print("1. View all books")
    print("2. Add a book")
    print("3. Remove a book")
    print("4. Search for a book")
    print("5. Exit")


def view_books(library):
    """Displays all book titles in the library with 1-based indexing."""
    if not library:
        print("Your library is empty.")
        return

    print("--- Books in Library ---")
    for index, title in enumerate(library, start=1):
        print(f"{index}. {title}")

if __name__ == "__main__":
    display_menu()
    sample_library = ["The Hobbit", "1984", "To Kill a Mockingbird"]
    view_books(sample_library)
    view_books([])
