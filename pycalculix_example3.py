# -*- coding: utf-8 -*-
from pycalculix_example import *
import pycalculix_example
pycalculix_example.show_gui = False
from bottle import route, run, request

@route('/f')
def f():
    global r, t
    r = float(request.query.r)
    t = float(request.query.t)
    return str(pycalculix_example.run())

run(host='localhost', port=8080, debug=True)

"""
# приклад веб-клієнта
import urllib.request
with urllib.request.urlopen('http://localhost:8080/f?r=1&t=1') as response:
   print(response.read())
"""