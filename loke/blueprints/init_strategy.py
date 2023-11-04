import pickle
from flask import Blueprint, current_app
from loke.database.db import get_db, close_db
from flask import request
from loke.trading_engine.Strategy import Strategy
from flask_caching import Cache
bp = Blueprint('init_strategy', __name__)


@bp.route('/init_strategy', methods=['POST'])
def init():
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
