# -*- coding: utf-8 -*-

from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, _app_ctx_stack, send_from_directory
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required
from flask_user import roles_required
from models.login import auth
from models.config import config
import os

# configuration
SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/flaskr_wechat'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'admin'
PLUGIN_DIR = 'plugins'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
db = SQLAlchemy(app)


def load_plugins(app):
    plugins = {}
    for plugin_name in os.listdir(app.config['PLUGIN_DIR']):
        plugin = {}
        plugin_dir_path = os.path.join(app.config['PLUGIN_DIR'], plugin_name)
        if os.path.isdir(plugin_dir_path):
            plugin_main_file_path = os.path.join(plugin_dir_path, plugin_name + '.py')
            print plugin_main_file_path
            if os.path.exists(plugin_main_file_path):
                plugin_module=__import__("plugins."+ plugin_name+ "."+ plugin_name, fromlist=[plugin_name])
                plugin_module.run(app)

def get_plugins():
    plugins = {}
    for plugin_name in os.listdir(app.config['PLUGIN_DIR']):
        plugin = {}
        plugin_dir_path = os.path.join(app.config['PLUGIN_DIR'], plugin_name)
        if os.path.isdir(plugin_dir_path):
            plugin_config_path = os.path.join(plugin_dir_path, 'config.ini')
            print plugin_config_path
            if os.path.exists(plugin_config_path):
                configs = config.Config(plugin_config_path);
                plugin['name'] = configs.get('base', 'name')
                plugin['path'] = plugin_dir_path
                plugin['icon'] = os.path.join(plugin_dir_path, configs.get('base', 'icon'))
            plugins[plugin_name] = plugin
    print plugins
    return plugins

@app.route('/')
@app.route('/index')
@login_required
def index():
    entries = {}
    plugins = get_plugins()
    return render_template('index.html', entries=entries, plugins = plugins)

@app.route('/plugins/<path:path>')
def get_resource(path):
    return send_from_directory('plugins', path)

@app.route('/member')
@login_required
def member():
    flash('New entry was successfully posted')
    return render_template('ss.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    from models import Admin
    form = LoginForm()
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
    logout_user()
    flash('You were logged out')
    return redirect(url_for('index'))


if __name__ == '__main__':
    user_model = auth.UserModel(db, app)
    #user_model.user_reset()
    user_model.user_model()
    load_plugins(app)
    app.run(host='0.0.0.0')
