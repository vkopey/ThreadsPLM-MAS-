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
t1 = 3.5 # товщина стінки ніпеля
t2 = 3.5 # товщина стінки муфти
r0 = 13.0/2 # внутрішній радіус ніпеля
h1=0.5 # висота 1 різьби ніпеля
h2=0.4 # висота 2 різьби ніпеля
h3=0.5 # висота різьби муфти
s1=0.5 # ширина 1 профілю ніпеля
s2=0.8 # ширина 2 профілю ніпеля
k=2.0 # крок
hh=0.1 # радіальний зазор в різьбі
l_=l-2 # довжина різьби

def findLine(lns,**args):
    """Usage:
    list(findLine(lines=model.lines, midpt=(6.5,15)))[0].get_name()
    """
    if 'midpt' in args:
        midpt=args['midpt']
        for l in lines:
            if l.midpt.x==midpt[0] and l.midpt.y==midpt[1]:
                yield l

def run():
    model_name = 'thread'
    model = pyc.FeaModel(model_name) # модель
    model.set_units('mm') # одиниці вимірювання
    part = pyc.Part(model) # деталь ніпеля
    part2 = pyc.Part(model) # деталь муфти
    # рисувати контури з'єднання
    part.goto(r0, 0) # перейти в точку
    l0=part.draw_line_ax(l) # рисувати лінію вздовж
    l1=part.draw_line_rad(t1) # рисувати лінію поперек
    part.draw_line_ax(-1)
    li=0
    while li<l_:
        part.draw_line_rad(-h1)
        part.draw_line_ax(-s1)
        part.draw_line_rad(h1-h2)
        part.draw_line_ax(-(s2-s1))
        part.draw_line_rad(h2)
        part.draw_line_ax(-(k-s2))
        li+=k
    part.draw_line_ax(-(l-1-li))
    l2=part.draw_line_rad(-t1)

    part2.goto(r0+t1+hh, l)
    part2.draw_line_ax(-1)
    li=0
    while li<l_: # for x in range(14):
        part2.draw_line_rad(-h3)
        part2.draw_line_ax(-s2)
        part2.draw_line_rad(h3)
        part2.draw_line_ax(-(k-s2))
        li+=k
    part2.draw_line_ax(-(l-1-li))
    l3=part2.draw_line_rad(t2)
    l4=part2.draw_line_ax(l)
    l5=part2.draw_line_rad(-t2)
    # показати геометрію
    model.plot_geometry(model_name + '_pre', display=show_gui)
    model.view.print_summary() # текстова інформація про геометрію

    # установити матеріал деталей
    mat = pyc.Material('steel')
    youngs=900e6 # сталь 2.1e11, 7800, 0.3
    mat.set_mech_props(910, youngs, 0.4) # властивості матеріалу
    model.set_matl(mat, part)
    model.set_matl(mat, part2)

    ln=model.lines

    # set contact
    factor = 5 # can be between 5 and 50
    kval = youngs*factor

    #Master=[l.get_name() for l in ln[2:86]]
    #Slave=[l.get_name() for l in ln[89:145]]
    # or
    Master=[l.get_name() for l in set(part2.lines)-set([l3[0], l4[0], l5[0]])]
    Slave=[l.get_name() for l in set(part.lines)-set([l0[0], l1[0], l3[0]])]
    model.set_contact_linear(Master, Slave, kval, True)
    # or
    # Master=[l.get_name() for l in ln[92:144+1:4]]
    # Slave=[l.get_name() for l in ln[7:85+1:6]]
    # for (master, slave) in zip(Master, Slave):
    #     model.set_contact_linear(Master, Slave, kval, True)

    model.set_esize(Master+Slave, 0.3)
    model.set_ediv(ln, 10)

    model.set_etype('axisym', part) # тип елементів - осесиметричні
    model.set_etype('axisym', part2)
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
    hh=0.1
    print(run())

    # seq=[]
    # for ll in [8,10,12,14,16,18,20,22,24,26,28]:
    #     l_=ll
    #     seq.append(run())

#hh=range(0,22,2)[165,134,98,66,39,36,36,36,35,35,35]
#l_=[8,10,12,14,16,18,20,22,24,26,28][40,38.4,37.7,37.2,36.8,36.6,36.4,36.3,36.3,36.2,36.2]
#k=[1.4, 1.6, 1.8, 2, 2.2, 2.4, 2.6] [34.9,36.2,36.1,36.2,36.5,36.8,37.1]


