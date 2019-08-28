# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 10:23:10 2019

@author: Pimprenelle
"""

from Drawing import *

sg = Drawing(alpha=0, omega=10, nameFile="exampletest.fig")

sg.addNode("F1",[(3,10)])
sg.addNode("F2",[(1,5),(6,9)])
sg.addNode("M1",[(0,5)])
sg.addNode("M2",[(0,10)])

sg.addLink("M1","F2",2,4)
sg.addLink("F2","F1",4,5)
sg.addLink("F2","F1",7,8)
sg.addLink("M1","M2",3,5)
sg.addLink("M1","F1",3.5,5,curving=0.20,height=0.60)

sg.addTimeLine()
sg.closeFile()
