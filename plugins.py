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
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, _app_ctx_stack
import os,config

class Plugins:
    pluginsInfo = {}

def scan_plugin():
    for plugindir in os.listdir(self.__pluginPath):
        plugindirpath = os.path.join(self.__pluginPath, plugindir)
        for pluginfile in os.listdir(plugindirpath):
            pluginfilepath = os.path.join(plugindirpath, pluginfile)
            pluginIniPath = os.path.join(plugindirpath, 'plugin.ini')
            if os.path.exists(pluginIniPath):
                print pluginIniPath




