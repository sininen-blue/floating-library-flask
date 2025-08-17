import os
from flask import Flask
from . import db
from .blueprints import book, book_update, review


def create_app(test_config: dict = None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'floating-library.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return "You aren't supposed to be here"

    db.init_app(app)

    app.register_blueprint(book.bp)
    app.register_blueprint(book_update.bp)
    app.register_blueprint(review.bp)

    return app
