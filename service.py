# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~

    A microblog example application written as Flask tutorial with
    Flask and sqlite3.

    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, _app_ctx_stack, send_from_directory
import os,config

# configuration
DATABASE = 'service.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'admin'
PLUGIN_DIR = 'plugins'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect(app.config['DATABASE'])
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db

    return top.sqlite_db

def load_plugins():
    plugins = {}
    for plugin_name in os.listdir(app.config['PLUGIN_DIR']):
        plugin = {}
        plugin_dir_path = os.path.join(app.config['PLUGIN_DIR'], plugin_name)
        plugin_config_path = os.path.join(plugin_dir_path, 'config.ini')
        print plugin_config_path
        if os.path.exists(plugin_config_path):
            configs = config.Config(plugin_config_path);
            plugin['name'] = configs.get('base', 'name')
            plugin['path'] = plugin_dir_path
            plugin['icon'] = os.path.join(plugin_dir_path, configs.get('base', 'icon'))
        plugins[plugin_name] = plugin
    return plugins
            


@app.teardown_appcontext
def close_db_connection(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select name, desc from plugins order by id desc')
    entries = cur.fetchall()
    plugins = load_plugins()
    print plugins
    return render_template('index.html', entries=entries, plugins = plugins)

@app.route('/plugins/<path:path>')
def get_resource(path):
    return send_from_directory('plugins', path)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into plugins (name, desc, author, version) values (?, ?, "hadong", "0.1")',
                 [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0')
