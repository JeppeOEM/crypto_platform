from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
import json
import pandas as pd
from loke.database.db import get_db
# from loke.functions.getDataframe import getDataframe
from loke.functions.getDataframe import getDataframe
import json


bp = Blueprint('data_strategy', __name__)


@bp.route('/<int:strategy_id>/load_pickled_df', methods=('POST', 'GET'))
def load_pickled_df(strategy_id):
    data = request.get_json()
    print(strategy_id)
    df = pd.read_pickle('data/pickles/test.pkl')
    print(df, "////////////////////////////////////////////////////////////////")
    print(df.columns, "columns")
    jsonData = createChartJson(df)
    # print(jsonData)

    # DONT use jsonify this time it is converted to json string already
    return jsonData


@bp.route('/<int:strategy_id>/current_chart', methods=('POST', 'GET'))
def current_chart(strategy_id):
    data = request.get_json()
    db = get_db()
    current_pair = db.execute(
        'SELECT pair FROM strategies WHERE fk_strategy_id = ? AND fk_user_id = ?', (strategy_id, g.user['id'])).fetchone()
    # print(jsonData)

    # DONT use jsonify this time it is converted to json string already
    return jsonify(current_pair)


def createChartJson(df):
    # python dictionary not json yet.
    # df.reset_index(inplace=True)
    # array2d = df.to_json(orient='values')
    candlesticks = []
   # df = df.reset_index()
    print(df.columns, "columns")
    # save index as column the name of index, which is timestamp
    df = df.reset_index()
    # Seems timeframe col needs to be called time for the conversion to work
    df.rename(columns={'timestamp': 'time'}, inplace=True)
    df['time'] = df['time'].apply(lambda x: x.timestamp())
    df = df.head(1000)
    json_string = df.to_json(orient='records', date_format='iso')
    json_string = json.dumps(json_string, default=str)

    """""
    for data in array2d:
        candlestick = {
            "time": data[0],
            "open": data[1],
            "high": data[2],
            "low" : data[3],
            "close": data[4],
        }
    candlesticks.append(candlestick)
    """

    return json_string
# @bp.route('/load_df', methods=('POST', 'GET'))
# def load_df():
#     data = request.get_json()
#     market_type = data['market_type']
#     timeframes = data['timeframes']
#     ticker = data['ticker']

#     df = getDataframe(market_type, timeframes, ticker)
#     df.reset_index(inplace=True)
#     print("HEAD HERE")
#     print(timeframes)
#     # print(resampled.head(200).to_string())
#     jsonData = createChartJson(df)
#     print(jsonData)
#     # broken pipe if to large amount of data
#     return jsonify(jsonData)
