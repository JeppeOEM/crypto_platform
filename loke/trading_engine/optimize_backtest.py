from loke.trading_engine.process_conds import process_conds
from loke.trading_engine.Backtest import Backtest


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
    if any(isinstance(v, dict) and v.get('ind') == indicator for v in values):
        for v in values:
            if isinstance(v, dict) and 'val' in v:
                v['val'] = val
                break


def update(conds, opti_val):
    for cond in conds:
        for item in opti_val:
            update_val(item[0], item[1], cond)
    return conds


def create_opti_params(params):
    opti_buy = []
    opti_sell = []
    for key, value in params.items():
        if key.endswith('_BUY'):
            key = key[:-4]
            opti_buy.append([key, value])
        if key.endswith('_SELL'):
            key = key[:-5]
            opti_sell.append([key, value])
    return opti_buy, opti_sell


def optimize_backtest(df, params, conditions):
    print("CONDITIOOOOOOOONS")
    print(conditions)
    print("THE params A SLOADED FROM OPTIMIZER")
    print(params)
    print("THE PARAMETERS A SLOADED FROM OPTIMIZER")

    opti_b, opti_s = create_opti_params(params)
    print(opti_b)
    print(opti_s)

    cond_buy = update(conditions['conds_buy'], opti_b)
    print(cond_buy)
    cond_sell = update(conditions['conds_sell'], opti_s)
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
