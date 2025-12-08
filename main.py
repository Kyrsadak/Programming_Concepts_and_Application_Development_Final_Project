from library import Library
from models import Book, Member

def input_int(prompt: str, allow_empty=False) -> int:
    while True:
        s = input(prompt).strip()
        if allow_empty and s == "":
            return None
        if not s.isdigit():
            print("Error: please enter a positive integer.")
            continue
        return int(s)

def input_nonempty(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s == "":
            print("Error: field must not be empty.")
            continue
        return s

def print_book(b: Book):
    status = "Available" if b.is_available else f"Borrowed (member_id={b.borrower_id})"
    print(f"[{b.id}] {b.title} — {b.author}, {b.year} | {status}")

def menu():
    lib = Library()
    while True:
        print("\n=== Library System ===")
        print("1. Add book")
        print("2. Remove book")
        print("3. Find book")
        print("4. List all books")
        print("5. Add member")
        print("6. Borrow book")
        print("7. Return book")
        print("8. Save to file (force)")
        print("9. Load from file (reload)")
        print("0. Exit")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                book_id = input_int("Book ID (number): ")
                title = input_nonempty("Title: ")
                author = input_nonempty("Author: ")
                year = input_int("Year of publication: ")
                b = Book(id=book_id, title=title, author=author, year=year)
                lib.add_book(b)
                print("Book added.")
            elif choice == "2":
                book_id = input_int("Book ID to remove: ")
                lib.remove_book(book_id)
                print("Book removed.")
            elif choice == "3":
                q = input_nonempty("Enter part of title/author or ID: ")
                results = lib.find_books(q)
                if not results:
                    print("No results found.")
                else:
                    for b in results:
                        print_book(b)
            elif choice == "4":
                books = lib.list_books()
                if not books:
                    print("Database is empty.")
                else:
                    for b in books:
                        print_book(b)
            elif choice == "5":
                member_id = input_int("Member ID (number): ")
                name = input_nonempty("Name: ")
                m = Member(member_id=member_id, name=name, borrowed_books=[])
                lib.add_member(m)
                print("Member added.")
            elif choice == "6":
                book_id = input_int("Book ID to borrow: ")
                member_id = input_int("Member ID: ")
                lib.borrow_book(book_id, member_id)
                print("Book borrowed.")
            elif choice == "7":
                book_id = input_int("Book ID to return: ")
                member_id = input_int("Member ID: ")
                lib.return_book(book_id, member_id)
                print("Book returned.")
            elif choice == "8":
                lib.save_to_file()
                print("Saved.")
            elif choice == "9":
                lib.load_from_file()
                print("Reloaded from file.")
            elif choice == "0":
                print("Exit. Bye.")
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    menu()
