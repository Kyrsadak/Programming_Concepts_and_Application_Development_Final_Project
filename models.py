from dataclasses import dataclass, asdict
from typing import List

@dataclass
class Book:
    id: int
    title: str
    author: str
    year: int
    is_available: bool = True
    borrower_id: int | None = None

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> "Book":
        return Book(
            id=int(d["id"]),
            title=str(d["title"]),
            author=str(d["author"]),
            year=int(d["year"]),
            is_available=bool(d.get("is_available", True)),
            borrower_id=d.get("borrower_id")
        )

@dataclass
class Member:
    member_id: int
    name: str
    borrowed_books: List[int]

    def to_dict(self) -> dict:
        return {
            "member_id": self.member_id,
            "name": self.name,
            "borrowed_books": self.borrowed_books[:]
        }

    @staticmethod
    def from_dict(d: dict) -> "Member":
        return Member(
            member_id=int(d["member_id"]),
            name=str(d["name"]),
            borrowed_books=list(d.get("borrowed_books", []))
        )
