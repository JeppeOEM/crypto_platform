from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from loke.auth import login_required
from loke.database.db import get_db
import importlib
import os
import json
from loke.trading_engine.Backtest import Backtest
from loke.trading_engine.Strategy import Strategy
from loke.trading_engine.call_optimizer import call_optimizer
from loke.trading_engine.process_conds import process_conds
import pickle
import pandas as pd
# DOES NOT HAVE URL PREFIX SO INDEX = / CREATE = /CREATE
# app.add_url_rule() associates the endpoint name 'index' with the /
# url so that url_for('index') or url_for('blog.index') will both work,
# generating the same / URL either way.
bp = Blueprint('blog', __name__)


@bp.route('/<int:strategy_id>/add_indicator', methods=('POST', 'GET'))
@login_required
def add_indicator(strategy_id):
    if request.method == 'POST':
        print(strategy_id)
        data = request.get_json()  # Get the JSON data from the request
        indicator = data.get('indicator')  # Extract the 'indicator' value
        category = data.get('category')
        indicator = indicator.capitalize()
        module_path = f"loke.trading_engine.indicators.{category}.{indicator}"
        module = importlib.import_module(f"{module_path}")
        Obj = getattr(module, f"{indicator}")
        obj = Obj()
        indicator = obj.type_dict()
        indicator = jsonify(indicator)
        print(indicator)
        # db = get_db()

        # db.execute(
        #         'INSERT INTO strategy_indicator_forms(fk_user_id, fk_exchange_id)'
        #         ' VALUES (?, ?)',
        #         (g.user['id'], strategy_id)
        # )
        # db.commit()

        return indicator


def get_indicators():

    indicators = []
    module_path = "loke.trading_engine.indicators.momentum"
    folder_path = "loke/trading_engine/indicators/momentum"

    class_files = [file for file in os.listdir(
        folder_path) if file.endswith(".py") and file != "__init__.py"]

    # Loop through the Python files and import the classes
    for file_name in class_files:
        # Remove the ".py" extension
        module_name = os.path.splitext(file_name)[0]
        module = importlib.import_module(f"{module_path}")
        Obj = getattr(module, f"{module_name}")
        obj = Obj()
        indicators.append(obj.type_dict())

    return indicators


@bp.route('/')
def index():
    db = get_db()
    # strategies = db.execute(
    #     'SELECT p.strategy_id, strategy_name, info, created, fk_user_id, username'
    #     ' FROM strategies p JOIN user u ON p.fk_user_id = u.id'
    #     ' ORDER BY created DESC'
    # ).fetchall()

    strategies = db.execute('SELECT * FROM strategies').fetchall()

    return render_template('blog/index.html', strategies=strategies, )


@bp.route('/createstrat', methods=('GET', 'POST'))
@login_required
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

            db.execute(
                'INSERT INTO strategies (strategy_name, info, fk_user_id, fk_exchange_id)'
                ' VALUES (?, ?, ?, ?)',
                (strategy_name, info, g.user['id'], exchange)
            )
            db.commit()
            return redirect(url_for('blog.index'))
            cur = db.execute('SELECT COUNT(*) FROM strategies')

    if request.method == 'GET':
        ndicators = get_indicators
        indicators = [{'kind': 'ao', 'fast': 'int', 'slow': 'int', 'offset': 'int'}, {
            'kind': 'rsi', 'length': 'int', 'scalar': 'float', 'talib': 'bool', 'offset': 'int'}]

    return render_template('blog/createstrat.html', indicators=indicators)


def get_strategy(id, check_user=True):
    strategy = get_db().execute(
        'SELECT p.strategy_id, strategy_name, info,expression, created, fk_user_id, username'
        ' FROM strategies p JOIN user u ON p.fk_user_id = u.id'
        ' WHERE p.strategy_id = ?',
        (id,)
    ).fetchone()

    if strategy is None:
        abort(404, f"strategy id {id} doesn't exist.")
    print(strategy)
    # print(strategy['fk_user_id'])
    print(g.user['id'])
    if check_user and strategy['fk_user_id'] != g.user['id']:
        abort(403)

    return strategy


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:strategy_id>/convert_indicator', methods=('POST',))
@login_required
def convert_indicator(strategy_id):
    print(strategy_id)
    if request.method == 'POST':
        data = request.get_json()  # Get the JSON data from the request
        print(data)
        indicator = {}
        for item in data:
            key, value = item
            indicator[key] = value
        print(indicator)
        json_dict = json.dumps(indicator)
        db = get_db()
        # SELECT 1 means it wont return the found row but 1, as we dont need the row
        # Check if the indicator with the given settings already exists
        print("THIS BOY", )

        existing_indicator = db.execute(
            'SELECT 1 FROM strategy_indicators '
            'WHERE fk_strategy_id = ? AND fk_user_id = ? AND settings = ? AND indicator_name = ?',
            (strategy_id, g.user['id'], json_dict, indicator['kind'])
        ).fetchone()

        if existing_indicator:
            return jsonify({'message': 'Indicator with the same settings already exists. No data inserted.'}), 400

        try:
            # Insert the indicator if it doesn't exist
            db.execute(
                'INSERT INTO strategy_indicators (fk_strategy_id, fk_user_id, settings, indicator_name) VALUES (?, ?, ?, ?)',
                (strategy_id, g.user['id'], json_dict, indicator['kind'])
            )
            db.commit()
            return jsonify({'message': 'Indicator successfully inserted'})
        except Exception as e:
            # Handle database-related errors
            return jsonify({'error': str(e)}), 500

