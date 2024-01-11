from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
import json
import pandas as pd
# from loke.functions.getDataframe import getDataframe

import json


bp = Blueprint('data_strategy', __name__)


@bp.route('/load_df', methods=('POST', 'GET'))
def load_df():
    data = request.get_json()
    market_type = data['market_type']
    timeframes = data['timeframes']
    ticker = data['ticker']

    df = getDataframe(market_type, timeframes, ticker)
    df.reset_index(inplace=True)
    print("HEAD HERE")
    print(timeframes)
    # print(resampled.head(200).to_string())
    jsonData = createChartJson(df)
    print(jsonData)
    # broken pipe if to large amount of data
    return jsonify(jsonData)


def createChartJson(df):
    # python dictionary not json yet.
    # df.reset_index(inplace=True)
    # array2d = df.to_json(orient='values')
    candlesticks = []
   # df = df.reset_index()
    df.rename(columns={'index': 'time'}, inplace=True)
    df['time'] = df['time'].apply(lambda x: x.timestamp())
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
