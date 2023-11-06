from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from loke.auth import login_required
from loke.database.db import get_db
# DOES NOT HAVE URL PREFIX SO INDEX = / CREATE = /CREATE
# app.add_url_rule() associates the endpoint name 'index' with the /
# url so that url_for('index') or url_for('blog.index') will both work,
# generating the same / URL either way.
bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    strategies = db.execute('SELECT * FROM strategies').fetchall()

    return render_template('blog/index.html', posts=posts, strategies=strategies)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
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
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


@bp.route('/createstrat', methods=('GET', 'POST'))
@login_required
def createstrat():
    if request.method == 'POST':
        strategy_name = request.form['strategy_name']
        expression = request.form['expression']
        exchange = request.form['expression']
        error = None

        if not strategy_name:
            error = 'strategy_name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO strategies (strategy_name, expression, fk_user_id, fk_exchange_id)'
                ' VALUES (?, ?, ?)',
                (strategy_name, expression, g.user['id'], exchange)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/createstrat.html')


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


def get_strategy(id, check_author=True):
    strategy = get_db().execute(
        'SELECT s.id, strategy_name, created, expression, username'
        ' FROM strategy s JOIN user u ON s.author_id = u.id'
        ' WHERE s.id = ?',
        (id,)
    ).fetchone()

    if strategy is None:
        abort(404, f"strategy id {id} doesn't exist.")

    if check_author and strategy['fk_user_id'] != g.user['id']:
        abort(403)

    return strategy

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
                'UPDATE post SET strategy_name = ?, expression = ?'
                ' WHERE id = ?',
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
