from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
from loke.endpoints.auth import login_required
from loke.database.db import get_db
from loke.trading_engine.Backtest import Backtest
from loke.trading_engine.Strategy import Strategy
from loke.trading_engine.call_optimizer import call_optimizer
from loke.trading_engine.process_conds import process_conds
from loke.controllers.StrategyController import get_strategy_controller
from .func_get_indicators import get_indicators
from loke.endpoints.data_page.get_hdf5_pairs import get_hdf5_pairs

import json
import pandas as pd
import numpy as np
import copy


# DOES NOT HAVE URL PREFIX SO INDEX = / and CREATE = /CREATE
# app.add_url_rule() associates the endpoint name 'index' with the /
# url so that url_for('index') or url_for('strategy.index') will both work,
# generating the same / URL either way.
bp = Blueprint('strategy', __name__)


@bp.route('/')
def index():
    db = get_db()
    # strategies = db.execute(
    #     'SELECT p.strategy_id, strategy_name, info, created, fk_user_id, username'
    #     ' FROM strategies p JOIN user u ON p.fk_user_id = u.id'
    #     ' ORDER BY created DESC'
    # ).fetchall()

    strategies = db.execute('SELECT * FROM strategies').fetchall()
    print(strategies)

    return render_template('strategy/index.html', strategies=strategies, )


@bp.route('/<int:strategy_id>/get_strategy', methods=['GET'])
def get_strategy(strategy_id):
    try:
        db = get_db()
        strategy = db.execute(
            'SELECT * FROM strategies WHERE strategy_id = ? AND fk_user_id = ?', (
                strategy_id, g.user['id'])
        ).fetchone()

        if strategy is not None:
            strategy_dict = dict(strategy)
            print(strategy_dict, "STRATEGY DICT")
            return jsonify(strategy_dict), 200
        else:
            return jsonify({'error': 'Strategy not found'}), 404

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500


@bp.route('/current_df', methods=('GET', 'POST'))
def current_df():
    print("#####################################################################")
    s = get_strategy_controller().get_strategy()
    name = "test"
    df = pd.read_pickle("data/pickles/test.pkl")
    # print(df.head(10), "CURRENT DF")
    return jsonify({"msg": f"{df.head(10)}"})


@bp.route('/<int:strategy_id>/strategy_pair', methods=['POST', 'GET'])
def strategy_pair(strategy_id):
    try:
        db = get_db()

        if request.method == 'POST':
            data = request.get_json()
            new_pair_value = data['pair']

            if new_pair_value is not None:
                db.execute(
                    'UPDATE strategies SET pair = ? WHERE strategy_id = ? AND fk_user_id = ?', (
                        new_pair_value, strategy_id, g.user['id'])
                )
                db.commit()

                return jsonify({'message': 'Pair value updated successfully'}), 200
            else:
                return jsonify({'error': 'Missing new_pair_value in the request'}), 400
        else:
           # Handle GET request if needed

            pair_result = db.execute(
                'SELECT pair FROM strategies WHERE strategy_id = ?', (
                    strategy_id,)
            ).fetchone()

            pair = pair_result['pair']
            return jsonify({'pair': pair}), 200

        # Handle GET request if needed

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:id>/reload_strategy_df', methods=['POST', 'GET'])
def reload_strategy_df(id):
    # db = get_db()
    db = get_db()
    indicators = db.execute(
        'SELECT settings, strategy_indicator_id, category FROM strategy_indicators WHERE fk_strategy_id = ?', (id,)).fetchall()
    total_indicators = []
    total_indicators_id = []
    # print("teeeeest", indicators[1])
    # print("teeeeest", indicators[0][0])
    # remove kind: name
    # THIS IS FOR LOADING DATAFRAME NOT SEND TO FRONTEND
    for row in indicators:
        try:
            # row[0][1] = settings
            data_dict = json.loads(row[0])

            print(data_dict)
            for key, value in data_dict.items():
                if key != "kind":
                    # save as int, float or string
                    data_dict[key] = int(value) if value.isdigit(
                    ) else float(value) if "." in value else value
            # assign id from strategy_indicators to indicator
                    # DANGER HERE
            # data_dict['id'] = row[1]
            # print("data_dict", data_dict)
            # copy object to avoid changing original
            data_dict_copy = copy.deepcopy(data_dict)
            total_indicators.append(data_dict)
            json_object = json.dumps(data_dict_copy, indent=4)
            total_indicators_id.append(
                {"id": row[1], "settings": json_object, "category": row[2]})

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    # strategy = db.execute(
    #     'SELECT pair, strategy_name, info FROM strategies WHERE strategy_id = ?', (
    #         id,)
    # ).fetchone()
    # exchange = "binance"
    # init_candles = 100
    # pair = strategy['pair']
    # name = strategy['strategy_name']
    # description = strategy['info']
    # s = Strategy(exchange, init_candles, pair, name, description)

    # s.addIndicators(total_indicators)
    # df = s.create_strategy()

    # df.to_pickle(f"data/pickles/{name}.pkl")


