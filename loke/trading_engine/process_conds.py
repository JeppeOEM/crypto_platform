from loke.trading_engine.Condition import Condition
import json
from loke.database.db import get_db


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


def get_conds(id):
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

    return buy, sell


# def get_strategy_params():
#     print("lol")
