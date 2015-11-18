# -*- coding: utf-8 -*-

from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, _app_ctx_stack, send_from_directory
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, roles_required
from models.login import auth
from models.plugin import plugin
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# configuration
DEBUG = True
SECRET_KEY = 'wechat'
CSRF_ENABLED = True
# datebase
SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/flaskr_wechat'
# plugin
PLUGIN_DIR = 'plugins'
# Flask-Mail settings
MAIL_USERNAME = 'email@example.com'
MAIL_PASSWORD = 'password'
MAIL_DEFAULT_SENDER = '"MyApp" <noreply@example.com>'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = int('465')
MAIL_USE_SSL = int(True)
# Flask-User settings
USER_APP_NAME = "wechat"    # Used by email templates

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
db = SQLAlchemy(app)

@app.route('/')
@app.route('/index')
@login_required
def index():
    entries = {}
    plugins = plugin.get_plugins(app)
    return render_template('index.html', entries=entries, plugins = plugins)

@app.route('/plugins/<path:path>')
def get_resource(path):
    return send_from_directory('plugins', path)

@app.route('/member')
@login_required
def member():
    flash('New entry was successfully posted')
    return render_template('ss.html')

if __name__ == '__main__':
    auth.setup(db, app)
    plugin.load_plugins(db, app)
    app.run(host='0.0.0.0')
