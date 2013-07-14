tornado-ips
===========

image processing server in tornado

Version
===========
0.0.1

Setup and run:
===========
pip install -r requirements.txt
python server.py

Usage
===========
        POST requset on
        http://server/process/

        more in example/client.py

Example json
===========
        [{'name': 'grayscale', 'options': []},
        {'name': 'rotate', 'options': [90]},
        {'name': 'mirror', 'options': []},
        {'name': 'filter', 'options': ['find_edges']},
        {'name': 'rotate', 'options': [90]},
        {'name': 'invert', 'options': []},
        {'name': 'text', 'options': ['(145, 230)', 'tornado IPS demo ^^', '#000']},
        {'name': 'save', 'options': ['file.png']}]

Actions description
===========
    This is http wrapper for python image processing library
    http://effbot.org/imagingbook/pil-index.htm#module-reference
    In local storage mode you can get result images like this:

    http://server/getimg/[myimage.png]

New versions
===========
    http://github.com/Sulverus/tornado-ips