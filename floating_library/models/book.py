from flask import abort
from typing import Any, Callable
from datetime import datetime
from floating_library.db import get_db


class Book:
    def __init__(self) -> None:
        self.id: int | None = None
        self.url: str
        self.title: str
        self.author: str
        self.chapter_count: int
        self.date_added: datetime
        self.date_updated: datetime

    def _set_attr(self, name: str, value: Any, cast: Callable) -> None:
        try:
            setattr(self, name, cast(value))
        except ValueError:
            raise ValueError(f"Invalid {name} value: {value!r}")

    def set_id(self, id) -> None:
        if id is not None:
            self._set_attr("id", id, int)

    def set_url(self, url) -> None:
        self._set_attr("url", url, str)

    def set_title(self, title) -> None:
        self._set_attr("title", title, str)

    def set_author(self, author) -> None:
        self._set_attr("author", author, str)

    def set_chapter_count(self, chapter_count) -> None:
        self._set_attr("chapter_count", chapter_count, int)

    def set_date_added(self, date_added) -> None:
        self._set_attr("date_added", date_added, datetime.fromtimestamp)

    def set_date_updated(self, date_updated) -> None:
        self._set_attr("date_updated", date_updated, datetime.fromtimestamp)


class BookHandler:
    def make(self, items: dict) -> Book:
        book: Book = Book()
        book.set_id(items.get("id"))
        book.set_url(items.get("url"))
        book.set_title(items.get("title"))
        book.set_author(items.get("author"))
        book.set_chapter_count(items.get("chapter_count"))
        book.set_date_added(items.get("date_added"))
        book.set_date_added(items.get("date_added"))

        return book

    def get_all(self) -> list[Book]:
        db = get_db()
        books = db.execute(
            'select * '
            'from book '
            'order by date_updated desc '
        ).fetchall()

        results: list[Book] = []
        for book in books:
            newBook: Book = self.make(dict(book))
            results.append(newBook)

        return results

    def get(self, id: int) -> Book:
        db = get_db()
        bookRow: int = db.execute(
            'select * from book where id = ?', (id,)
        ).fetchone()

        if bookRow is None:
            abort(404, f"Book with id: {id} does not exist")

        book: Book = self.make(dict(bookRow))

        return book

    def save(self, book: Book) -> None:
        db = get_db()
        db.execute(
            'insert into book '
            '(url, title, author, chapter_count, date_added, date_updated) '
            'values (?, ?, ?, ?, ?, ?) ',
            (book.url, book.title, book.author,
             book.chapter_count, book.date_added, book.date_updated)
        )
        db.commit()

    def update(self, id: int, book: Book) -> None:
        book: Book = self.get(id)
        if book is None:
            abort(404, f"Book with id: {id} does not exist")

        db = get_db()
        db.execute(
            'update book '
            'set chapter_count = ?, '
            'date_updated = ? '
            'where id = ?'
            (book.chapter_count, book.date_updated.timestamp(), id)
        )
        db.commit()

    def delete(self, id) -> None:
        book: Book = self.get(id)
        if book is None:
            abort(404, f"Book with id: {id} does not exist")

        db = get_db()
        db.execute(
            'delete from book where id = ?',
            (id,)
        )
        db.commit()
