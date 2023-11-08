import os
import pandas_ta as ta
from flask import Flask
from flask_caching import Cache

from flask import Flask, request, jsonify
from flask_caching import Cache
import pandas as pd
import pickle
from loke.trading_engine.Strategy import Strategy
from loke.trading_engine.Condition import Condition
from loke.trading_engine.Backtest import Backtest
from loke.trading_engine.load_conditions import load_conditions
from loke.trading_engine.call_optimizer import call_optimizer
from loke.database import db
from loke.blueprints.test import test
from loke.trading_engine.indicators.momentum.Rsi import Rsi
from loke.trading_engine.indicators.momentum.Ao import Ao
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from . import auth
from . import blog
from . import cache_import
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

    # index points to blog index as it no prefix is defined for the blueprint
    app.add_url_rule('/', endpoint='index')

    @app.route("/")
    def index():
        return render_template("loke/templates/index.html")

    @app.route('/init_strategy', methods=['POST', 'GET'])
    def init_strategy():
        if request.method == "POST":
            data = request.get_json()
            strategy_id = data['strategy_id']
            exchange = data['exchange']
            init_candles = ['init_candles']
            symbol = data['symbol']
            name = data['name']
            description = data['description']

            rsi = Rsi()
            rsi.set(20, 50, 0)
            ao = Ao()
            ao.set(15, 15, 0)

            print(f"{rsi.type_dict()}")

            s = Strategy(exchange, init_candles, symbol, name, description)
            s.addIndicators([
                # {"kind": "rsi", "length": 15, "scalar": 40},
                rsi.get(),
                ao.get(),
                {"kind": "ema", "length": 8},
                {"kind": "ema", "length": 21},
                {"kind": "bbands", "length": 20},
                {"kind": "macd", "fast": 8, "slow": 21}
            ])
            df = s.create_strategy()
            df = df.head(215)
            df.to_json("lol.json", orient='records', compression='infer')
            print(df.columns)
            columns = s.column_dict()
            df_bytes = pickle.dumps(df)
            cache.set('df_cache_key', df_bytes)
            resp = {"message": f'{df}'}
            return resp

    @app.route('/load_conditions', methods=['POST'])
    def strategy():
        data = request.get_json()
        selected_conds_buy = data['conds_buy']
        selected_conds_sell = data['conds_sell']
        df = pd.read_pickle("df.pkl")
        # df_bytes = cache.get('df_cache_key')
        # df = pickle.loads(df_bytes)

        df = load_conditions(df, selected_conds_buy, selected_conds_sell)
        df_bytes = pickle.dumps(df)
        cache.set('df_cache_key', df_bytes)
        json_string = {"message": 'something'}
        # print(df.head(3))
        return json_string

    @app.route('/backtest', methods=['GET'])
    def backtest():
        df_bytes = cache.get('df_cache_key')
        df = pickle.loads(df_bytes)
        print("BACK HIT")
        bt = Backtest()
        result = bt.run(df)
        json_string = {"message": f'{result}'}
        return json_string

    @app.route('/optimize', methods=['POST'])
    def optimize():
        data = request.get_json()
        # data = request.data
        exchange = data['exchange']
        init_candles = ['init_candles']
        symbol = data['symbol']
        name = data['name']
        description = data['description']
        s = Strategy(exchange, init_candles, symbol, name, description)
        s.addIndicators([
            {"kind": "rsi", "length": 15},
        ])

        df = s.create_strategy()
        call_optimizer(df, "dynamic", 10, 10)

        columns = s.column_dict()
        resp = {"message": f'{columns}'}
        return resp

    db.init_app(app)

    return app
