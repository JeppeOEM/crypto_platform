def infoDict(request):
    data = request.data
    market_type = data['market_type']
    timeframes = data['timeframes']
    ticker = data['ticker']
    tickers = data['tickers']
    from_timestamp = data["timerange_start"]
    end_timestamp = data["timerange_end"]
    the_dict = {
        "market_type": market_type,
        "timeframes": timeframes,
        "ticker": ticker,
        "tickers": tickers,
        "from_timestamp": from_timestamp,
        "end_timestamp": end_timestamp
    }
    return the_dict