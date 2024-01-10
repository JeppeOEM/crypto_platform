from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from loke.endpoints.auth import login_required
from loke.database.db import get_db
from loke.endpoints.strategy.strategy import get_strategy

import pandas as pd

bp = Blueprint('conditions', __name__)
# def insert_condition(cond):
#     db = get_db()
#     db.execute('INSERT INTO buy_conditions (fk_strategy_id, fk_user_id, indicator_name, settings) VALUES (?,?,?,?)',
#                    (strategy_id, g.user['id'], indicator['kind'], json_dict))


@bp.route('/<int:strategy_id>/delete_condition', methods=['POST'])
def delete_condition(strategy_id):
    db = get_db()
    data = request.get_json()
    print(data, "DATA")

    if data['side'] == "buy":
        table_name = 'buy_conditions'
    else:
        table_name = 'sell_conditions'

    # Fix the DELETE statement
    db.execute(f'DELETE FROM {table_name} WHERE fk_strategy_id = ? AND fk_user_id = ? AND condition_id = ?',
               (strategy_id, g.user['id'], data['id']))
    db.commit()

    return jsonify({'message': 'condition deleted'}), 200


@bp.route('/<int:strategy_id>/delete_condition_list', methods=['POST'])
def delete_condition_list(strategy_id):
    db = get_db()
    data = request.get_json()
    print(data, "DATA")

    if data['side'] == "buy":
        table_name = 'buy_condition_lists'
    else:
        table_name = 'sell_condition_lists'

    # Fix the DELETE statement
    db.execute(f'DELETE FROM {table_name} WHERE strategy_id = ? AND user_id = ? AND list_id = ?',
               (strategy_id, g.user['id'], data['id']))
    db.commit()

    return jsonify({'message': 'Row updated'}), 200


@bp.route('/<int:strategy_id>/update_condition_row', methods=['POST'])
def update_row(strategy_id):
    db = get_db()
    data = request.get_json()
    print(data, "DATA")

    if data['side'] == "buy":
        table_name = 'buy_conditions'
    else:
        table_name = 'sell_conditions'
    db.execute('UPDATE {} SET list_row = ? WHERE fk_strategy_id = ? AND fk_user_id = ? AND condition_id = ?'.format(
        table_name), (data['list_row'], strategy_id, g.user['id'], data['id']))
    db.commit()
    return jsonify({'message': 'Row updated'}), 200


@bp.route('/<int:strategy_id>/cond_list', methods=('POST', 'GET'))
# @login_required
def cond_list(strategy_id):
    side = request.args.get('side', None)
    print(side, "SIDE")
    if side == "buy":
        table_name = 'buy_condition_lists'
    else:
        table_name = 'sell_condition_lists'

    db = get_db()
    if request.method == 'POST':
        cur = db.cursor()
        cur.execute(
            'INSERT INTO {} (fk_user_id, fk_strategy_id) VALUES (?, ?)'.format(table_name), (g.user['id'], strategy_id))
        db.commit()

        return jsonify({'message': 'Condition list successfully created'}), 200

    if request.method == 'GET':

        cond_lists = db.execute(
            'SELECT * FROM {} '
            'WHERE fk_user_id = ? AND fk_strategy_id = ?'.format(table_name), (g.user['id'], strategy_id)).fetchall()
        # Convert the SQL rows to a list of dictionaries
        result = [dict(row) for row in cond_lists]

        return jsonify(result)


@bp.route('/<int:id>/load_conditions', methods=['GET'])
def load_conditions(id):
    db = get_db()
    buy_conds_cursor = db.execute(
        'SELECT * FROM buy_conditions '
        'WHERE fk_user_id = ? AND fk_strategy_id = ?',
        (g.user['id'], id)
    )
    buy_conds = [dict(row) for row in buy_conds_cursor.fetchall()]

    sell_conds_cursor = db.execute(
        'SELECT * FROM sell_conditions '
        'WHERE fk_user_id = ? AND fk_strategy_id = ?',
        (g.user['id'], id)
    )
    sell_conds = [dict(row) for row in sell_conds_cursor.fetchall()]

    result_dict = {
        'buy_conds': buy_conds,
        'sell_conds': sell_conds
    }

    return jsonify(result_dict), 200


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
    cur = db.cursor()
    data = request.get_json()
    if request.method == 'POST':
        if data['side'] == "buy":
            print("BUY CONDS")
            print(data['buy_cond'])
            existing_indicator = db.execute(
                'SELECT 1 FROM buy_conditions '
                'WHERE fk_strategy_id = ? AND fk_user_id = ? AND indicator_json = ?',
                (id, g.user['id'], data['buy_cond'])
            ).fetchone()

            if existing_indicator:
                return jsonify({'message': 'Condition with the same settings already exists. No data inserted.'}), 400

            try:
                cur.execute(
                    'INSERT INTO buy_conditions (fk_strategy_id, fk_user_id, indicator_json, fk_list_id, list_row) VALUES (?, ?, ?, ?, ?)',
                    (id, g.user['id'], data['buy_cond'],
                     data['primary_key'], 1)
                )
                db.commit()

                last_row = cur.execute('SELECT last_insert_rowid()').fetchone()
                condition_id = last_row[0]
                return jsonify({'id': condition_id}), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        if data['side'] == "sell":

            existing_indicator = db.execute(
                'SELECT 1 FROM sell_conditions '
                'WHERE fk_strategy_id = ? AND fk_user_id = ? AND indicator_json = ?',
                (id, g.user['id'], data['sell_cond'])
            ).fetchone()

            if existing_indicator:
                return jsonify({'message': 'Indicator with the same settings already exists. No data inserted.'}), 400

            try:
                # Insert the indicator if it doesn't exist
                cur.execute(
                    'INSERT INTO sell_conditions (fk_strategy_id, fk_user_id, indicator_json, fk_list_id, list_row) VALUES (?, ?, ?, ?, ?)',
                    (id, g.user['id'], data['sell_cond'],
                     data['primary_key'], 1)
                )
                db.commit()
                last_row = cur.execute('SELECT last_insert_rowid()').fetchone()
                condition_id = last_row[0]
                return jsonify({'id':  condition_id}), 200
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