@bp.route('/<int:id>/init_strategy', methods=['POST', 'GET'])
def init_strategy(id):
    if request.method == "POST":

        db = get_db()
        indicators = db.execute(
            'SELECT settings, strategy_indicator_id, category, chart_info FROM strategy_indicators WHERE fk_strategy_id = ?', (id,)).fetchall()
        total_indicators = []
        total_indicators_id = []
        # print("teeeeest", indicators[1])
        # print("teeeeest", indicators[0][0])
        # remove kind: name
        # THIS IS FOR LOADING DATAFRAME NOT SEND TO FRONTEND
        for row in indicators:
            try:
                # row[0][1] = settings
                data_dict = json.loads(row[0])

                print(data_dict)
                for key, value in data_dict.items():
                    if key != "kind":
                        # save as int, float or string
                        data_dict[key] = int(value) if value.isdigit(
                        ) else float(value) if "." in value else value
                # assign id from strategy_indicators to indicator
                        # DANGER HERE
                # data_dict['id'] = row[1]
                # print("data_dict", data_dict)
                # copy object to avoid changing original
                data_dict_copy = copy.deepcopy(data_dict)
                total_indicators.append(data_dict)
                json_object = json.dumps(data_dict_copy, indent=4)
                # total_indicators_id.append(
                #     {"id": row[1], "settings": json_object, "category": row[2]})
                total_indicators_id.append(
                    {"id": row[1], "settings": json_object, "category": row[2], "chart_info": row[3]})

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")

        try:
            # Assuming 'db' is your SQLite database connection
            pair_result = db.execute(
                'SELECT pair, strategy_name, info FROM strategies WHERE strategy_id = ?', (
                    id,)
            ).fetchone()

            pair = pair_result['pair']
            name = pair_result['strategy_name']
            description = pair_result['info']
            # This will print the string value of 'pair'

            db.commit()

        except Exception as e:
            print(e)
            return jsonify({'error': str(e)}), 500

        exchange = "binance"
        init_candles = 100

        print("¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤INIT STRATEGY¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤")

        print(exchange, init_candles, pair, name, description)
        s = Strategy(exchange, init_candles, pair, name, description)

        s.addIndicators(total_indicators)
        df = s.create_strategy()

        df.to_pickle(f"data/pickles/{name}.pkl")
        cols = df.columns.to_list()
        # print(cols, "COLUMNS")
        # print(df)
        # keep kind: name to populate inputs
        # get_strategy_controller().set_strategy(s)
        # ss = get_strategy_controller().get_strategy()

        dataset_pairs = get_hdf5_pairs(exchange)
        print("DATASET PAIRS", dataset_pairs,
              "¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤")
        print(dataset_pairs, "DATASET PAIRS")
        return jsonify({"cols": cols, "indicators":  total_indicators_id, "dataset_pairs": dataset_pairs})


# @bp.route('/<int:strategy_id>/strategy', methods=('GET', 'POST'))
# # @login_required
# def strategy(strategy_id):

#     return render_template('strategy/{strategy_id}/updatestrat.html')


