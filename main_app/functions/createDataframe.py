import pandas as pd
def createDataframe(start_download, end_download, exchange, ticker, timeframe):
    ohlcvs_list = []
    start_download = int(start_download)
    end_download = int(end_download)
    while start_download < end_download:
        print('Fetching candles starting from', start_download)
        ohlcvs = exchange.fetch_ohlcv(ticker, timeframe, start_download)
        if not len(ohlcvs):
            break
        start_download = ohlcvs[-1][0] + exchange.parse_timeframe(timeframe) * 1000
        ohlcvs_list += ohlcvs
    df_ohlcv = pd.DataFrame(ohlcvs_list, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df_ohlcv.set_index('timestamp', inplace=True)
    print("tail of new DF after while loop", df_ohlcv.tail(2))
    return df_ohlcv