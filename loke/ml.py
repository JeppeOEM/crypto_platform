from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from hmmlearn.hmm import GaussianHMM

bp = Blueprint('ml', __name__)


@bp.route('/markov', methods=('POST', 'GET'))
def markovModel(request):
    data = request.data
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
    df = getDataframe(req_dict['market_type'],
                      req_dict['timeframes'], req_dict['ticker'])

    df = df.copy()
    addIndicators(df, indicators)
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
    preparePlot(df, hidden_states, req_dict)
    to_json = df.to_json(orient='records', date_format='iso')
    json_string = json.dumps(to_json, default=str)
    return HttpResponse(json_string, content_type='application/json')
