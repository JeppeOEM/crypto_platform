import matplotlib.pyplot as plt, mpld3
import time
import matplotlib

def plotPlot(all_labels, colors, reqDict, number_of_states):
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

    plt.savefig(f"data/plots/{ts}_{ticker}_markov_s{number_of_states}_{market_type}.svg")





def preparePlot(df, hidden_states, requestDict):

    prices = df["close"].values.astype(float)
    print("Correct Number of rows: ", len(prices) == len(hidden_states))
    hidden_states.min()
    number_of_states = hidden_states.max()
    i = 0
    all_labels = []
    colors = ["blue","green","red","yellow","black"]


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
        plotPlot(all_labels, colors,requestDict, number_of_states)


    if  number_of_states == 2:
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
        plotPlot(all_labels, colors,requestDict, number_of_states)
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
        plotPlot(all_labels, colors,requestDict, number_of_states)
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
        plotPlot(all_labels, colors, requestDict, number_of_states)

        return labels_0, labels_1, labels_2, labels_3, labels_4


