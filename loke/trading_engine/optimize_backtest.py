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


def update_val(indicator, val, condition_buy):
    flag = False
    for l in condition_buy:
        for inner in l:
            try:
                if inner['ind'] == indicator:
                    continue
                    flag = True

            except:
                continue
            try:
                if flag and inner['val']:
                    print(inner['val'])
                    inner['val'] = val
                    flag = False
            except:
                continue
    return condition_buy


def optimize_backtest(df, parameters, conditions):
    val = parameters["RSI_15_BUY"]
    val2 = parameters["RSI_15_SELL"]
    val3 = parameters["volume_BUY"]

    condition_buy = conditions['conds_buy']
    condition_sell = conditions['conds_sell']

    opti = [['RSI_15', val], ['volume', val3]]
    opti_sell = [['RSI_15', val2]]
    for item in opti:
        condition_buy = update_val(item[0], item[1], condition_buy)

    # for item in opti_sell:
    #     condition_sell = update_val(item[0], item[1], condition_sell)
    # condition_buy = [["random", {
    #     "ind": "RSI_15"}, {"cond": "<"}, {"val": val2}], ["random", {
    #         "ind": "volume"}, {"cond": ">"}, {"val": val3}]]
    # condition_sell = [["random", {
    #     "ind": "RSI_15"}, {"cond": ">"}, {"val": val}]]
    # condition_buy = [["name1112221", {
    #     "ind": "RSI_15"}, {"cond": "<"}, {"val": val2}], ["name1112221", {
    #         "ind": "volume"}, {"cond": ">"}, {"val": val3}]]
    # condition_sell = [["nam22221322", {
    #     "ind": "RSI_15"}, {"cond": ">"}, {"val": val}]]

    df = process_conds(df, condition_buy, condition_sell)

    backtest = Backtest()
    pnl, drawdown = backtest.run(df)
    return pnl, drawdown
