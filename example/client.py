# -*- coding: utf-8 -*-
from random import randint
import requests
import json

url = 'http://127.0.0.1:8888/process/'
acts = [{'name': 'grayscale', 'options': []},
        {'name': 'rotate', 'options': [90]},
        {'name': 'mirror', 'options': []},
        {'name': 'filter', 'options': ['find_edges']},
        {'name': 'rotate', 'options': [90]},
        {'name': 'invert', 'options': []},
        {'name': 'text', 'options': ['(145, 230)', 'tornado IPS demo ^^', '#000']},
        {'name': 'save', 'options': ['test_json'+str(randint(1, 1000))+'.png']}]

request_format = {'format': 'local_file', 'filename': 'tux.png'}
post_body = {'command_type': request_format, 'actions': acts}

print requests.post(url, data=json.dumps(post_body)).text