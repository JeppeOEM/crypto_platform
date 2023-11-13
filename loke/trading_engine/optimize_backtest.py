from loke.trading_engine.process_conds import process_conds
from loke.trading_engine.Backtest import Backtest


def optimize_backtest(df, val, val2, val3, parameters, conditions):
    print("conditions")
    print(conditions['conds_buy'])
    print(conditions['conds_sell'])

    buy = conditions['conds_sell']
    sell = conditions['conds_buy']

    sell_dict = {key: value for key, value in conditions.items()
                 if '_SELL' in key}
    buy_dict = {key: value for key, value in conditions.items()
                if '_BUY' in key}

    # print(sell_dict)
    # print(buy_dict)
    for param_name, param_value in parameters.items():
        print(f"Parameter Name: {param_name}, Parameter Value: {param_value}")

    condition_buy = [["name1112221", {
        "ind": "RSI_15"}, {"cond": "<"}, {"val": val2}], ["name1112221", {
            "ind": "volume"}, {"cond": ">"}, {"val": val3}]]
    condition_sell = [["nam22221322", {
        "ind": "RSI_15"}, {"cond": ">"}, {"val": val}]]

    df = process_conds(df, condition_buy, condition_sell)

    backtest = Backtest()
    pnl, drawdown = backtest.run(df)
    return pnl, drawdown
