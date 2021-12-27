# -*- coding: utf-8 -*-
import sys

import pycalculix as pyc
# шлях до gmsh, ccx, cgx
pyc.environment.GMSH=r"d:\Portable\gmsh-4.8.4-Windows64\gmsh.exe"
pyc.environment.CCX=r"d:\Portable\cae_20200725_windows\bin\ccx.exe"
pyc.environment.CGX=r"d:\Portable\cae_20200725_windows\bin\cgx.exe"
model_name = 'thread'
model = pyc.FeaModel(model_name) # модель
model.set_units('mm') # одиниці вимірювання

show_gui = True # показувати графіки

# геометричні параметри з'єднання
l = 30
t1 = 3.5
t2 = 3.5
r0 = 6.5
hh=0.1

part = pyc.Part(model) # деталь

def run():
    # рисувати контури з'єднання
    part.goto(r0, 0) # перейти в точку
    l1=part.draw_line_ax(l) # рисувати лінію вздовж
    l2=part.draw_line_rad(t1) # рисувати лінію поперек
    l3=part.draw_line_rad(t2)
    l4=part.draw_line_ax(-l)
    l5=part.draw_line_rad(-t2)
    l6=part.draw_line_rad(-t1)

    # зазори
    for i in range(15): # 15 отворів
        d=i*2.0 # осьова координата
        w = 1.2 # ширина
        h = hh # висота
        part.goto(10, 0.3+d, holemode=True) # перейти в точку, режим отворів
        part.draw_line_rad(h) # рисувати лінію поперек
        part.draw_line_ax(w) # рисувати лінію вздовж
        part.draw_line_rad(-h)
        part.draw_line_ax(-w)

    for i in range(14): # 14 отворів
        d=i*2.0 # осьова координата
        w = 0.5 # ширина
        h = hh # висота
        part.goto(9.5, 1.5+d, holemode=True) # перейти в точку, режим отворів
        part.draw_line_rad(h) # рисувати лінію поперек
        part.draw_line_ax(w) # рисувати лінію вздовж
        part.draw_line_rad(-h)
        part.draw_line_ax(-w)

    # показати геометрію
    model.plot_geometry(model_name + '_pre', display=show_gui)
    model.view.print_summary() # текстова інформація про геометрію

    model.set_etype('axisym', part) # тип елементів - осесиметричні
    model.set_eshape('tri', 2) # форма елементів - трикутні
    model.mesh(0.1, 'gmsh') # створити сітку за допомогою gmsh
    model.plot_elements(model_name+'_elements', display=show_gui) # показати сітку
    model.view.print_summary()
    model.print_summary()

    # установити матеріал деталей
    mat = pyc.Material('steel')
    mat.set_mech_props(7800, 210*(10**9), 0.3) # властивості матеріалу
    model.set_matl(mat, part)

    # установити навантаження і граничні умови
    #model.set_constr('fix',part.bottom,'x')
    # низ нерухомий
    model.set_constr('fix',[l5[0]],'x')
    model.set_constr('fix',[l5[0]],'y')
    model.set_load("press", [l2[0]], -10e6) # навантаження у верхній частині

    # створити завдання
    prob = pyc.Problem(model, 'struct')

    try:
        prob.solve() # розв'язати
    except:
        pass

    prob.rfile.set_time(1.0) # результати в заданий момент часу

    # рисунки результатів
    fields = 'Sx,Sy,S1,S2,S3,Seqv,ux,uy,utot' # величини для результатів
    fields = fields.split(',')
    for field in fields: # для кожної величини
        fname = model_name+'_'+field
        prob.rfile.nplot(field, fname, display=False) # рисунок

    return prob.rfile.get_nmax('Seqv') # максимальне значення екв. напруження

if __name__=="__main__":
    show_gui = False
    hh=0.1
    print(run())

