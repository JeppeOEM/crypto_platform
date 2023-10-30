import pandas as pd
import numpy as np

from pyhhmm.gaussian import GaussianHMM

def markovModel(original_df):
    df = original_df.copy()
    df["Returns"] = (df["Adj Close"] / df["Adj Close"].shift(1)) - 1
    df["Range"] = (df["High"] / df["Low"]) - 1
    df.dropna(inplace=True)
    df.head()