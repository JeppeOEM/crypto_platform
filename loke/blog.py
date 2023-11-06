from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from loke.auth import login_required
from loke.database.db import get_db
import importlib
import os

# DOES NOT HAVE URL PREFIX SO INDEX = / CREATE = /CREATE
# app.add_url_rule() associates the endpoint name 'index' with the /
# url so that url_for('index') or url_for('blog.index') will both work,
# generating the same / URL either way.
bp = Blueprint('blog', __name__)


def get_indicators():

    indicators = []
    module_path = "loke.trading_engine.indicators.momentum"
    folder_path = "loke/trading_engine/indicators/momentum"

    class_files = [file for file in os.listdir(
        folder_path) if file.endswith(".py") and file != "__init__.py"]

    # Loop through the Python files and import the classes
    for file_name in class_files:
        # Remove the ".py" extension
        module_name = os.path.splitext(file_name)[0]
        module = importlib.import_module(f"{module_path}")
        Obj = getattr(module, f"{module_name}")
        obj = Obj()
        indicators.append(obj.type_dict())

    return indicators


print(get_indicators())


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    strategies = db.execute('SELECT * FROM strategies').fetchall()
    indicators = get_indicators
    parent_list = [{'kind': 'ao', 'fast': 'int', 'slow': 'int', 'offset': 'int'}, {
        'kind': 'rsi', 'length': 'int', 'scalar': 'float', 'talib': 'bool', 'offset': 'int'}]

    return render_template('blog/index.html', posts=posts, strategies=strategies, parent_list=parent_list)



@bp.route('/add_indicator', methods=('POST',))
@login_required
def add_indicator():
    data = request.get_json()  # Parse JSON data from the request body
    indicator = data.get('indicator')  # Get the 'indicator' value
    db = get_db()
    cur = db.execute('SELECT COUNT(*) FROM strategies')
    num_strategies = cur.fetchone()[0]
    num_strategies+=1
    db.execute(
                'INSERT INTO strategy_indicators (strategy_id, indicator_id)'
                ' VALUES (?, ?, ?, ?)',
                (strategy_name, expression, g.user['id'], exchange)
            )
    db.commit()      
    return redirect(url_for('blog.index'))

@bp.route('/createstrat', methods=('GET', 'POST'))
@login_required
def createstrat():
    if request.method == 'POST':
        strategy_name = request.form['strategy_name']
        expression = request.form['expression']
        exchange = request.form['exchange']
        error = None

        if not strategy_name:
            error = 'strategy_name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            
            db.execute(
                'INSERT INTO strategies (strategy_name, expression, fk_user_id, fk_exchange_id)'
                ' VALUES (?, ?, ?, ?)',
                (strategy_name, expression, g.user['id'], exchange)
            )
            db.commit()
            return redirect(url_for('blog.index'))
            cur = db.execute('SELECT COUNT(*) FROM strategies')
    
    if request.method == 'GET':
  
        indicators = [{'kind': 'ao', 'fast': 'int', 'slow': 'int', 'offset': 'int'}, {
        'kind': 'rsi', 'length': 'int', 'scalar': 'float', 'talib': 'bool', 'offset': 'int'}]

    return render_template('blog/createstrat.html',indicators=indicators, num_strategies=num_strategies)


def get_strategy(id, check_user=True):
    strategy = get_db().execute(
        'SELECT p.strategy_id, strategy_name, expression, created, fk_user_id, username'
        ' FROM strategies p JOIN user u ON p.fk_user_id = u.id'
        ' WHERE p.strategy_id = ?',
        (id,)
    ).fetchone()

    if strategy is None:
        abort(404, f"strategy id {id} doesn't exist.")
    print(strategy)
    # print(strategy['fk_user_id'])
    print(g.user['id'])
    if check_user and strategy['fk_user_id'] != g.user['id']:
        abort(403)

    return strategy


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


# converts to int automatically


@bp.route('/<int:id>/stratupdate', methods=('GET', 'POST'))
@login_required
def stratupdate(id):
    strategy = get_strategy(id)

    if request.method == 'POST':
        strategy_name = request.form['strategy_name']
        expression = request.form['expression']
        error = None

        if not strategy_name:
            error = 'strategy_name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE strategies SET strategy_name = ?, expression = ?'
                ' WHERE strategy_id = ?',
                (strategy_name, expression, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/updatestrat.html', strategy=strategy)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))


@bp.route('/<int:id>/deletestrat', methods=('POST',))
@login_required
def deletestrat(id):
    get_strategy(id)
    db = get_db()
    db.execute('DELETE FROM strategies WHERE strategy_id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
