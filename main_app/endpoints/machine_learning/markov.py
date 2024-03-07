# import mpld3
import matplotlib.pyplot as plt
import matplotlib
import time
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from hmmlearn.hmm import GaussianHMM
import pandas as pd

bp = Blueprint('markov', __name__)

# A standart RSI 14 indicator Must be loaded to the dataframe 

@bp.route('/markov', methods=('POST', 'GET'))
def markov():
    data = request.get_json()
    market_type = data['market_type']
    timeframes = data['timeframes']
    ticker = data['ticker']
    n_comp = data['n_components']
    indicators = data['indicators']
    train_cols = data['train_cols']
    # tickers = data['tickers']
    # from_timestamp = data["timerange_start"]
    # end_timestamp = data["timerange_end"]
    req_dict = {
        "market_type": market_type,
        "timeframes": timeframes,
        "ticker": ticker,
    }
    # df = getDataframe(req_dict['market_type'],
    #                   req_dict['timeframes'], req_dict['ticker'])
    df = pd.read_pickle(f"data/pickles/test.pkl")
    df = df.copy()
    # addIndicators(df, indicators)
    for col in df.columns:
        print(col)
    df.dropna(inplace=True)
    df['volume'] = df['volume'].astype('int64')
    X_train = df[train_cols]
    # model = GaussianHMM(n_states=4, covariance_type='full', n_emissions=2)
    model = GaussianHMM(n_components=n_comp,
                        covariance_type='full', n_iter=100).fit(X_train)
    # model.train([np.array(X_train.values)])
    hidden_states = model.predict(X_train)
    # hidden_states = model.predict([X_train.values])[0]
    prepare_plot(df, hidden_states, req_dict)
    # to_json = df.to_json(orient='records', date_format='iso')
    # json_string = json.dumps(to_json, default=str)
    json_string = {"message": "TEST"}
    return json_string


def plot_plot(all_labels, colors, reqDict, number_of_states):
    matplotlib.use('SVG')
    market_type = reqDict['market_type']
    timeframe = reqDict['timeframes']
    ticker = reqDict["ticker"]
    print("ticker", ticker)
    ticker = ticker.replace(":", "")
    ticker = ticker.replace("/", "")
    print("ticker", ticker)
    ts = time.time()
    for i, label in enumerate(all_labels):
        plt.plot(label, colors[i])

    plt.savefig(
        f"data/plots/{ts}_{ticker}_markov_s{number_of_states}_{market_type}.svg")


def prepare_plot(df, hidden_states, requestDict):

    prices = df["close"].values.astype(float)
    print("Correct Number of rows: ", len(prices) == len(hidden_states))
    hidden_states.min()
    number_of_states = hidden_states.max()
    i = 0
    all_labels = []
    colors = ["blue", "green", "red", "yellow", "black"]

    if number_of_states == 1:
        labels_0 = []
        labels_1 = []
        all_labels = [labels_0, labels_1]
        for s in hidden_states:
            if s == 0:
                labels_0.append(prices[i])
                labels_1.append(float('nan'))

            if s == 1:
                labels_0.append(prices[i])
                labels_1.append(float('nan'))
            i += 1
        plot_plot(all_labels, colors, requestDict, number_of_states)

    if number_of_states == 2:
        labels_0 = []
        labels_1 = []
        labels_2 = []
        all_labels = [labels_0, labels_1, labels_2]
        for s in hidden_states:
            if s == 0:
                labels_0.append(prices[i])
                labels_1.append(float('nan'))
                labels_2.append(float('nan'))
            if s == 1:
                labels_0.append(float('nan'))
                labels_1.append(prices[i])
                labels_2.append(float('nan'))
            if s == 2:
                labels_0.append(float('nan'))
                labels_1.append(float('nan'))
                labels_2.append(prices[i])
            i += 1
        plot_plot(all_labels, colors, requestDict, number_of_states)
        return labels_0, labels_1, labels_2

    if number_of_states == 3:
        labels_0 = []
        labels_1 = []
        labels_2 = []
        labels_3 = []
        all_labels = [labels_0, labels_1, labels_2, labels_3]
        for s in hidden_states:
            if s == 0:
                labels_0.append(prices[i])
                labels_1.append(float('nan'))
                labels_2.append(float('nan'))
                labels_3.append(float('nan'))
            if s == 1:
                labels_0.append(float('nan'))
                labels_1.append(prices[i])
                labels_2.append(float('nan'))
                labels_3.append(float('nan'))
            if s == 2:
                labels_0.append(float('nan'))
                labels_1.append(float('nan'))
                labels_2.append(prices[i])
                labels_3.append(float('nan'))
            if s == 3:
                labels_0.append(float('nan'))
                labels_1.append(float('nan'))
                labels_3.append(float('nan'))
                labels_2.append(prices[i])
            i += 1
        plot_plot(all_labels, colors, requestDict, number_of_states)
        return labels_0, labels_1, labels_2, labels_3

    if number_of_states == 4:
        labels_0 = []
        labels_1 = []
        labels_2 = []
        labels_3 = []
        labels_4 = []
        all_labels = [labels_0, labels_1, labels_2, labels_3, labels_4]
        for s in hidden_states:
            if s == 0:
                labels_0.append(prices[i])
                labels_1.append(float('nan'))
                labels_2.append(float('nan'))
                labels_3.append(float('nan'))
                labels_4.append(float('nan'))
            if s == 1:
                labels_0.append(float('nan'))
                labels_1.append(prices[i])
                labels_2.append(float('nan'))
                labels_3.append(float('nan'))
                labels_4.append(float('nan'))
            if s == 2:
                labels_0.append(float('nan'))
                labels_1.append(float('nan'))
                labels_2.append(prices[i])
                labels_3.append(float('nan'))
                labels_4.append(float('nan'))
            if s == 3:
                labels_0.append(float('nan'))
                labels_1.append(float('nan'))
                labels_2.append(float('nan'))
                labels_3.append(prices[i])
                labels_4.append(float('nan'))
            if s == 4:
                labels_0.append(float('nan'))
                labels_1.append(float('nan'))
                labels_2.append(float('nan'))
                labels_3.append(float('nan'))
                labels_4.append(prices[i])
            i += 1
        plot_plot(all_labels, colors, requestDict, number_of_states)

        return labels_0, labels_1, labels_2, labels_3, labels_4
