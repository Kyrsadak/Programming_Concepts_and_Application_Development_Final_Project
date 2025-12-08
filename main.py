from library import Library
from models import Book, Member

def input_int(prompt: str, allow_empty=False) -> int:
    while True:
        s = input(prompt).strip()
        if allow_empty and s == "":
            return None
        if not s.isdigit():
            print("Ошибка: введите положительное целое число.")
            continue
        return int(s)

def input_nonempty(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s == "":
            print("Ошибка: поле не должно быть пустым.")
            continue
        return s

def print_book(b: Book):
    status = "Доступна" if b.is_available else f"Выдана (member_id={b.borrower_id})"
    print(f"[{b.id}] {b.title} — {b.author}, {b.year} | {status}")

def menu():
    lib = Library()
    while True:
        print("\n=== Library System ===")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Список всех книг")
        print("5. Добавить члена (member)")
        print("6. Выдать книгу")
        print("7. Принять книгу")
        print("8. Сохранить в файл (force)")
        print("9. Загрузить из файла (reload)")
        print("0. Выход")
        choice = input("Выберите опцию: ").strip()
        try:
            if choice == "1":
                book_id = input_int("ID книги (число): ")
                title = input_nonempty("Название: ")
                author = input_nonempty("Автор: ")
                year = input_int("Год издания: ")
                b = Book(id=book_id, title=title, author=author, year=year)
                lib.add_book(b)
                print("Книга добавлена.")
            elif choice == "2":
                book_id = input_int("ID книги для удаления: ")
                lib.remove_book(book_id)
                print("Книга удалена.")
            elif choice == "3":
                q = input_nonempty("Введите часть названия/автора или ID: ")
                results = lib.find_books(q)
                if not results:
                    print("Ничего не найдено.")
                else:
                    for b in results:
                        print_book(b)
            elif choice == "4":
                books = lib.list_books()
                if not books:
                    print("База пуста.")
                else:
                    for b in books:
                        print_book(b)
            elif choice == "5":
                member_id = input_int("ID члена (число): ")
                name = input_nonempty("Имя: ")
                m = Member(member_id=member_id, name=name, borrowed_books=[])
                lib.add_member(m)
                print("Член добавлен.")
            elif choice == "6":
                book_id = input_int("ID книги для выдачи: ")
                member_id = input_int("ID члена: ")
                lib.borrow_book(book_id, member_id)
                print("Книга выдана.")
            elif choice == "7":
                book_id = input_int("ID книги для возврата: ")
                member_id = input_int("ID члена: ")
                lib.return_book(book_id, member_id)
                print("Книга принята обратно.")
            elif choice == "8":
                lib.save_to_file()
                print("Сохранено.")
            elif choice == "9":
                lib.load_from_file()
                print("Перезагружено из файла.")
            elif choice == "0":
                print("Выход. Пока.")
                break
            else:
                print("Неверный выбор.")
        except Exception as e:
            print("Ошибка:", e)

if __name__ == "__main__":
    menu()
