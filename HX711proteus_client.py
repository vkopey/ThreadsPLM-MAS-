# -*- coding: utf-8 -*-

import serial,time
def run():
    ser = serial.Serial(port='COM7', baudrate=9600) # відкрити порт COM
    print(ser.portstr) # перевірити чи порт використовується

    X,Y=[],[]
    for x in range(10):
        y=ser.readline() # читати рядок
        y=float(y)
        X.append(x)
        Y.append(y)
        time.sleep(1) # чекати 1 секунду

    ser.close() # закрити порт
    return X,Y