from typing import *
import logging
import datetime
import time
import pandas as pd

from main_app.data_download.Hdf5 import Hdf5Client
from main_app.data_download.BinanceClient import BinanceClient


logger = logging.getLogger()


def collect_all(client: BinanceClient, exchange: str, symbol: str):

    h5_db = Hdf5Client(exchange)
    h5_db.create_dataset(symbol)

    oldest_ts, most_recent_ts = h5_db.get_first_last_timestamp(symbol)

    # Initial Request

    if oldest_ts is None:
        data = client.get_historical_data(
            symbol, end_time=int(time.time() * 1000) - 60000)

        if len(data) == 0:
            logger.warning("%s %s: no initial data found", exchange, symbol)
            return
        else:
            logger.info("%s %s: Collected %s initial data from %s to %s", exchange, symbol, len(data),
                        ms_to_dt(data[0][0]), ms_to_dt(data[-1][0]))

        oldest_ts = data[0][0]
        most_recent_ts = data[-1][0]

        h5_db.write_data(symbol, data)

    data_to_insert = []

    # Most recent data

    while True:

        data = client.get_historical_data(
            symbol, start_time=int(most_recent_ts + 60000))

        if data is None:
            time.sleep(4)  # Pause in case an error occurs during the request
            continue

        if len(data) < 2:
            break

        data = data[:-1]

        data_to_insert = data_to_insert + data

        if len(data_to_insert) > 10000:
            h5_db.write_data(symbol, data_to_insert)
            data_to_insert.clear()

        if data[-1][0] > most_recent_ts:
            most_recent_ts = data[-1][0]

        logger.info("%s %s: Collected %s recent data from %s to %s", exchange, symbol, len(data),
                    ms_to_dt(data[0][0]), ms_to_dt(data[-1][0]))

        time.sleep(1.1)

    h5_db.write_data(symbol, data_to_insert)
    data_to_insert.clear()

    # Older data

    while True:

        data = client.get_historical_data(
            symbol, end_time=int(oldest_ts - 60000))

        if data is None:
            time.sleep(4)  # Pause in case an error occurs during the request
            continue

        if len(data) == 0:
            logger.info("%s %s: Stopped older data collection because no data was found before %s", exchange, symbol,
                        ms_to_dt(oldest_ts))
            break

        data_to_insert = data_to_insert + data

        if len(data_to_insert) > 10000:
            h5_db.write_data(symbol, data_to_insert)
            data_to_insert.clear()

        if data[0][0] < oldest_ts:
            oldest_ts = data[0][0]

        logger.info("%s %s: Collected %s older data from %s to %s", exchange, symbol, len(data),
                    ms_to_dt(data[0][0]), ms_to_dt(data[-1][0]))

        time.sleep(1.1)

    h5_db.write_data(symbol, data_to_insert)


def ms_to_dt(ms: int) -> datetime.datetime:
    return datetime.datetime.utcfromtimestamp(ms / 1000)


def resample_timeframe(data: pd.DataFrame, tf: str) -> pd.DataFrame:
    return data.resample(TF_EQUIV[tf]).agg(
        {"open": "first", "high": "max", "low": "min",
            "close": "last", "volume": "sum"}
    )


TF_EQUIV = {"1m": "1Min", "5m": "5Min", "15m": "15Min",
            "30m": "30Min", "1h": "1H", "4h": "4H", "12h": "12H", "1d": "D"}
