# -*- coding: utf-8 -*-
import os

DEFAULT_PORT = 8888
DEBUG = True
VERSION = '0.0.1'

SERVER_CONF = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "random value",
    "xsrf_cookies": False}

SERVER_DEFAULT_PAGE = "templates/index.html"
LOCAL_STORAGE_PATH = os.path.join(os.path.dirname(__file__), 'tmp')
