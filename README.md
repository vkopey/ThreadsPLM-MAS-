# ThreadsPLM-MAS-
## Educational multi-agent PLM system for threaded connections 
Authors: Kopei V.B.(vkopey@gmail.com, volodymyr.kopey@nung.edu.ua), Onysko O.R.(onysko.oleg@gmail.com, oleh.onysko@nung.edu.ua)
## Навчальна мультиагентна PLM-система для підтримки життєвого циклу різьбових з’єднань
Автори: Копей В. Б. , Онисько О. Р. 
## Install:
1. Download and unpack [Python-3.8.9x64](https://sourceforge.net/projects/portable-python/files/Portable%20Python%203.8/Portable%20Python-3.8.9%20x64.exe/download)
2. Install Python packages with Console-Launcher.exe and PIP:
```
pip install https://download.lfd.uci.edu/pythonlibs/archived/numpy-1.22.4+mkl-cp38-cp38-win_amd64.whl
pip install https://download.lfd.uci.edu/pythonlibs/archived/scipy-1.7.3-cp38-cp38-win_amd64.whl
pip install https://download.lfd.uci.edu/pythonlibs/archived/matplotlib-3.5.2-cp38-cp38-win_amd64.whl
pip install notebook==6.4.6
pip install pycalculix==1.1.4
pip install pyserial==3.5
pip install ray==2.2.0
pip install sympy==1.10.1
```
3. Download and unpack [gmsh-4.8.4-Windows64](https://gmsh.info/bin/Windows/gmsh-4.8.4-Windows64.zip)
4. Download and unpack [CalculiX Advanced Environment v0.8.0](https://github.com/calculix/cae/releases/download/v0.8.0/cae_20200725_windows.zip)
5. Edit the path to gmsh.exe, ccx.exe, cgx.exe in mypycalculix.py
6. Edit the path to jupyter-notebook.exe in ThreadPLM_ray.bat 
7. For SCADA actors using you need HX711.pdsprj and:
a) Proteus 8.13;
b) Null-modem emulator (com0com)
(https://sourceforge.net/projects/com0com/files/com0com/3.0.0.0/com0com-3.0.0.0-i386-and-x64-signed.zip/download). Run setupg.exe and create the virtual pair COM6-COM7.

## Usage:
1. Run ThreadPLM_ray.bat
2. Cells/Run all 

## Citing:
If you use ThreadsPLM-MAS- please cite the following reference in your work (books, articles, reports, etc.):

Kopei, V.; Onysko, O.; Barz, C.; Dašić, P.; Panchuk, V. Designing a Multi-Agent PLM System for Threaded Connections Using the Principle of Isomorphism of Regularities of Complex Systems. Machines 2023, 11, 263. https://doi.org/10.3390/machines11020263
