
from flask import Flask, request, jsonify
from flask_caching import Cache
import pandas as pd
import pickle
from trading_engine.Strategy import Strategy
from trading_engine.Condition import Condition
from trading_engine.Backtest import Backtest
config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app = Flask(__name__)
# tell Flask to use the above defined config
app.config.from_mapping(config)
cache = Cache(app)


@app.route('/cache_dataframe', methods=['POST'])
def cache_dataframe():
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [25, 30, 35, 28],
        'City': ['New York', 'San Francisco', 'Los Angeles', 'Chicago']
    }
    print("hej")
    df = pd.DataFrame(data)

    # Pickle the DataFrame
    pickled_df = pickle.dumps(df)

    try:    # Store the pickled DataFrame in the cache
        cache.set('cached_dataframe', pickled_df)
        return 'DataFrame cached successfully', 200
    except:
        return 'Invalid data provided', 400


@app.route('/get_cached_dataframe', methods=['GET'])
def get_cached_dataframe():
    # Try to retrieve the pickled DataFrame from the cache
    cached_data = cache.get('cached_dataframe')

    if cached_data:
        # Unpickle the DataFrame
        df = pickle.loads(cached_data)
        return jsonify(df.to_dict(orient='records')), 200
    else:
        return 'DataFrame not found in cache', 404


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
    df_bytes = cache.get('df_cache_key')
    df = pickle.loads(df_bytes)
    selected_conds_buy = data['conds_buy']
    selected_conds_sell = data['conds_sell']
    conds = [{"cond": "<"}, {"cond": ">"}, {
        "cond": "=="}, {"cond": "and"}, {"cond": "or"}]
    values = [{"val": 41}, {"val": 48}, {"val": 15}]
    or_and = [{"or_and": "&"}, {"or_and": "or"}]
    # selected_conds = ["empty zero index param", indicators[0], conds[0], values[0]]
    con = Condition(df)
    # con.add_custom_condition(
    #    "vol", "buy", "self.df['volume'] < (self.df['volume'].rolling(window=30).mean().shift(1) * 20)")

    # REMEBER: [[]] INNER NEEDS STR at 0
    for count, cond in enumerate(selected_conds_buy):
        name = cond[0]
        con.make_condition(name, "buy", *cond)
    for count, cond in enumerate(selected_conds_sell):
        name = cond[0]
        con.make_condition(name, "sell", *cond)
    df_signal_buy = con.filter_signals(df, "buy_")
    df_signal_sell = con.filter_signals(df, "sell_")
    print(df_signal_buy.dtypes)
    # removed .values below
    combine_buy_signals = df_signal_buy.values
    combine_sell_signals = df_signal_sell.values
    # will write the prefix to the data
    df = con.combine_signals(combine_buy_signals, "open_trade")
    df = con.combine_signals(combine_sell_signals, "close_trade")
    print(df.head(3))
    df_bytes = pickle.dumps(con.get_df())
    cache.set('df_cache_key', df_bytes)
    json_string = {"message": 'something'}
    # print(df.head(3))
    return json_string


@app.route('/backtest', methods=['GET'])
def backtesting():
    df_bytes = cache.get('df_cache_key')
    df = pickle.loads(df_bytes)
    print("BACK HIT")
    bt = Backtest()
    result = bt.run(df)
    json_string = {"message": f'{result}'}
    return json_string


if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False)
