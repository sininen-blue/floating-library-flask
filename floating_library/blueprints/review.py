from flask import (
    Blueprint, flash, render_template, request
)
from ..db import get_db
from datetime import datetime
from floating_library.handlers.request_handler import RequestHandler

bp = Blueprint('review', __name__, url_prefix='/review')


@bp.route('/create', methods=['GET'])
def create_form():
    return render_template('review/create_form.html')


@bp.route('/create', methods=['POST'])
def create():
    error = None

    book_id = request.form.get('book_id')
    rating = request.form.get('rating')
    body = request.form.get('body')
    date_added = datetime.today().timestamp()
    date_updated = date_added

    if not book_id:
        error = "Book is required"
    if not rating:
        error = "Rating is required"
    if not body:
        error = "Review is required"

    if error is not None:
        flash(error)
    else:
        db = get_db()
        db.execute(
            'insert into review (book_id, rating, body, date_added, date_updated) '
            'values (?, ?, ?, ?, ?)',
            (book_id, rating, body, date_added, date_updated)
        )
        db.commit()


@bp.route('/<int:id>/update')
def update():
    r: RequestHandler = RequestHandler(request)
    error = None

    review_id: str = r.get('review_id')
    book_id: str = r.get('book_id')
    rating: str = r.get('rating')
    body: str = r.get('body')
    date_updated: datetime = datetime.today().timestamp()

    if error is not None:
        flash(error)
    else:
        db = get_db()
        db.execute(
            'update review '
            'set '
            'book_id = ?, '
            'rating = ?, '
            'body = ?, '
            'date_updated = ? '
            'where id = ?',
            (book_id, rating, body, date_updated, review_id)
        )
        db.commit()
