from trading_engine.load_conditions import load_conditions
from trading_engine.Backtest import Backtest


def optimize_backtest(df, val):
    condition_buy = [["name1112221", {
        "ind": "RSI_15"}, {"cond": "<"}, {"val": 45}]]
    condition_sell = [["nam22221322", {
        "ind": "RSI_15"}, {"cond": ">"}, {"val": val}]]

    df = load_conditions(df, condition_buy, condition_sell)

    backtest = Backtest()
    pnl, drawdown = backtest.run(df)
    return pnl, drawdown
