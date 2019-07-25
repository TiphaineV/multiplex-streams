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

sg.addLink("M1","F2",2,4)
sg.addLink("F2","F1",4,5)
sg.addLink("F2","F1",7,8)

sg.addTimeLine()
sg.closeFile()
