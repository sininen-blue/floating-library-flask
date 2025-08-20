from flask import (
    Blueprint, flash, render_template, request, redirect, url_for, abort
)
from floating_library.parsers import parse
from floating_library.db import get_db
from floating_library.handlers.request_handler import RequestHandler
from datetime import datetime

bp = Blueprint('book', __name__, url_prefix='/book')


@bp.route('/', methods=['GET'])
def index():
    db = get_db()
    books = db.execute(
        'select * '
        'from book '
        'order by date_updated desc '
    ).fetchall()

    return render_template('book/index.html', books=books)

# show route


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

        title = results.get('title')
        author = results.get('author')
        chapter_count = results.get('chapter_count')
        date_added = datetime.today().timestamp()
        date_updated = date_added
        db = get_db()
        db.execute(
            'insert into book (url, title, author, chapter_count, date_added, date_updated) '
            'values (?, ?, ?, ?, ?, ?) ',
            (url, title, author, chapter_count, date_added, date_updated)
        )
        db.commit()
        return redirect(url_for('book.index'))


@bp.route('/<int:id>/delete', methods=['DELETE'])
def delete(id):
    db = get_db()

    book = db.execute().fetchone()
    if book is None:
        abort(404, f"Bood with id: {id} does not exist")

    db.execute(
        'delete from book where id = ?',
        (id,)
    )
    db.commit()
    return redirect(url_for('book.index'))
