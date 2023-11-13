from loke.trading_engine.Condition import Condition
import json
from loke.database.db import get_db


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
        'SELECT buy_eval FROM buy_conditions WHERE fk_strategy_id = ?', (id,)).fetchone()
    sell = db.execute(
        'SELECT sell_eval FROM sell_conditions WHERE fk_strategy_id = ?', (id,)).fetchone()

    def type_cast(d):
        for key in d:
            if key == "val":
                key['val'] = float(key['val'])
        return d
    buy = type_cast(json.loads(buy[0]))
    sell = type_cast(json.loads(sell[0]))
    buy = buy[0].insert(0, "buy")
    sell = sell[0].insert(0, 'sell')

    print(buy, sell)

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
    print(sell)

    params = {
        "RSI_BUY": {"name": "rsi sell val", "type": int, "min": 15, "max": 55},
        "RSI_SELL": {"name": "rsi sell val", "type": int, "min": 56, "max": 80},
    }
    return params
