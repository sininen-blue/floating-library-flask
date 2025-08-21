from flask import (
    Blueprint, flash, render_template, request, redirect, url_for, abort
)
from floating_library.parsers import parse
from floating_library.db import get_db
from floating_library.handlers.request_handler import RequestHandler
from floating_library.models.book import Book, BookHandler
from datetime import datetime

bp = Blueprint('book', __name__, url_prefix='/book')
bh: BookHandler = BookHandler()


@bp.route('/', methods=['GET'])
def index():
    books: list[Book] = bh.get_all()

    return render_template('book/index.html', books=books)


@bp.route('/search', methods=['GET'])
def show():
    query = request.args.get("q")
    books: list[Book] = bh.search(query)
    return render_template('book/index.html', books=books)


@bp.route('/create', methods=['GET'])
def create_form():
    return render_template('book/create.html')


@bp.route('/create', methods=['POST'])
def create():
    r: RequestHandler = RequestHandler(request)
    error: str = None

    url: str = r.get('book_url')

    if error is not None:
        flash(error)
    else:
        results: dict[str, str | list[str]] = parse(url)
        book: Book = bh.make(results)
        bh.save(book)

        return redirect(url_for('book.index'))


@bp.route('/<int:id>/update', methods=['PUT'])
def update(id):
    db = get_db()
    error: str = None

    book: Book = bh.get(id)

    if error is not None:
        flash(error)
    else:
        results: dict[str, str | list[str]] = parse(book.url)
        updatedBook: Book = bh.make(results)

        if updatedBook.chapter_count > book.chapter_count:
            bh.update(id, updatedBook)

            diff: int = updatedBook.chapter_count - book.chapter_count
            db.execute(
                'insert into book_update '
                '(book_id, added_chapters, date_added) '
                'values (?, ?, ?)',
                (book["id"], diff, datetime.today().timestamp())
            )
            db.commit()

    return index()


@bp.route('/<int:id>/delete', methods=['DELETE'])
def delete(id):
    bh.delete(id)
    return redirect(url_for('book.index'))
