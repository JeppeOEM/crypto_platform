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


def update_val(indicator, val, values):
    flag = False
    for v in values:
        if isinstance(v, dict):
            try:
                v['ind'] == indicator
                for vv in values:
                    if 'val' in vv:
                        vv['val'] = val
                        print(vv)

            except:
                continue


# def update_val(indicator, val, conds):
#     print(conds)
#     for l in conds:
#         for indi in l:
#             try:
#                 print(indi['ind'])
#                 print(indicator)
#                 if indi['ind'] == indicator:
#                     indi['val'] = val
#                     break
#             except:
#                 continue
#     return conds


def update(conds, opti_val):
    for cond in conds:
        for item in opti_val:
            update_val(item[0], item[1], cond)
    return conds


def optimize_backtest(df, parameters, conditions):
    val = parameters["RSI_15_BUY"]
    val2 = parameters["RSI_15_SELL"]
    val3 = parameters["volume_BUY"]

    opti = [['RSI_15', val], ['volume', val3]]
    opti_sell = [['RSI_15', val2]]

    cond_buy = update(conditions['conds_buy'], opti)
    print(cond_buy)
    cond_sell = update(conditions['conds_sell'], opti_sell)
    print(cond_sell)

    # print(val)
    # print(val2)
    # print(val3)
    # print("COOOOOOOOONDS OPTIMIZEBACKTEST")
    # print(conditions['conds_buy'])
    # print(conditions['conds_sell'])
    df = process_conds(df, conditions['conds_buy'], conditions['conds_sell'])

    backtest = Backtest()
    pnl, drawdown = backtest.run(df)
    return pnl, drawdown

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
