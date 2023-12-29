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
# DOES NOT HAVE URL PREFIX SO INDEX = / and CREATE = /CREATE
# app.add_url_rule() associates the endpoint name 'index' with the /
# url so that url_for('index') or url_for('blog.index') will both work,
# generating the same / URL either way.
bp = Blueprint('optimization', __name__)
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