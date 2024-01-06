from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from loke.endpoints.auth import login_required
from loke.database.db import get_db
import importlib
import os
import json
from loke.endpoints.strategy.strategy import get_strategy
from loke.trading_engine.Backtest import Backtest
from loke.trading_engine.Strategy import Strategy
from loke.trading_engine.call_optimizer import call_optimizer
from loke.trading_engine.process_conds import process_conds
import pickle
import pandas as pd
import copy

bp = Blueprint('conditions', __name__)
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

    return jsonify(result_dict)


@bp.route('/<int:id>/delete_cond', methods=('POST',))
@login_required
def del_last_buy_cond(id):
    get_strategy(id)
    side = "buy_condition"
    db = get_db()
    table_name = 'buy_condition' if side == 'BUY' else 'sell_condition'

    db.execute('DELETE FROM {}  WHERE strategy_id = ?'.format(table_name), (id,))
    db.commit()
    return redirect(url_for('strategy.index'))


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

                return jsonify({'error': str(e)}), 500

# CREATE ROUTE NAME


@bp.route('/<int:id>/deletestratsssssss', methods=('POST',))
@login_required
def del_last_sell_cond(id):
    get_strategy(id)
    db = get_db()
    db.execute('DELETE FROM strategies WHERE strategy_id = ?', (id,))
    db.commit()
    return redirect(url_for('strategy.index'))
