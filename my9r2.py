# -*- coding: utf-8 -*-
import ray
import time,random
import numpy as np
from scipy.optimize import curve_fit

def dict2arr(XY):
    "Converts dictionary to X and Y arrays with X ordered"
    X=np.array(list(XY.keys()))
    Y=np.array(list(XY.values()))
    I=X.argsort(); X,Y=X[I],Y[I] # сортуємо по X
    return X,Y

def f(x): # тестова функція, у якої шукаємо мінімум
    #time.sleep(10) # імітація тривалих обчислень
    return (np.sin(x)-2.5)**2

@ray.remote
class FEA(object):
    def __init__(self):
        self.ready=dict()
    def rule(self, x=0.1):
        if x in self.ready: return self.ready[x]#None
        import mypycalculix
        mypycalculix.show_gui = False
        mypycalculix.hh=x
        s=mypycalculix.run(str(x)[:7]+'_'+str(id(self)))
        # s=f(x)
        self.ready[x]=s
        return s

##
class Opti(object):
    "Agent for finding the minimum. Abstract base class"
    def __init__(self, f):
        "f - optimization object (function or ray.actor.ActorHandle)"
        self.f=f
        self.i=1
    def calc(self, x):
        "Return function value by argument x"
        if type(self.f)==ray.actor.ActorHandle:
            return ray.get(self.f.rule.remote(x)) # якщо агент
        return self.f(x) # якщо функція
    def find(self, XY):
        pass
    def rule(self):
        "Agent behavior rule"
        XY={}
        while len(XY)<20: # умова завершення роботи
            #X,Y=dict2arr(XY); i=Y.argmin()
            #while Y[i-2:i+3].std()>0.01 # або така

            XY=ray.get(e.getXY.remote()) # отримати середовище
            XY_={x:XY[x] for x in XY if XY[x]!=None} # без None
            x=self.find(XY_) # шукати перспективний x в XY
            if x==None: continue # якщо немає
            if not ray.get(e.setxy.remote(x, None)): continue # запобігти повторних обчислень
            print(self.i, self.__class__.__name__, x)
            self.i+=1
            y=self.calc(x) # обчислити y
            ray.get(e.setxy.remote(x,y)) # передати в середовище
        return None

##
@ray.remote
class OptiR(Opti):
    "Agent for finding the minimum by the regression model"
    def __init__(self, f, F):
        "F - function-model"
        Opti.__init__(self, f)
        self.F=F

    def fit(self, X, Y):
        "Returns model coefficients and R**2"
        popt, pcov = curve_fit(self.F, X, Y)
        R2=np.corrcoef(Y, self.F(X, *popt))[0,1]**2
        return  popt, R2

    def find(self, XY):
        "Returns the minimum argument of the function f calculated by the grid method from regression"
        if len(XY)<6: return None # недостатньо даних
        X,Y=dict2arr(XY)
        popt, R2 = self.fit(X,Y) # отримати модель
        if R2<0.5: return None # модель погана
        x=np.linspace(X.min(), X.max(), 1000) # сітка значень x
        Y=self.F(x, *popt) # відповідні значення y
        i=Y.argmin() # індекс мінімуму
        x=x[i] # аргумент мінімуму
        return x

##
@ray.remote
class OptiX(Opti):
    "Agent for finding the minimum by the grid-stochastic method"
    def __init__(self, f):
        Opti.__init__(self, f)

    def find(self, XY):
        "Returns the argument of the minimum of the function f calculated by the grid-stochastic method"
        X,Y=dict2arr(XY)
        I=Y.argsort() # індекси сортування по Y
        i=int(abs(np.random.normal(0, 1)))#len(X)/6 # випадковий індекс 0,1,2...
        if i>len(X)-1: i=len(X)-1 # не виходити за межі
        i=I[i] # індекс найменшого у Y
        # сусід зліва (-1) справа (+1)
        if i==0: d=1 # якщо крайній лівий
        elif i==len(X)-1: d=-1 # якщо крайній правий
        else: d=np.random.choice([-1, 1]) # якщо не крайній
        j=i+d # індекс сусіда
        dx=abs((X[i]-X[j])/2) # крок по X
        x=X[i]+d*dx
        return x

##
@ray.remote
class Environment(object):
    "Agent environment for optimization agens with X, Y values"
    def __init__(self, XY={}):
        self.XY=XY # словник даних X, Y
    def getXY(self): # прочитати все
        return self.XY
    def setXY(self, XY): # записати все
        self.XY=XY
    def setxy(self, x, y): # записати пару
        if x in self.XY and y==None: return False # якщо зарезервовано
        self.XY[x]=y
        return True

##Приклад оптимізації
if __name__=='__main__':
    ray.init()
    #X=np.linspace(0., 5., 6) # сітка початкових X
    X=np.linspace(0.08, 0.2, 6)
    e=Environment.remote() # актор-середовище
    # актори-агенти для оптимізації
    O=[OptiX.remote(FEA.remote()) for x in X]
    Y=ray.get([o.calc.remote(x) for o,x in zip(O,X)]) # початкові значення
    ray.get(e.setXY.remote(dict(zip(X, Y)))) # установити поч. середовище
    # додаткові актори-агенти для оптимізації іншим методом
    O.append(OptiR.remote(FEA.remote(), lambda x,a,b,c: a*x**2+b*x+c))
    O.append(OptiR.remote(FEA.remote(), lambda x,a,b,c,d: a*x**3+b*x**2+c*x+d))

    ray.get([o.rule.remote() for o in O]) # агенти працюють, поки усі не повернуть None

    XY=ray.get(e.getXY.remote())
    X,Y=dict2arr(XY)
    print("argmin:", X[Y.argmin()]) # мінімум
    # візуалізація:
    x=np.linspace(X.min(), X.max(), 100)
    import matplotlib.pyplot as plt
    #plt.plot(x,f(x)) # тестова функція
    popt, R2=ray.get(O[-1].fit.remote(X,Y))
    f=lambda x,a,b,c,d: a*x**3+b*x**2+c*x+d
    plt.plot(x,f(x, *popt))
    plt.plot(X,Y,"o") # її точки
    plt.show()

    ray.shutdown()
"""
argmin: 0.2
len(X)=23
calc time 17 min=1020 s (5.6 times faster)
X=[0.08      , 0.092     , 0.104     , 0.116     , 0.128     ,
       0.14      , 0.152     , 0.158     , 0.164     , 0.16788589,
       0.17105105, 0.17117117, 0.17141141, 0.17177177, 0.17189189,
       0.17388589, 0.176     , 0.182     , 0.188     , 0.191     ,
       0.194     , 0.197     , 0.2       ]
Y=[38618729.67123595, 36860824.02985587, 36150937.53901827,
       35948449.77464258, 35793019.13641821, 35664023.10830902,
       35547121.39625373, 35492154.05353696, 35439526.62875169,
       35406542.96524867, 35380278.50568732, 35379241.45597246,
       35377194.0539382 , 35374362.74125656, 35373396.01098543,
       35356919.86867634, 35340198.2716566 , 35293598.03307109,
       35248187.70929933, 35227239.22293656, 35205495.42401016,
       35178895.95922533, 35162912.34240986]
popt, R2=(array([-5.89538308e+09,  2.81486018e+09, -4.47734462e+08,  5.91554139e+07]), 0.9677245158601997)
"""