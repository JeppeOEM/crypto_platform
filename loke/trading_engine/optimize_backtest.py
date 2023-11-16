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

    opti_b, opti_s = create_opti_params(params)
    update(conditions['conds_buy'], opti_b)
    update(conditions['conds_sell'], opti_s)
    df = process_conds(df, conditions['conds_buy'], conditions['conds_sell'])

    backtest = Backtest()
    pnl, drawdown = backtest.run(df)
    return pnl, drawdown


