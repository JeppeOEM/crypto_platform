import os
import pandas_ta as ta
from flask import Flask
from flask_caching import Cache

from flask import Flask, request, jsonify
from flask_caching import Cache

from loke.database import db

from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from . import auth
from . import blog
from . import ml

from flask_caching import Cache

cache = Cache()


def register_extensions(app):
    cache.init_app(app)


def create_app(test_config=None):
    # The app needs to know where it’s located to set up some paths,
    # and __name__ is a convenient way to tell it that.
    # instance_relative_config=True tells the app that configuration files are
    # relative to the instance folder(the current flask package).

    app = Flask(__name__, instance_relative_config=True)
    register_extensions(app)
    app.config.from_mapping(
        # should be overridden with a random value when deploying.
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        CACHE_TYPE="SimpleCache",
        CACHE_DEFAULT_TIMEOUT=300

    )
    # cache = Cache(app)

# tell Flask to use the above defined config

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(ml.bp)
    # index points to blog index as it no prefix is defined for the blueprint
    app.add_url_rule('/', endpoint='index')

    @app.route("/")
    def index():
        return render_template("loke/templates/index.html")

    db.init_app(app)

    return app
