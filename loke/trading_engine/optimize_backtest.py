from loke.trading_engine.process_conds import process_conds
from loke.trading_engine.Backtest import Backtest
from itertools import chain


def are_nested_arrays_equal(arr1, arr2):
    if len(arr1) != len(arr2):
        return False

    for a, b in zip(arr1, arr2):
        if isinstance(a, list) and isinstance(b, list):
            if not are_nested_arrays_equal(a, b):
                return False
        else:
            if a != b:
                return False

    return True


def optimize_backtest(df, val, val2, val3, parameters, conditions):
    print("conditions optmizse")
    print(conditions['conds_buy'])
    print(conditions['conds_sell'])

    sell = conditions['conds_sell']
    buy = conditions['conds_buy']

    sell_dict = {key: value for key, value in conditions.items()
                 if '_SELL' in key}
    buy_dict = {key: value for key, value in conditions.items()
                if '_BUY' in key}
    print(sell_dict)
    
    # print(sell_dict)
    # print(buy_dict)
    # for param_name, param_value in parameters.items():
    #     print(f"Parameter Name: {param_name}, Parameter Value: {param_value}")

    condition_buy = [["random", {
        "ind": "RSI_15"}, {"cond": "<"}, {"val": val2}], ["random", {
            "ind": "volume"}, {"cond": ">"}, {"val": val3}]]
    condition_sell = [["random", {
        "ind": "RSI_15"}, {"cond": ">"}, {"val": val}]]
    # condition_buy = [["name1112221", {
    #     "ind": "RSI_15"}, {"cond": "<"}, {"val": val2}], ["name1112221", {
    #         "ind": "volume"}, {"cond": ">"}, {"val": val3}]]
    # condition_sell = [["nam22221322", {
    #     "ind": "RSI_15"}, {"cond": ">"}, {"val": val}]]
    print("buy")
    print(buy)
    print("condition buy")
    print(condition_buy)
    if are_nested_arrays_equal(condition_buy, buy):
        print("The nested arrays are equal.")
    else:
        print("The nested arrays are not equal.")

    df = process_conds(df, condition_buy, condition_sell)

    backtest = Backtest()
    pnl, drawdown = backtest.run(df)
    return pnl, drawdown
