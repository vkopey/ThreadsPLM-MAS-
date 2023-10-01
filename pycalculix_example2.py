# -*- coding: utf-8 -*-
from pycalculix_example import *
import pycalculix_example
pycalculix_example.show_gui = False

def f(x):
    global t,r
    t=x[0]
    r=x[1]
    return run()

if __name__=="__main__":
    import numpy as np
    from scipy.optimize import minimize, brute
    res=brute(f, (slice(1., 3., 1.), slice(1., 3., 1.)), finish=None)
    #res=brute(f, ((1.,3.),(1.,3.)), Ns=2, finish=None)
    print(res)
    #res = minimize(f, x0=[2.0, 2.0], bounds=[(1, 3),(1, 3)])
    #print("argmin=",res.x)
