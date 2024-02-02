from flask import (
    Blueprint, flash, g, redirect, render_template, request, jsonify
)
from werkzeug.exceptions import abort
from loke.endpoints.auth import login_required
from loke.database.db import get_db


import importlib
import os
import json
import pandas as pd
import numpy as np


bp = Blueprint('indicators_strategy', __name__)


@bp.route('/<int:strategy_id>/add_indicator', methods=('POST', 'GET'))
# @login_required
def add_indicator(strategy_id):
    if request.method == 'POST':
        data = request.get_json()  # Get the JSON data from the request
        indicator = data.get('indicator')  # Extract the 'indicator' name
        category = data.get('category')
        indicator = indicator.capitalize()
        module_path = f"loke.trading_engine.indicators.{category}.{indicator}"
        module = importlib.import_module(f"{module_path}")
        Obj = getattr(module, f"{indicator}")
        obj = Obj()
        indicator = obj.type_dict()

        indicator = jsonify(indicator)
        print(indicator, "INDICATOR")
        # db = get_db()

        # db.execute(
        #         'INSERT INTO strategy_indicator_forms(fk_user_id, fk_exchange_id)'
        #         ' VALUES (?, ?)',
        #         (g.user['id'], strategy_id)
        # )
        # db.commit()

        return indicator


@bp.route('/<int:strategy_id>/convert_indicator', methods=('POST',))
# @login_required
def convert_indicator(strategy_id):

    if request.method == 'POST':

        data = request.get_json()
        print(data, "DAAAAAAAAAAAAAAAAAAA")
        # remove id from data
        category = data.pop(0)
        print(category, "CATEGORY")
        strategy_indicator_id = data.pop()
        print(strategy_indicator_id, "FORM ID",
              g.user['id'], "USER ID", strategy_id, "STRAT ID")
        indicator = {}
        for item in data:
            key, value = item
            indicator[key] = value
        json_dict = json.dumps(indicator)
        db = get_db()
        # SELECT 1 means it wont return the found row, but 1, as we dont need the row
        # Check if the indicator with the given settings already exists
        existing_indicator = db.execute(
            'SELECT 1 FROM strategy_indicators '
            'WHERE fk_strategy_id = ? AND fk_user_id = ? AND settings = ? AND indicator_name = ?',
            (strategy_id, g.user['id'], json_dict, indicator['kind'])
        ).fetchone()

        if existing_indicator:
            return jsonify({'message': 'Indicator with the same settings already exists. No data inserted.'}), 400

        try:
            # Check if the row with the specified strategy_indicator_id already exists
            existing_row = db.execute(
                'SELECT * FROM strategy_indicators WHERE strategy_indicator_id = ? AND fk_user_id = ? AND fk_strategy_id = ?',
                (strategy_indicator_id, g.user['id'], strategy_id)
            ).fetchone()
            print(existing_row, "EXISTING ROW")
            if existing_row:
                # If the row exists, update it
                db.execute(
                    'UPDATE strategy_indicators SET fk_strategy_id=?, fk_user_id=?, settings=?, indicator_name=? WHERE strategy_indicator_id=?',
                    (strategy_id, g.user['id'], json_dict,
                     indicator['kind'], strategy_indicator_id)
                )
                db.commit()
                return jsonify({'message': 'Indicator successfully updated'}), 200
            else:
                # If the row doesn't exist, insert a new one
                db.execute(
                    'INSERT INTO strategy_indicators (fk_strategy_id, fk_user_id, settings, indicator_name, category) VALUES (?, ?, ?, ?, ?)',
                    (strategy_id, g.user['id'], json_dict,
                     indicator['kind'], category)
                )
                db.commit()
                return jsonify({'message': 'Indicator successfully inserted'})

        except Exception as e:
            # Handle database-related errors
            return jsonify({'error': str(e)}), 500
