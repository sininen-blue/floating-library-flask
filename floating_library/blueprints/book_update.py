from flask import (
    Blueprint, render_template,
)
from ..db import get_db

bp = Blueprint('update', __name__, url_prefix='/update')


@bp.route('/', methods=['GET'])
def index():
    db = get_db()

    updates = db.execute(
        'select u.id, book_id, added_chapters, date_added '
        'from book_update u '
        'join book b on u.book_id = b.id '
        'order by date_added desc'
    ).fetchall()

    return render_template('update/index.html', updates=updates)