# converts to int automatically


@bp.route('/<int:id>/stratupdate', methods=('GET', 'POST'))
@login_required
def stratupdate(id):
    strategy = get_strategy(id)
    print("Strategy Data:", strategy)
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
            return redirect(url_for('blog.index'))
    if request.method == 'GET':
        indicators = [{'kind': 'ao', 'fast': 'int', 'slow': 'int', 'offset': 'int'}, {
            'kind': 'rsi', 'length': 'int', 'scalar': 'float', 'talib': 'bool', 'offset': 'int'}]
        # settings = db.execute(
        #     'SELECT * FROM strategy_indicators WHERE fk_strategy_id = ?',
        #     (id,)
        # ).fetchall()
        # print(settings)
    return render_template('blog/updatestrat.html', strategy=strategy, indicators=indicators)


@bp.route('/<int:id>/update_chart', methods=['POST'])
@login_required
def update_chart(id):
    print(id)
    db = get_db()

    # Your code to generate or fetch new content
    new_content = "New content fetched from the server"
    return jsonify({'content': new_content})


# def insert_condition(cond):
#     db = get_db()
#     db.execute('INSERT INTO buy_conditions (fk_strategy_id, fk_user_id, indicator_name, settings) VALUES (?,?,?,?)',
#                    (strategy_id, g.user['id'], indicator['kind'], json_dict))


@bp.route('/<int:id>/load_conditions', methods=['POST'])
def load_conditions(id):
    db = get_db()
    buy_conds = db.execute(
        'SELECT buy_eval FROM buy_conditions '
        'WHERE fk_user_id = ? AND fk_strategy_id = ?',
        (g.user['id'], id)
    ).fetchall()

    sell_conds = db.execute(
        'SELECT sell_eval FROM sell_conditions '
        'WHERE fk_user_id = ? AND fk_strategy_id = ?',
        (g.user['id'], id)
    ).fetchall()
    print("load_condtion")
    sell_conds = [row[0] for row in sell_conds]
    buy_conds = [row[0] for row in buy_conds]
    print(sell_conds, "SELL")
    result_dict = {
        'buy_conds': buy_conds,
        'sell_conds': sell_conds
    }
    # result_dict = {
    #     'buy_conds': "buy_conds",
    #     'sell_conds': "sell_conds"
    # }
    print(result_dict)
    return jsonify(result_dict)


@bp.route('/<int:id>/backtest', methods=['POST'])
def backtest(id):
    print(id)
    data = request.get_json()
    name = data['name']
    buy, sell = get_conds(id)
    print(buy, sell)
    # selected_conds_buy = data['conds_buy']
    buy[0].insert(0, "b")
    # selected_conds_sell = data['conds_sell']
    sell[0].insert(0, "s")
    df = pd.read_pickle(f"data/pickles/{name}.pkl")

    df = process_conds(df, buy, sell)
    # df_bytes = pickle.dumps(df)
    # cache.set('df_cache_key', df_bytes)
    df.to_pickle(f"data/pickles/{name}.pkl")

    print("BACK HIT")
    bt = Backtest()
    result = bt.run(df)
    json_string = {"message": f'{result}'}
    return json_string


@bp.route('/<int:id>/optimizer_params', methods=['POST'])
def optimizer_params(id):
    db = get_db()
    data = request.get_json()
    params = data['optimizer_params']
    params_class = data['params_class']

    try:
        for param in params:
            name, operator, data_type, opti_min, opti_max, side = param

            # Check if a row with the same values already exists
            table_name = 'buy_optimization' if side == 'BUY' else 'sell_optimization'
            existing_row = db.execute(
                'SELECT 1 FROM {} '
                'WHERE fk_strategy_id = ? AND optimization_name = ? AND operator = ? AND '
                'data_type = ? AND class = ? AND optimization_min = ? AND optimization_max = ?'
                .format(table_name),
                (id, name, operator, data_type, params_class, opti_min, opti_max)
            ).fetchone()

            if existing_row:
                print("Row with the same values already exists. Skipping insertion.")
            else:
                db.execute(
                    'INSERT INTO {} '
                    '(fk_strategy_id, fk_user_id, optimization_name, data_type, class, operator, '
                    'optimization_min, optimization_max) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
                    .format(table_name),
                    (id, g.user['id'], name, data_type,
                     params_class, operator, opti_min, opti_max)
                )

        db.commit()
        return jsonify({'message': 'optimization saved to the database'})
    except Exception as e:
        db.rollback()
        print(e)
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:id>/optimize', methods=['POST'])
def optimize(id):
    data = request.get_json()
    # data = request.data
    exchange = data['exchange']
    init_candles = ['init_candles']
    symbol = data['symbol']
    name = data['name']
    description = data['description']
    # s = Strategy(exchange, init_candles, symbol, name, description)
    # s.addIndicators([
    #     {"kind": "rsi", "length": 15},
    # ])

    # df = s.create_strategy()
    df = pd.read_pickle(f"data/pickles/{name}.pkl")
    call_optimizer(df, 5, 5, id)

    # columns = s.column_dict()
    resp = {"message": 'optimized'}
    return resp

