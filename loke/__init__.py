from .endpoints import auth
from .endpoints.strategy import strategy
from .endpoints.strategy import data_strategy
from .endpoints.strategy import indicators_strategy
from .endpoints.machine_learning import markov
from .endpoints.optimization import optimization
from .endpoints.optimization import conditions
from .controllers.StrategyController import StrategyController
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from loke.database import db
from flask import Flask, request, jsonify
from flask_caching import Cache
from flask import Flask
import pandas_ta as ta
import os
import mimetypes
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')
###


# General Info:
# Dataframe column name can be sensitive to change (_BUY / _SELL)
# DOES NOT HAVE URL PREFIX SO INDEX = / and CREATE = /CREATE
# app.add_url_rule() associates the endpoint name 'index' with the /
# url_for('index') or url_for('strategy.index') will both work,


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

    # load the instance config, if it exists, when not testing
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # file and blueprint must be called the same
    app.register_blueprint(auth.bp)
    app.register_blueprint(strategy.bp)
    app.register_blueprint(data_strategy.bp)
    app.register_blueprint(indicators_strategy.bp)
    app.register_blueprint(conditions.bp)
    app.register_blueprint(optimization.bp)
    app.register_blueprint(markov.bp)
    app.add_url_rule('/', endpoint='index')

    @app.route("/")
    def index():
        return render_template("loke/templates/index.html")

    db.init_app(app)

    return app
