
from flask import Flask, request, jsonify
from flask_caching import Cache
import pandas as pd
import pickle
from trading_engine.Strategy import Strategy
from trading_engine.Condition import Condition
from trading_engine.Backtest import Backtest
from trading_engine.load_conditions import load_conditions
from trading_engine.call_optimizer import call_optimizer
config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app = Flask(__name__)
# tell Flask to use the above defined config
app.config.from_mapping(config)
cache = Cache(app)


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
    condition_buy = [
        ["name1112221", {"ind": "RSI_15"}, {"cond": "<"}, {"val": 47}]],
    condition_sell = [
        ["nam22221322", {"ind": "RSI_15"}, {"cond": ">"}, {"val": 51}]]

    df = s.create_strategy()
    call_optimizer(df, "dynamic", 10, 10)

    columns = s.column_dict()
    resp = {"message": f'{columns}'}
    return resp


if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False)