# Is called when a indicator is submitted and loads indicators to the dataframe


@bp.route('/<int:id>/init_strategy', methods=['POST', 'GET'])
def init_strategy(id):
    if request.method == "POST":
        print(id)
        db = get_db()
        indicators = db.execute(
            'SELECT settings FROM strategy_indicators WHERE fk_strategy_id = ?', (id,)).fetchall()
        total_indicators = []

        # remove kind: name
        for row in indicators:
            try:
                # row 0 = settings
                data_dict = json.loads(row[0])
                for key, value in data_dict.items():
                    print(key, value)
                    if key != "kind":
                        data_dict[key] = int(value) if value.isdigit(
                        ) else float(value) if "." in value else value
                total_indicators.append(data_dict)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")

        data = request.get_json()
        exchange = data['exchange']
        init_candles = ['init_candles']
        symbol = data['symbol']
        name = data['name']
        description = data['description']
        s = Strategy(exchange, init_candles, symbol, name, description)
        s.addIndicators(total_indicators)
        df = s.create_strategy()

        df.to_pickle(f"data/pickles/{name}.pkl")
        cols = df.columns.to_list()
        print(cols)
        # keep kind: name to populate inputs
        indicators_inputs = [row[0] for row in indicators]
        print(indicators)
        return jsonify({"cols": cols, "indicators": indicators_inputs})


@bp.route('/<int:id>/condition', methods=['POST', 'GET'])
def condition(id):
    db = get_db()
    data = request.get_json()
    if request.method == 'POST':
        if data['side'] == "buy":
            print("BUY CONDS")
            print(data['buy_cond'])
            existing_indicator = db.execute(
                'SELECT 1 FROM buy_conditions '
                'WHERE fk_strategy_id = ? AND fk_user_id = ? AND buy_eval = ?',
                (id, g.user['id'], data['buy_cond'])
            ).fetchone()

            if existing_indicator:
                return jsonify({'message': 'Condition with the same settings already exists. No data inserted.'}), 400

            try:
                db.execute(
                    'INSERT INTO buy_conditions (fk_strategy_id, fk_user_id, buy_eval) VALUES (?, ?, ?)',
                    (id, g.user['id'], data['buy_cond'])
                )
                db.commit()
                return jsonify({'message': 'condition saved to database'})
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        if data['side'] == "sell":

            existing_indicator = db.execute(
                'SELECT 1 FROM sell_conditions '
                'WHERE fk_strategy_id = ? AND fk_user_id = ? AND sell_eval = ?',
                (id, g.user['id'], data['sell_cond'])
            ).fetchone()

            if existing_indicator:
                return jsonify({'message': 'Indicator with the same settings already exists. No data inserted.'}), 400

            try:
                # Insert the indicator if it doesn't exist
                db.execute(
                    'INSERT INTO sell_conditions (fk_strategy_id, fk_user_id, sell_eval) VALUES (?, ?, ?)',
                    (id, g.user['id'], data['sell_cond'])
                )
                db.commit()
                return jsonify({'message': 'condition saved to database'})
            except Exception as e:
                # Handle database-related errors
                return jsonify({'error': str(e)}), 500


@bp.route('/<int:id>/deletestrat', methods=('POST',))
@login_required
def deletestrat(id):
    get_strategy(id)
    db = get_db()
    db.execute('DELETE FROM strategies WHERE strategy_id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))


@bp.route('/<int:id>/delete_cond', methods=('POST',))
@login_required
def del_last_buy_cond(id):
    get_strategy(id)
    side = "buy_condition"
    db = get_db()
    table_name = 'buy_condition' if side == 'BUY' else 'sell_condition'

    db.execute('DELETE FROM {}  WHERE strategy_id = ?'.format(table_name), (id,))
    db.commit()
    return redirect(url_for('blog.index'))


@bp.route('/<int:id>/deletestrat', methods=('POST',))
@login_required
def del_last_sell_cond(id):
    get_strategy(id)
    db = get_db()
    db.execute('DELETE FROM strategies WHERE strategy_id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))


@bp.route('/<int:id>/truncate', methods=('POST',))
@login_required
def truncate(id):
    get_strategy(id)
    db = get_db()
    db.execute('DELETE FROM strategies WHERE strategy_id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
