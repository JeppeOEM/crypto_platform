from database.Hdf5 import Hdf5Client


import pandas_ta as ta
import numpy as np
import pandas as pd
from numpy.random import randn


class Strategy:
    def __init__(self, exchange, init_candles, symbol, name, description):
        self.init_candles = init_candles
        self.exchange = exchange
        self.symbol = symbol
        self.name = name
        self.description = description
        self.__indicators = []
        self.df = self.initialize()

    def initialize(self):
        h5_db = Hdf5Client(self.exchange)
        data = h5_db.get_rows(self.symbol, self.init_candles)
        return data

    def addIndicators(self, indicators):
        self.__indicators = indicators

    def column_dict(self):
        column_dict = {col: col for col in self.df.columns}
        return column_dict

    def create_strategy(self):
        strategy = ta.Strategy(
            name=self.name, description=self.description, ta=self.__indicators)
        self.df.ta.strategy(strategy)

        return self.df
