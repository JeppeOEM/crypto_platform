from flask import (
    Blueprint, flash, g, redirect, render_template, request, jsonify
)
from werkzeug.exceptions import abort
from main_app.endpoints.auth import login_required
from main_app.database.db import get_db
from main_app.data_download.Hdf5 import Hdf5Client
from main_app.data_download.BinanceClient import BinanceClient
from main_app.data_download.data_collector import collect_all
from main_app.endpoints.data_page.get_hdf5_pairs import get_hdf5_pairs
import importlib
import os
import json
import pandas as pd
import numpy as np
import ccxt


bp = Blueprint('data_page', __name__)


@bp.route('/data_dashboard', methods=('POST', 'GET'))
# @login_required
def data_dashboard():
    if request.method == 'POST':
        print("post")

    if request.method == 'GET':
        print("get")
        exchange = "binance"
        pair_info = get_hdf5_pairs()
        print("first last", pair_info)
        print(pair_info)
        return render_template('data_download/dashboard.html', pair_info=pair_info)


@bp.route('/download_coin', methods=('POST', 'GET'))
def download_coin():
    data = request.get_json()
    client = BinanceClient(False)
    print(data['coin'])
    collect_all(client, "binance", data['coin'])


@bp.route('/get_all_dataset_pairs', methods=('POST', 'GET'))
def get_all_dataset_pairs():
    pair_info = get_hdf5_pairs()
    return jsonify(pair_info)


@bp.route('/get_all_pairs', methods=('POST', 'GET'))
def get_all_pairs():

    if exchange == 'binance':
        exchange = ccxt.binance()

    markets = exchange.load_markets()
    pairs = list(markets.keys())
    spot = []
    margin = []
    for ticker in pairs:
        if ":" in ticker and "-" not in ticker:
            margin.append(ticker)
        elif "-" not in ticker:
            spot.append(ticker)

    data = {"margin": margin, "spot": spot}

    return data
