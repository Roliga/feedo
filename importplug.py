#!/bin/python3

# 
# Module to import plugins (really just python modules) in a specified directory
#

import importlib
import os
import sys

def import_plugins(path):
    sys.path.insert(0, path)

    plugins = {}

    for plugin in os.listdir(path):
        if plugin[-3:] == '.py':
            name = plugin[:-3]
            plugins[name] = importlib.import_module(name)

    return plugins
