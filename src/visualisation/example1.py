# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 10:23:10 2019

@author: Pimprenelle
"""

from Drawing import *

sg = Drawing(alpha=0, omega=20, nameFile="exampletest2.fig")

sg.addNode("F1",[(4,10),(12,20)])
sg.addNode("F2",[(10,20)])
sg.addNode("M1",[(0,2),(4,8),(15,19)])
sg.addNode("M2",[(0,10)])

sg.addLink("F1","M1",5,10)
sg.addLink("F1","M1",15,17)
sg.addLink("M1","M2",1,2)
sg.addLink("M1","M2",6,7)


sg.addTimeLine()
sg.closeFile()
