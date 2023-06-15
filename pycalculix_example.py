# -*- coding: utf-8 -*-
import sys

import pycalculix as pyc
# шлях до gmsh, ccx, cgx
pyc.environment.GMSH=r"d:\Portable\gmsh-4.8.4-Windows64\gmsh.exe"
pyc.environment.CCX=r"d:\Portable\cae_20200725_windows\bin\ccx.exe"
pyc.environment.CGX=r"d:\Portable\cae_20200725_windows\bin\cgx.exe"

show_gui = True # показувати графіки

# геометричні параметри з'єднання
l = 30 # довжина
t = 3.5 # товщина стінки
r = 5.0 # внутрішній радіус

def run(name=''):
    model_name = 'thread'+name
    model = pyc.FeaModel(model_name) # модель
    model.set_units('mm') # одиниці вимірювання
    part = pyc.Part(model) # деталь
    # рисувати контури деталі
    part.goto(r, 0) # перейти в точку
    l0=part.draw_line_ax(l) # рисувати лінію вздовж
    l1=part.draw_line_rad(t) # рисувати лінію поперек
    l2=part.draw_line_ax(-l)
    l3=part.draw_line_rad(-t)

    # показати геометрію
    model.plot_geometry(model_name + '_pre', display=show_gui)
    model.view.print_summary() # текстова інформація про геометрію

    # установити матеріал деталей
    mat = pyc.Material('plastic')
    youngs=900e6 # сталь 2.1e11, 7800, 0.3
    mat.set_mech_props(910, youngs, 0.4) # властивості матеріалу
    model.set_matl(mat, part)

    ln=model.lines
    model.set_etype('axisym', part) # тип елементів - осесиметричні
    model.set_eshape('tri', 2) # форма елементів - трикутні tri, чотирикутні quad
    model.mesh(0.1, 'gmsh') # створити сітку за допомогою gmsh
    model.plot_elements(model_name+'_elements', display=show_gui) # показати сітку
    model.view.print_summary()
    model.print_summary()

    # установити навантаження і граничні умови
    #model.set_constr('fix',[ln[0]],'x')
    # низ нерухомий
    model.set_constr('fix',[l3[0]],'x')
    model.set_constr('fix',[l3[0]],'y')
    model.set_load("press", [l1[0]], -5e6) # навантаження у верхній частині

    # створити завдання
    prob = pyc.Problem(model, 'struct')

    try:
        prob.solve() # розв'язати
    except:
        print('solver error!')

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
    #print(run())

    Y=[]
    for t in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]:
        Y.append(run())



