from flask import (
    Blueprint, flash, render_template, request
)
from ..db import get_db
from datetime import datetime

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
