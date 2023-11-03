def get_all_tickers(exchange, market_type):
    markets = exchange.load_markets()
    tickers = list(markets.keys())
    spot = []
    margin = []
    for ticker in tickers:
        if ":" in ticker and "-" not in ticker:
            margin.append(ticker)
        elif "-" not in ticker:
            spot.append(ticker)
    if market_type == "spot":
        return spot
    if market_type == "margin":
        return margin

    return margin, spot