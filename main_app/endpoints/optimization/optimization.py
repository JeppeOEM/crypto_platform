from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from main_app.endpoints.auth import login_required
from main_app.database.db import get_db
import importlib
import os
import json
from main_app.trading_engine.Backtest import Backtest
from main_app.trading_engine.Strategy import Strategy
from main_app.trading_engine.call_optimizer import call_optimizer
from main_app.trading_engine.process_conds import process_conds
import pickle
import pandas as pd
import copy
import uuid
import json

bp = Blueprint('optimization', __name__)


@bp.route('/<int:id>/get_optimizer_param', methods=['POST'])
def get_optimizer_param(id):
    try:
        db = get_db()
        data = request.get_json()
        print(data)
        condition_id = data['condition_id']
        side = data['side'][1:].lower()
        print(side, "SIDE")
        if side == "buy":
            table = 'buy_optimization'
        else:
            table = 'sell_optimization'
        params = db.execute(
            'SELECT * FROM {} WHERE fk_strategy_id = ? AND fk_user_id = ? AND fk_condition_id = ?'.format(
                table),
            (id, g.user['id'], condition_id)
        ).fetchone()
        print(dict(params), "PARAMS")
        return jsonify(dict(params)), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500


@bp.route('/<int:id>/optimizer_params', methods=['POST'])
def optimizer_params(id):
    db = get_db()

    data = request.get_json()
    params = data['optimizer_params']
    params_class = data['params_class']
    # fk_list_id = data['fk_list_id']
    # list_row = data['list_row']
    list_row = 1
    try:
        for param in params:
            name, operator, data_type, opti_min, opti_max, side, fk_list_id, fk_condition_id = param
            fk_list_id = int(fk_list_id)
            table_name = 'buy_optimization' if side == 'BUY' else 'sell_optimization'

            exist_query = db.execute(
                'SELECT 1 FROM {} WHERE fk_strategy_id = ? AND fk_condition_id = ? AND fk_user_id = ?'.format(
                    table_name),
                (id, fk_condition_id, g.user['id'])
            )

            exist = exist_query.fetchone()

            if exist:
                db.execute(
                    'UPDATE {} SET optimization_name = ?, operator = ?, data_type = ?, optimization_min = ?, optimization_max = ?, fk_list_id = ?, list_row = ? '
                    'WHERE fk_strategy_id = ? AND fk_condition_id = ? AND fk_user_id = ?'
                    .format(table_name),
                    (name, operator, data_type, opti_min, opti_max,
                     fk_list_id, list_row, id, fk_condition_id, g.user['id'])
                )
            else:
                db.execute(
                    'INSERT INTO {} '
                    '(fk_strategy_id, fk_user_id, optimization_name, data_type, class, operator, '
                    'optimization_min, optimization_max, fk_list_id, list_row, fk_condition_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
                    .format(table_name),
                    (id, g.user['id'], name, data_type, params_class,
                     operator, opti_min, opti_max, fk_list_id, list_row, fk_condition_id)
                )

        db.commit()
        return jsonify({'message': 'optimization saved/updated'})
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
