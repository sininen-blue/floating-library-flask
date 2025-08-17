from flask import (
    Blueprint, flash, render_template, request, redirect, url_for, abort
)
from floating_library.db import get_db

bp = Blueprint('book', __name__, url_prefix='/book')


@bp.route('/', methods=['GET'])
def index():
    db = get_db()
    books = db.execute().fetchall()  # TODO: specifics of fetchall and fetchone

    context = {
        "books": books
    }
    return render_template('book/index.html', context)


@bp.route('/create', methods=['GET'])
def create_form():
    return render_template('book/create_form.html')


@bp.route('/create', methods=['POST'])
def create():
    error = None

    url = request.form.get('book_url')
    if not url:
        error = "Url is required"

    # parse

    if error is not None:
        flash(error)
    else:
        db = get_db()
        db.execute()  # TODO: here
        db.commit()
        return redirect(url_for('book.index'))


@bp.route('/<int:id>/delete', methods=['DELETE'])
def delete(id):
    db = get_db()

    book = db.execute().fetchone()
    if book is None:
        abort(404, f"Bood with id: {id} does not exist")

    db.execute('delete from book where id = ?', (id,))
    db.commit()
    return redirect(url_for('book.index'))
