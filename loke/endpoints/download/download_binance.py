import os
import ccxt
import pandas as pd
import time
import json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
# markets = exchange.load_markets()
# for market in markets:
#     print(market)
# print all possible methods
# lol = dir(ccxt.binance())
# print(lol)

bp = Blueprint('download', __name__)


@bp.route('/binance/all', methods=['GET'])
def get_market_data():
    data = request.get_json()
    print(data, "got the dataaaaaaaaaaaaaaaaaaaa")

    ticker = 'BTC/USDT'
    timeframe = '1m'
    exchange_id = 'binance'
    exchange_class = getattr(ccxt, exchange_id)
    exchange = exchange_class({
        'apiKey': APIK,
        'secret': SK,
    })
    from_ts = exchange.parse8601('2023-09-28 16:00:00')
    print("from_ts", from_ts)

    lowest_stamp, highest_stamp = timestamp_min_max(exchange_id)

    ohlcv_list = []
    ohlcv = exchange.fetch_ohlcv(ticker, timeframe, since=from_ts, limit=1000)
    ohlcv_list.append(ohlcv)
    while True:
        from_ts = ohlcv[-1][0]  # last element in the list
        new_ohlcv = exchange.fetch_ohlcv(
            ticker, timeframe, since=from_ts, limit=1000)
        ohlcv.extend(new_ohlcv[1:])
        time.sleep(1)
        if len(new_ohlcv) != 1000:  # check if there is 1000 in newest data
            break
    df = pd.DataFrame(
        ohlcv, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    # df['date'] = pd.to_datetime(df['date'], unit='ms')
    df.set_index('date', inplace=True)
    df = df.sort_index(ascending=True)
    first_date = df.index.min()
    last_date = df.index.max()
    ticker = ticker.replace('/', '_')

    file_path = f'data/{exchange_id}/{timeframe}_{first_date}_{last_date}_{ticker}.json'
    # print(file_path)
    # print(df.head())
    df.to_csv('lol.csv', index=True)

    df.to_json(file_path)

    return "Lol"


def timestamp_min_max(exchange):

    data_folder = f'data/{exchange}/'

    # Get a list of all files in the data folder
    file_list = os.listdir(data_folder)

    file_data_list = []

    for file_name in file_list:

        parts = file_name.split('_')

        file_data = {
            'lowest': int(parts[1]),
            'highest': int(parts[2])
        }

        file_data_list.append(file_data)

        file_data_list.sort(key=lambda x: x['lowest'])

    overlap = False
    overlap_start = None
    overlap_end = None

    for i in range(len(file_data_list) - 1):
        current_file_data = file_data_list[i]
        next_file_data = file_data_list[i + 1]

        # Check for overlap
        if current_file_data['highest'] >= next_file_data['lowest']:
            overlap = True
            overlap_start = max(
                current_file_data['lowest'], next_file_data['lowest'])
            overlap_end = min(
                current_file_data['highest'], next_file_data['highest'])

            # Calculate the duration of the overlap
            print("current file starting time:", )
            overlap_duration = overlap_end - overlap_start

            print(f"Overlap between {current_file_data['lowest']} and {current_file_data['highest']} "
                  f"and {next_file_data['lowest']} and {next_file_data['highest']}: Duration = {overlap_duration}"
                  f"overlap start", overlap_start, "overlap ends", overlap_end)

    if not overlap:
        print("No overlapping timestamps found")

    # Find the minimum and maximum values
    lowest_stamp = min(file_data['lowest'] for file_data in file_data_list)
    highest_stamp = max(file_data['highest'] for file_data in file_data_list)

    return lowest_stamp, highest_stamp

    # overlapping_entries = TimerangeModel.query.filter(
    #     TimerangeModel.timerange_start <= timerange.timerange_end,
    #     TimerangeModel.timerange_end >= timerange.timerange_start
    # ).all()

    # if overlapping_entries:
    #     overlapping_entries_data = []
    #     for entry in overlapping_entries:
    #         entry_data = {
    #             "id": entry.id,  # Replace with the actual attribute name in your model
    #             "timerange_start": entry.timerange_start,
    #             "timerange_end": entry.timerange_end,
    #             # Add other attributes as needed
    #         }
    #         overlapping_entries_data.append(entry_data)
    #     print(overlapping_entries_data)
