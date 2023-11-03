import os

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


def create_app(test_config=None):
    # The app needs to know where it’s located to set up some paths,
    # and __name__ is a convenient way to tell it that.
    # instance_relative_config=True tells the app that configuration files are
    # relative to the instance folder(the current flask package).

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        # should be overridden with a random value when deploying.
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        CACHE_TYPE="SimpleCache",
        CACHE_DEFAULT_TIMEOUT=300

    )
    cache = Cache(app)

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

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/init_strategy', methods=['POST'])
    def init_strategy():
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
            {"kind": "ema", "length": 8},
            {"kind": "ema", "length": 21},
            {"kind": "bbands", "length": 20},
            {"kind": "macd", "fast": 8, "slow": 21}
        ])
        df = s.create_strategy()
        columns = s.column_dict()
        df_bytes = pickle.dumps(df)
        cache.set('df_cache_key', df_bytes)
        resp = {"message": f'{columns}'}
        return resp

    @app.route('/load_conditions', methods=['POST'])
    def strategy():
        data = request.get_json()
        selected_conds_buy = data['conds_buy']
        selected_conds_sell = data['conds_sell']
        df_bytes = cache.get('df_cache_key')
        df = pickle.loads(df_bytes)
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
    return app
