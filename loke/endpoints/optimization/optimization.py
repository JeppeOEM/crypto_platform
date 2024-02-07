from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from loke.endpoints.auth import login_required
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
import copy


bp = Blueprint('optimization', __name__)


@bp.route('/<int:id>/optimizer_params', methods=['POST'])
def optimizer_params(id):
    db = get_db()
    data = request.get_json()
    params = data['optimizer_params']
    print(params, "PARAMS")
    params_class = data['params_class']
    # fk_list_id = data['fk_list_id']
    # list_row = data['list_row']
    list_row = 1
    try:
        for param in params:
            name, operator, data_type, opti_min, opti_max, side, fk_list_id = param
            fk_list_id = int(fk_list_id)
            print(param, "PARAzzzzzzzzzzzzzzzzM")
            print(fk_list_id, "FK LIST ID")
            # Check if a row with the same values already exists
            table_name = 'buy_optimization' if side == 'BUY' else 'sell_optimization'
            existing_row = db.execute(
                'SELECT 1 FROM {} '
                'WHERE fk_strategy_id = ? AND optimization_name = ? AND operator = ? AND '
                'data_type = ? AND class = ? AND optimization_min = ? AND optimization_max = ? AND '
                'fk_list_id = ? AND list_row = ?'
                .format(table_name),
                (id, name, operator, data_type, params_class,
                 opti_min, opti_max, fk_list_id, list_row)
            ).fetchone()

            if existing_row:
                print("Row with the same values already exists. Skipping insertion.")
            else:
                db.execute(
                    'INSERT INTO {} '
                    '(fk_strategy_id, fk_user_id, optimization_name, data_type, class, operator, '
                    'optimization_min, optimization_max, fk_list_id, list_row) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
                    .format(table_name),
                    (id, g.user['id'], name, data_type, params_class,
                     operator, opti_min, opti_max, fk_list_id, list_row)
                )

        db.commit()
        return jsonify({'message': 'optimization saved to the database'})
    except Exception as e:
        db.rollback()
        print(e)
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:strategy_id>/optimize', methods=['POST'])
def optimize(strategy_id):
    data = request.get_json()
    # data = request.data
    exchange = data['exchange']
    init_candles = ['init_candles']
    # symbol = data['symbol']
    name = data['name']
    description = data['description']
    # s = Strategy(exchange, init_candles, symbol, name, description)
    # s.addIndicators([
    #     {"kind": "rsi", "length": 15},
    # ])

    # df = s.create_strategy()
    df = pd.read_pickle(f"data/pickles/{name}.pkl")
    # params: df, pop_size, generations, strategy_id
    optimization_result = call_optimizer(df, 5, 5, strategy_id)
    result_json = json.dumps(optimization_result)
    db = get_db()
    try:
        db.execute(
            'INSERT INTO optimization_results'
            '(fk_strategy_id, fk_user_id, result) VALUES (?, ?, ?)',
            (strategy_id, g.user['id'], result_json)
        )
        db.commit()
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

    print(optimization_result)

    # columns = s.column_dict()
    resp = {"message": "optimization complete"}
    return resp


@bp.route('/<int:strategy_id>/optimization_results', methods=['POST'])
def optimization_results(strategy_id):

    db = get_db()
    rows = db.execute(
        'SELECT * FROM optimization_results '
        'WHERE fk_strategy_id = ? AND fk_user_id = ? '
        'ORDER BY optimization_result_id DESC',
        (strategy_id, g.user['id'])
    ).fetchall()

    result_list = [dict(row) for row in rows]

    return jsonify(result_list), 200


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