@bp.route('/createstrat', methods=('GET', 'POST'))
# @login_required
def createstrat():
    if request.method == 'POST':
        strategy_name = request.form['strategy_name']
        info = request.form['info']
        exchange = request.form['exchange']
        error = None

        if not strategy_name:
            error = 'strategy_name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cur = db.cursor()

            try:
                cur.execute(
                    'INSERT INTO strategies (strategy_name, info, fk_user_id, fk_exchange_id, pair)'
                    ' VALUES (?, ?, ?, ?, ?)',
                    (strategy_name, info, g.user['id'], exchange, "ETHUSDT")
                )

                last_row = cur.execute('SELECT last_insert_rowid()').fetchone()
                strategy_id = last_row[0]
                # strategy starts with 2 list allways

                cur.execute(
                    'INSERT INTO condition_lists (fk_user_id, fk_strategy_id, side)'
                    ' VALUES (?, ?, ?)',
                    (g.user['id'], strategy_id, "buy")
                )
                cur.execute(
                    'INSERT INTO condition_lists (fk_user_id, fk_strategy_id, side)'
                    ' VALUES (?, ?, ?)',
                    (g.user['id'], strategy_id, "sell")
                )

                db.commit()

            except Exception as e:
                # An error occurred, rollback the transaction
                db.rollback()
                print("##########################################################")
                print("Error!!: {}".format(e))
                flash(f"Error: {str(e)}")
            return redirect(url_for('strategy.stratupdate', id=strategy_id))

    # NO get request ever send
    if request.method == 'GET':
        return render_template('strategy/createstrat.html')

    # db.execute(
    #     'INSERT INTO sell_condition_lists (fk_user, fk_strategy_id, frontend_id)'
    #     ' VALUES (?, ?, ?)',
    #     (g.user['id'], strategy_id exchange)
    # )


# This is the page were you can add indicators to a strategy
@bp.route('/<int:id>/stratupdate', methods=('GET', 'POST'))
# @login_required
def stratupdate(id):
    strategy = get_strategy(id)
    if request.method == 'POST':

        strategy_name = request.form['strategy_name']
        info = request.form['info']
        error = None

        if not strategy_name:
            error = 'strategy_name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE strategies SET strategy_name = ?, info = ?'
                ' WHERE strategy_id = ?',
                (strategy_name, info, id)
            )
            db.commit()
            return redirect(url_for('strategy.index'))

    if request.method == 'GET':
        momentum = get_indicators("momentum")
        trend = get_indicators("trend")

    return render_template('strategy/updatestrat.html', strategy=strategy, momentum=momentum, trend=trend)


def get_strategy(id, check_user=True):
    strategy = get_db().execute(
        'SELECT p.strategy_id, strategy_name, info,expression, created, fk_user_id, username'
        ' FROM strategies p JOIN user u ON p.fk_user_id = u.id'
        ' WHERE p.strategy_id = ?',
        (id,)
    ).fetchone()

    if strategy is None:
        abort(404, f"strategy id {id} doesn't exist.")

    if check_user and strategy['fk_user_id'] != g.user['id']:
        abort(403)

    return strategy


# @bp.route('/<int:id>/update_chart', methods=['POST'])
# #@login_required
# def update_chart(id):
#     print(id)
#     db = get_db()

#     # Your code to generate or fetch new content
#     new_content = "New content fetched from the server"
#     return jsonify({'content': new_content})


@bp.route('/<int:id>/truncate', methods=('POST',))
# @login_required
def truncate(id):
    get_strategy(id)
    db = get_db()
    db.execute('DELETE FROM strategies WHERE strategy_id = ?', (id,))
    db.commit()
    return redirect(url_for('strategy.index'))


# @bp.route('/<int:id>/backtest', methods=['POST'])
# def backtest(id):
#     print(id)
#     data = request.get_json()
#     name = data['name']
#     buy, sell = get_conds(id)
#     print(buy, sell)
#     # selected_conds_buy = data['conds_buy']
#     buy[0].insert(0, "b")
#     # selected_conds_sell = data['conds_sell']
#     sell[0].insert(0, "s")
#     df = pd.read_pickle(f"data/pickles/{name}.pkl")

#     df = process_conds(df, buy, sell)
#     # df_bytes = pickle.dumps(df)
#     # cache.set('df_cache_key', df_bytes)
#     df.to_pickle(f"data/pickles/{name}.pkl")

#     print("BACK HIT")
#     bt = Backtest()
#     result = bt.run(df)
#     json_string = {"message": f'{result}'}
#     return json_string


