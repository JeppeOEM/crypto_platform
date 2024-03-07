import os
import ccxt
import pandas as pd
from functions.createFolder import createFolder
from functions.createDataframe import createDataframe


def download(ticker, timeframe, exchange, from_timestamp, end_timestamp, market_type):
    print(exchange.iso8601(exchange.milliseconds()), 'Loading markets')
    markets = exchange.load_markets()
    print(exchange.iso8601(exchange.milliseconds()), 'Markets loaded')

    if end_timestamp == "now":
        end_timestamp = exchange.milliseconds()

    if market_type == "margin":
        cutOutChar = ticker.replace(":","")
        ticker_parts = cutOutChar.split("/")
    else:
        ticker_parts = ticker.split("/")


    folder_structure = f'data/{market_type}/{exchange}/{ticker_parts[0]}_{ticker_parts[1]}/'
    createFolder(folder_structure)
    file_path = f'{folder_structure}{timeframe}_{ticker_parts[0]}_{ticker_parts[1]}_{from_timestamp}_{end_timestamp}.json'
    #data_folder = f'data/{exchange}/{ticker_parts[0]}_{ticker_parts[1]}'

    file_list = os.listdir(folder_structure)
    rewrite = False
    file_path_to_rewrite = ""
    existing_df = None
    getLatestData = False

    for file_name in file_list:
        filename_parts = file_name.split('_')
        filename_timeframe = filename_parts[0]
        filename_currency1 = filename_parts[1]
        filename_currency2 = filename_parts[2]
        filename_from_timestamp = filename_parts[3]
        filename_end_timestamp = int(filename_parts[4].replace('.json', ''))
        getLatestData = end_timestamp > filename_end_timestamp

        if filename_timeframe == timeframe and filename_currency1 == ticker_parts[0]:
            print(filename_from_timestamp)
            end_timestamp = filename_from_timestamp
            rewrite = True
            print("HIT THE REWRITE THING")
            file_path_to_rewrite = file_name
            try:
                # Read the JSON file into a DataFrame with 'split' orientation
                existing_df = pd.read_json(
                    f'{folder_structure}{file_path_to_rewrite}',
                    orient='split',
                    date_unit='s'
                )
                existing_df.index = existing_df.index.astype('int64')

                print("Successfully loaded the JSON file into a DataFrame:")
                print(existing_df)
                # start_download, end_download, exchange, ticker, timeframe

            except Exception as e:
                print("Error reading the JSON file:", e)

            # downloadLatest(filename_end_timestamp)

            break

    df_ohlcv = createDataframe(int(from_timestamp), int(end_timestamp), exchange, ticker, timeframe)

    if getLatestData:
        print("******************GETTING LATEST TIMESTAMPS*****************")
        end_timestamp = exchange.milliseconds()
        df_latest_timestamps = createDataframe(filename_end_timestamp, end_timestamp, exchange, ticker, timeframe)
        print(df_latest_timestamps.head(1))

    print(from_timestamp, "FROM TIMESTAMP")
    print(end_timestamp, "END TIMESTAMP")
    exchange = ccxt.binance()
    print(exchange.iso8601(exchange.milliseconds()), 'Loading markets')
    markets = exchange.load_markets()
    print(exchange.iso8601(exchange.milliseconds()), 'Markets loaded')

    now = exchange.milliseconds()

    if not rewrite:
        print("NO REWRITE")
        df_ohlcv.to_json(file_path, orient='split', compression='infer')
        print(f"Created a new JSON file: {file_path}")
    else:
        print("REWRITE")
        print("NEW df_ohlcv")
        print(df_ohlcv.head(2))
        print("OLD JSON existing_df")
        print(existing_df.head(2))
        merged_start_timestamp = df_ohlcv.index[0]
        merged_end_timestamp = existing_df.index[-1]
        merged_updated_path = f'{timeframe}_{ticker_parts[0]}_{ticker_parts[1]}_{merged_start_timestamp}_{merged_end_timestamp}.json'
        if getLatestData:
            merged_df = pd.concat([df_ohlcv, existing_df, df_latest_timestamps])
        else:
            merged_df = pd.concat([df_ohlcv, existing_df])

        try:
            merged_df.to_json(f'{folder_structure}{merged_updated_path}', orient='split', compression='infer')
            print(f"JSON file saved successfully: {folder_structure}{merged_updated_path}")
        except Exception as e:
            print(f"Error saving JSON file: {e}")
        if os.path.exists(f'{folder_structure}{file_path_to_rewrite}'):
            os.remove(f'{folder_structure}{file_path_to_rewrite}')
        print(f"Updated the existing JSON file: {file_path_to_rewrite}")
        print(f"To new filename: {file_path}")
        print("Rewrite HEAD merged")
        print(merged_df.head(1))
        print("Rewrite TAIL merged")
        print(merged_df.tail(1))
        print("end stamp", end_timestamp)
