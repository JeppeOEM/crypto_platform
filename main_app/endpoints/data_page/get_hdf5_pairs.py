from main_app.data_download.Hdf5 import Hdf5Client
from datetime import datetime


def get_hdf5_pairs(exchange):
    h5_db = Hdf5Client(exchange)
    pair_names = h5_db.get_all_dataset_names()
    pair_info = []
    for pair in pair_names:
        first_ts, last_ts = h5_db.get_first_last_timestamp(pair)
        first_ts = datetime.utcfromtimestamp(first_ts / 1000.0)
        last_ts = datetime.utcfromtimestamp(last_ts / 1000.0)
        pair_dict = {pair: (first_ts, last_ts)}
        pair_info.append(pair_dict)
    return pair_info
