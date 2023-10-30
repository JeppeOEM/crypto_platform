# Read the JSON file into a DataFrame with 'split' orientation
import pandas as pd
import numpy as np
import os
current_directory = os.getcwd()
print(current_directory)

#path = 'data/margin/Binance/1INCH_USDTUSDT/'
#relative_path = os.path.join(current_directory, "data","margin","Binance","1INCH_USDTUSDT", "1m_1INCH_USDTUSDT_159810060000_1696699021660.json")
#print(relative_path)
#if os.path.exists(relative_path):
#    print(f" exists.")
#else:
#    print(f" does not exist.")

#relative_path = r"{}".format(relative_path)

def addMark(df, timeframe, multi_timeframe):

    if timeframe == "5m":
        df.iloc[::5, df.columns.get_loc(timeframe)] = True
        if multi_timeframe == False:
            df = df[df['5m'] == True]
    elif timeframe == "15m":
        df.iloc[::15, df.columns.get_loc(timeframe)] = True
        if multi_timeframe == False:
            df = df[df['15m'] == True]
    elif timeframe == "30m":
        df.iloc[::30, df.columns.get_loc(timeframe)] = True
        if multi_timeframe == False:
            df = df[df['30m'] == True]
    elif timeframe == "1h":
        df.iloc[::60, df.columns.get_loc(timeframe)] = True
        if multi_timeframe == False:
            df = df[df['1h'] == True]
    elif timeframe == "2h":
        df.iloc[::120, df.columns.get_loc(timeframe)] = True
        if multi_timeframe == False:
            df = df[df['2h'] == True]
    elif timeframe == "4h":
        df.iloc[::240, df.columns.get_loc(timeframe)] = True
        if multi_timeframe == False:
            df = df[df['4h'] == True]
    else:
        raise ValueError("Invalid timeframe")


    df.to_json("mask.json", orient='records', compression='infer')

    #df.loc[mask, timeframe] = True

    return df

def resample_timeseries(timeframes, relative_path, multi_timeframe=False):
    df = pd.read_json(relative_path,
        orient='split'
    )
    df.index = pd.to_datetime(df.index)
    for timeframe in timeframes:
        if timeframe != "1m":
            df[timeframe] = False
        for i in range(1445):
            row = df.iloc[i]
            if timeframe == "1m":
                break
            if timeframe == "5m" and row.name.minute % 5 == 0:
                print(f'Index: {row.name} {row.name.minute}')
                print("filtered")
                df = df[df.index >= row.name]
                df = addMark(df, timeframe, multi_timeframe)
                break
            elif timeframe == "15m" and row.name.minute % 15 == 0:
                print(f'Index: {row.name} {row.name.minute}')
                df = df[df.index >= row.name]
                df = addMark(df, timeframe, multi_timeframe)
                break
            elif timeframe == "30m" and row.name.minute % 30 == 0:
                print(f'Index: {row.name} {row.name.minute}')
                df = df[df.index >= row.name]
                df = addMark(df, timeframe, multi_timeframe)
                break
            elif timeframe == "1h" and row.name.minute == 0:
                print(f'Index: {row.name} {row.name.minute}')
                df = df[df.index >= row.name]
                df = addMark(df, timeframe, multi_timeframe)
                break
            elif timeframe == "2h" and row.name.hour % 2 == 0 and row.name.minute == 0:
                print(f'Index: {row.name} {row.name.hour}')
                df = df[df.index >= row.name]
                df = addMark(df, timeframe, multi_timeframe)
                break
            elif timeframe == "4h" and row.name.hour % 4 == 0 and row.name.minute == 0:
                print(f'Index: {row.name} {row.name.hour}')
                df = df[df.index >= row.name]
                df = addMark(df, timeframe, multi_timeframe)
                break

    df.to_json("lol.json", orient='records', compression='infer')
    return df



