import json
from typing import List, Optional
from models import Book, Member
import os

DATA_FILE = "database.json"

class Library:
    def __init__(self):
        self.books: List[Book] = []
        self.members: List[Member] = []
        self.load_from_file()

    # ---------- Book management ----------
    def add_book(self, book: Book) -> None:
        if self.find_book_by_id(book.id):
            raise ValueError(f"Book with id={book.id} already exists.")
        self.books.append(book)
        self.save_to_file()

    def remove_book(self, book_id: int) -> None:
        book = self.find_book_by_id(book_id)
        if not book:
            raise ValueError("Book not found.")
        if not book.is_available:
            raise ValueError("Cannot remove a book that is currently borrowed.")
        self.books = [b for b in self.books if b.id != book_id]
        self.save_to_file()

    def find_book_by_id(self, book_id: int) -> Optional[Book]:
        for b in self.books:
            if b.id == book_id:
                return b
        return None

    def find_books(self, query: str) -> List[Book]:
        q = query.lower().strip()
        results = []
        for b in self.books:
            if q in b.title.lower() or q in b.author.lower() or q == str(b.id):
                results.append(b)
        return results

    def list_books(self) -> List[Book]:
        return self.books[:]

    # ---------- Member management ----------
    def add_member(self, member: Member) -> None:
        if self.find_member_by_id(member.member_id):
            raise ValueError(f"User with id={member.member_id} already exists.")
        self.members.append(member)
        self.save_to_file()

    def find_member_by_id(self, member_id: int) -> Optional[Member]:
        for m in self.members:
            if m.member_id == member_id:
                return m
        return None

    # ---------- Borrow / Return ----------
    def borrow_book(self, book_id: int, member_id: int) -> None:
        book = self.find_book_by_id(book_id)
        if not book:
            raise ValueError("Book not found.")
        if not book.is_available:
            raise ValueError("Book is already borrowed.")
        member = self.find_member_by_id(member_id)
        if not member:
            raise ValueError("Library member not found.")
        # simple logic: no limits on the number of books
        book.is_available = False
        book.borrower_id = member_id
        member.borrowed_books.append(book_id)
        self.save_to_file()

    def return_book(self, book_id: int, member_id: int) -> None:
        book = self.find_book_by_id(book_id)
        if not book:
            raise ValueError("Book not found.")
        if book.is_available:
            raise ValueError("Book is not borrowed.")
        if book.borrower_id != member_id:
            raise ValueError("This book is not borrowed by the specified member.")
        member = self.find_member_by_id(member_id)
        if not member:
            raise ValueError("Library member not found.")
        # return
        book.is_available = True
        book.borrower_id = None
        if book_id in member.borrowed_books:
            member.borrowed_books.remove(book_id)
        self.save_to_file()

    # ---------- Persistence ----------
    def save_to_file(self) -> None:
        data = {
            "books": [b.to_dict() for b in self.books],
            "members": [m.to_dict() for m in self.members]
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_from_file(self) -> None:
        if not os.path.exists(DATA_FILE):
            # создать пустой файл
            self.books = []
            self.members = []
            self.save_to_file()
            return
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.books = [Book.from_dict(d) for d in data.get("books", [])]
            self.members = [Member.from_dict(d) for d in data.get("members", [])]
        except (json.JSONDecodeError, IOError):
            # on error — start with an empty database (and create a valid file)
            self.books = []
            self.members = []
            self.save_to_file()