@bp.route('/<int:id>/deletestrat', methods=('POST',))
# @login_required
def deletestrat(id):
    get_strategy(id)
    db = get_db()
    db.execute('DELETE FROM strategies WHERE strategy_id = ?', (id,))
    db.commit()
    return redirect(url_for('strategy.index'))
# def insert_condition(cond):
#     db = get_db()
#     db.execute('INSERT INTO buy_conditions (fk_strategy_id, fk_user_id, indicator_name, settings) VALUES (?,?,?,?)',
#                    (strategy_id, g.user['id'], indicator['kind'], json_dict))


# @bp.route('/<int:id>/load_conditions', methods=['POST'])
# def load_conditions(id):
#     db = get_db()
#     buy_conds = db.execute(
#         'SELECT indicator_json FROM buy_conditions '
#         'WHERE fk_user_id = ? AND fk_strategy_id = ?',
#         (g.user['id'], id)
#     ).fetchall()

#     sell_conds = db.execute(
#         'SELECT indicator_json FROM sell_conditions '
#         'WHERE fk_user_id = ? AND fk_strategy_id = ?',
#         (g.user['id'], id)
#     ).fetchall()
#     print("load_condtion")
#     sell_conds = [row[0] for row in sell_conds]
#     buy_conds = [row[0] for row in buy_conds]
#     print(sell_conds, "SELL")
#     result_dict = {
#         'buy_conds': buy_conds,
#         'sell_conds': sell_conds
#     }

#     return jsonify(result_dict)


# @bp.route('/<int:id>/delete_cond', methods=('POST',))
# #@login_required
# def del_last_buy_cond(id):
#     get_strategy(id)
#     side = "buy_condition"
#     db = get_db()
#     table_name = 'buy_condition' if side == 'BUY' else 'sell_condition'

#     db.execute('DELETE FROM {}  WHERE strategy_id = ?'.format(table_name), (id,))
#     db.commit()
#     return redirect(url_for('strategy.index'))

# @bp.route('/<int:id>/condition', methods=['POST', 'GET'])
# def condition(id):
#     db = get_db()
#     data = request.get_json()
#     if request.method == 'POST':
#         if data['side'] == "buy":
#             print("BUY CONDS")
#             print(data['buy_cond'])
#             existing_indicator = db.execute(
#                 'SELECT 1 FROM buy_conditions '
#                 'WHERE fk_strategy_id = ? AND fk_user_id = ? AND indicator_json = ?',
#                 (id, g.user['id'], data['buy_cond'])
#             ).fetchone()

#             if existing_indicator:
#                 return jsonify({'message': 'Condition with the same settings already exists. No data inserted.'}), 400

#             try:
#                 db.execute(
#                     'INSERT INTO buy_conditions (fk_strategy_id, fk_user_id, indicator_json) VALUES (?, ?, ?)',
#                     (id, g.user['id'], data['buy_cond'])
#                 )
#                 db.commit()
#                 return jsonify({'message': 'condition saved to database'})
#             except Exception as e:
#                 return jsonify({'error': str(e)}), 500

#         if data['side'] == "sell":

#             existing_indicator = db.execute(
#                 'SELECT 1 FROM sell_conditions '
#                 'WHERE fk_strategy_id = ? AND fk_user_id = ? AND indicator_json = ?',
#                 (id, g.user['id'], data['sell_cond'])
#             ).fetchone()

#             if existing_indicator:
#                 return jsonify({'message': 'Indicator with the same settings already exists. No data inserted.'}), 400

#             try:
#                 # Insert the indicator if it doesn't exist
#                 db.execute(
#                     'INSERT INTO sell_conditions (fk_strategy_id, fk_user_id, indicator_json) VALUES (?, ?, ?)',
#                     (id, g.user['id'], data['sell_cond'])
#                 )
#                 db.commit()
#                 return jsonify({'message': 'condition saved to database'})
#             except Exception as e:
#                 # Handle database-related errors
#                 return jsonify({'error': str(e)}), 500


# @bp.route('/<int:id>/deletestrat', methods=('POST',))
# #@login_required
# def del_last_sell_cond(id):
#     get_strategy(id)
#     db = get_db()
#     db.execute('DELETE FROM strategies WHERE strategy_id = ?', (id,))
#     db.commit()
#     return redirect(url_for('strategy.index'))
