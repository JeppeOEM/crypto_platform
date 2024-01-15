from .load_json_path import load_json_path
from .resample_timeseries import resample_timeseries
import ccxt


def getDataframe(market_type, timeframes, ticker):
    multi_timeframe = False
    print(multi_timeframe)
    print(len(timeframes))
    if len(timeframes) > 1:
        multi_timeframe = True
    exchange_id = 'binance'

    if exchange_id == 'binance':
        exchange = ccxt.binance()
    path = load_json_path(market_type, exchange_id, "1m", ticker)
    print(path)
    df = resample_timeseries(timeframes, path, multi_timeframe)
    return df