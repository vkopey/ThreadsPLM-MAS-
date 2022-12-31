# -*- coding: utf-8 -*-
import numpy as np
from sympy import *
from sympy.plotting.plot import plot3d_parametric_line

def helixPoints2(f1="t", f2="t+100", f3="t", h=30, num=50, plot=True):
    x,y,z=symbols('x y z', real=True)
    t=symbols('t', real=True, positive=True)
    P= Matrix([[1,1,0,1]])
    f1=sympify(f1, locals={"t":t})
    T1=Matrix([[cos(f1),0,0,0],
               [0,sin(f1),0,0],
               [0,0,1,0],
               [0,0,0,1]]) # перетворення - поворот навколо Z
    f2=sympify(f2, locals={"t":t})
    T2=Matrix([[f2,0,0,0],
               [0,f2,0,0],
               [0,0,1,0],
               [0,0,0,1]]) # перетворення - масштабування по X,Y
    f3=sympify(f3, locals={"t":t})
    T3=Matrix([[1,0,0,0],
               [0,1,0,0],
               [0,0,1,0],
               [0,0,f3,1]]) # перетворення - переміщення по Z
    T4=Matrix([[1,0,0,0],
               [0,1,0,0],
               [0,0,t,0],
               [0,0,0,1]]) # перетворення - масштабування по Z

    L=P*T1*T2*T3#*T4 # параметричне рівняння гвинтової лінії
    print(L)
    s=solve(Eq(L[2], h), t) # знайти t з рівняння z(t)=h
    tmax=float(s[0].evalf())
    print(f2, 0, L[2]) # рівняння кривої обгортки гвинтової лінії
    fx,fy,fz= lambdify(t, L[0], "numpy"), lambdify(t, L[1], "numpy"), lambdify(t, L[2], "numpy")
    T=np.linspace(0, tmax, num)
    X, Y, Z = fx(T), fy(T), fz(T)
    if plot:
        plot3d_parametric_line((L[0], L[1], L[2], (t, 0, tmax)), (f2, t*0.001, L[2], (t, 0, tmax)), markers=[{'args': [X, Y, Z, 'ko']}])
    return list(zip(X, Y, Z))

## приклад
if __name__=="__main__":
    #5 - крок
    # P=helixPoints2(f1="2*pi*t/5", f2="0.001*t+100", f3="t", h=30, num=2, plot=True)
    # P=helixPoints2(f1="t", f2="0.001*t+100", f3="5*t/(2*pi)", h=30, num=2, plot=True)
    # P=helixPoints2(f1="t", f2="t**2+100", f3="5*t/(2*pi)", h=30, num=2, plot=True)
    P=helixPoints2(f1="2*pi*t/5", f2="t**2+100", f3="t**1.3", h=30, num=2, plot=True)
    # P=helixPoints2(f1="2*pi*t/5", f2="0.001*t+100", f3="Piecewise((t, t <= 10), (2*t-10, t > 10))", h=30, num=2000, plot=True)



