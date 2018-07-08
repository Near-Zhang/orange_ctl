import os
from utils.common_api_views import *

plugin = os.path.dirname(os.path.abspath(__file__)).split('/')[-1]

class enable(Base_enable):
    _plugin = plugin

class config(Base_config):
    _plugin = plugin

class fetch_config(Base_fetch_config):
    _plugin = plugin

class sync(Base_sync):
    _plugin = plugin

class selectors(Base_selectors):
    _plugin = plugin

class selectors_order(Base_selectors_order):
    _plugin = plugin

class rules(Base_rules):
    _plugin = plugin

class rules_order(Base_rules_order):
    _plugin = plugin

