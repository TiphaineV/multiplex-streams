# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 10:23:10 2019

@author: Pimprenelle
"""

from Drawing import *

sg = Drawing(alpha=0, omega=10, nameFile="exampletest.fig")

sg.addNode("R1,U1,M1",[(3,10)])
sg.addNode("R2,U1,Math")
sg.addNode("R1,U1,CS")



sg.addTimeLine()
sg.closeFile()
