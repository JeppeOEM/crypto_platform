from loke.trading_engine.process_conds import process_conds
from loke.trading_engine.Backtest import Backtest


def optimize_backtest(df, val, val2, val3):
    condition_buy = [["name1112221", {
        "ind": "RSI_15"}, {"cond": "<"}, {"val": val2}], ["name1112221", {
            "ind": "volume"}, {"cond": ">"}, {"val": val3}]]
    condition_sell = [["nam22221322", {
        "ind": "RSI_15"}, {"cond": ">"}, {"val": val}]]

    df = process_conds(df, condition_buy, condition_sell)

    backtest = Backtest()
    pnl, drawdown = backtest.run(df)
    return pnl, drawdown
