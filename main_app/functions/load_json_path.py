import os

def load_json_path(market_type, exchange, timeframe, ticker):
    if market_type == "margin":
        cutOutChar = ticker.replace(":", "")
        ticker_parts = cutOutChar.split("/")
    else:
        ticker_parts = ticker.split("/")

    folder_structure = f'data/{market_type}/{exchange}/{ticker_parts[0]}_{ticker_parts[1]}/'

    matching_files = []

    for file in os.listdir(folder_structure):
        if file.startswith(f'{timeframe}_{ticker_parts[0]}_{ticker_parts[1]}'):
            matching_files.append(file)


    if not matching_files:
        raise FileNotFoundError(f"No matching JSON files found in {folder_structure}.")

    # Assuming there is only one matching file, load its content into a JSON object
    file_to_load = matching_files[0]
    file_path = os.path.join(folder_structure, file_to_load)

    # Load the JSON file content into a Python dictionary
#    with open(file_path, 'r') as json_file:
#       json_data = json.load(json_file)

    return file_path
