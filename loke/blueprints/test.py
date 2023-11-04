from flask import Blueprint
from loke.database.db import get_db, close_db
import pandas as pd
import pandas_ta as ta

test = Blueprint('my_blueprint', __name__)


@test.route('/my_route')
def my_route_function():
    db = get_db()
    cur = db.cursor()
    table = "indicators"
    indicator = "ATR"
    indicator_name = 'RsssssSI'
    # remeber , as it turns value into a tuple
    cur.execute("INSERT INTO indicators (indicator_name) VALUES (?)",
                (indicator_name,))

    db.commit()
    df = pd.DataFrame()

    lol = help(df.ta)
    print(cur)
    return 'This is a route in my blueprint!'
