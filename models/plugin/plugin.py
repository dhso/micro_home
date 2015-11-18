# -*- coding: utf-8 -*-

from models.config import config
import sys, os
reload(sys)
sys.setdefaultencoding('utf-8')

def load_plugins(db, app):
    plugins = {}
    for plugin_name in os.listdir(app.config['PLUGIN_DIR']):
        plugin = {}
        plugin_dir_path = os.path.join(app.config['PLUGIN_DIR'], plugin_name)
        if os.path.isdir(plugin_dir_path):
            plugin_main_file_path = os.path.join(plugin_dir_path, plugin_name + '.py')
            if os.path.exists(plugin_main_file_path):
                plugin_module=__import__("plugins."+ plugin_name+ "."+ plugin_name, fromlist=[plugin_name])
                plugin_module.run(db, app)

def get_plugins(app):
    plugins = {}
    for plugin_name in os.listdir(app.config['PLUGIN_DIR']):
        plugin = {}
        plugin_dir_path = os.path.join(app.config['PLUGIN_DIR'], plugin_name)
        if os.path.isdir(plugin_dir_path):
            plugin_config_path = os.path.join(plugin_dir_path, 'config.ini')
            if os.path.exists(plugin_config_path):
                configs = config.Config(plugin_config_path);
                plugin['name'] = configs.get('base', 'name')
                plugin['path'] = plugin_dir_path
                plugin['icon'] = os.path.join(plugin_dir_path, configs.get('base', 'icon'))
            plugins[plugin_name] = plugin
    return plugins