from loke.trading_engine.Condition import Condition
import json
from loke.database.db import get_db
import numpy as np


def data_type(d_type):
    if d_type == "float":
        return float
    else:
        return int


def process_conds(df, selected_conds_buy, selected_conds_sell):

    # selected_conds = ["empty zero index param", indicators[0], conds[0], values[0]]
    con = Condition(df)
    # con.add_custom_condition(
    #    "vol", "buy", "self.df['volume'] < (self.df['volume'].rolling(window=30).mean().shift(1) * 20)")

    # REMEBER: [[]] INNER NEEDS STR at 0
    for count, cond in enumerate(selected_conds_buy):
        name = cond[0]
        con.make_condition(name, "buy", *cond)
    for count, cond in enumerate(selected_conds_sell):
        name = cond[0]
        con.make_condition(name, "sell", *cond)
    df_signal_buy = con.filter_signals(df, "buy_")
    df_signal_sell = con.filter_signals(df, "sell_")

    # removed .values below
    combine_buy_signals = df_signal_buy.values
    combine_sell_signals = df_signal_sell.values
    # will write the prefix to the data
    df = con.combine_signals(combine_buy_signals, "open_trade")
    df = con.combine_signals(combine_sell_signals, "close_trade")

    return df


def create_conds(id):
    db = get_db()

    buy = db.execute(
        'SELECT buy_eval FROM buy_conditions WHERE fk_strategy_id = ?', (id,)).fetchall()
    sell = db.execute(
        'SELECT sell_eval FROM sell_conditions WHERE fk_strategy_id = ?', (id,)).fetchall()

    def type_cast(conds):
        for cond in conds:
            for key in cond:
                if key == "val":
                    key['val'] = float(key['val'])
            cond.insert(0, "random")
        return conds
    print(buy)
    print(sell)

    buy_arr = []
    sell_arr = []
    for b in buy:
        bb = json.loads(b[0])
        buy_arr.append(bb)
    for s in sell:
        ss = json.loads(s[0])
        sell_arr.append(ss)

    print(buy_arr)
    print(sell_arr)

    # s_conds = [json.loads(s['buy_eval']) for s in sell]

    buy = type_cast(buy_arr)
    sell = type_cast(sell_arr)

    for idx, arr in enumerate(buy):
        print(arr[idx][1])

        # buy[0].insert(0, "buy")
        # sell[0].insert(0, 'sell')
    def flatten_inner_list(nested_list):
        flattened_list = []

        for sublist in nested_list:
            flat_sublist = [sublist[0]] + sublist[1]
            flattened_list.append(flat_sublist)
        return flattened_list

    buy = flatten_inner_list(buy)
    sell = flatten_inner_list(sell)
    conds = {
        "conds_buy": buy,
        "conds_sell": sell
    }
    params = get_strategy_params(id)
    return conds, params


def get_values(sql_rows):
    buy_arr = []
    for row in sql_rows:
        name = row['optimization_name']
        opti_class = row['class']
        operator = row['operator']
        opti_max = row['optimization_max']
        opti_min = row['optimization_min']
        d_type = row['data_type']
        d_type = data_type(d_type)
        obj = {f"{name}": {"name": opti_class,
                           "type": d_type, "min": opti_min, "max": opti_max}}
        buy_arr.append(obj)
        # for v in val:
        #     print(v)
        #     # arr.append(v[0])

    print("####################BUY ARR##############")
    print(buy_arr)
    return buy_arr


def get_strategy_params(id):
    db = get_db()
    buy = db.execute(
        'SELECT optimization_name, class, data_type, operator, optimization_min, optimization_max FROM buy_optimization WHERE fk_strategy_id = ?', (id,)).fetchall()
    sell = db.execute(
        'SELECT optimization_name, class, data_type, operator, optimization_min, optimization_max FROM sell_optimization WHERE fk_strategy_id = ?', (id,)).fetchall()
    s_arr = get_values(sell)
    b_arr = get_values(buy)

    params = {}

    def build_params(params, arr):
        for opti_param in arr:
            for key, value in opti_param.items():
                params[key] = value

    build_params(params, s_arr)
    build_params(params, b_arr)

    for key, value in params.items():
        # default value is allways float
        if value["type"] == int:
            value["min"] = int(value["min"])
            value["max"] = int(value["max"])

    print("####################SELL STRAT PARAMS##############")
    print(params)

    # params = {
    #     "RSI_15_BUY": {"name": "rsi sell val", "type": int, "min": 15, "max": 55},
    #     "RSI_15_SELL": {"name": "rsi sell val", "type": int, "min": 56, "max": 80},
    # }
    return params


# [["name1112221", {
#     "ind": "RSI_15"}, {"cond": "<"}, {"val": val2}], ["name1112221", {
#         "ind": "volume"}, {"cond": ">"}, {"val": val3}]]


# [['random', [{'ind': 'RSI_15'}, {'cond': '<'}, {'val': 1}]],
#     ['random', [{'ind': 'volume'}, {'cond': '<'}]],['random', [{'ind': 'volume'}, {'cond': '<'}]],['random', [{'ind': 'volume'}, {'cond': '<'}]]]
