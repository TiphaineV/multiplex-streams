# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 11:59:41 2019

@author: Pimprenelle
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 09:56:13 2019

@author: Pimprenelle
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 00:46:20 2019

@author: Pimprenelle
"""


from Drawing import *


from visuMultiStream import *
from intervals import *
from structure import *
from elemMSGraph import *
from multiLayers import *

sg = Drawing(alpha=0, omega=10, nameFile="exampleRapport.fig")

sg.addNode("A",[(0,10)])
sg.addNode("B",[(0,8)])
sg.addNode("C",[(4,10)])

sg.addLink("A","B",2,6)
sg.addLink("B","C",4,8)

sg.addTimeLine()
sg.closeFile()





t0=0
tend=10
scale = 1
interval = Interval(0,(tend-t0)/scale)

mil = Aspect("milieu",["plaine","foret"])

struct= LayerStruct([mil])

nA = NodeT("A",IntervalList([Interval(4,10)]),nodeLabel="A")
nB = NodeT("B",IntervalList([Interval(0,0)]),nodeLabel="B")
nC = NodeT("C",IntervalList([Interval(0,8)]),nodeLabel="C")
nD = NodeT("D",IntervalList([Interval(0,10)]),nodeLabel="D")

nl=NodeTList([nA,nB,nC,nD])

layer1=Layer(struct,["plaine"],Interval(0,10),nl)

link1= Link(IntervalList([Interval(0,4)]),nA,["plaine"],nB,["plaine"])
link2= Link(IntervalList([Interval(1,5)]),nA,["plaine"],nC,["plaine"])
link3= Link(IntervalList([Interval(4,8)]),nA,["plaine"],nD,["plaine"])

nE = NodeT("A",IntervalList([Interval(4,10)]),nodeLabel="A")
nF = NodeT("B",IntervalList([Interval(0,0)]),nodeLabel="B")
nG = NodeT("C",IntervalList([Interval(0,8)]),nodeLabel="C")
nH = NodeT("D",IntervalList([Interval(0,10)]),nodeLabel="D")
nI = NodeT("D",IntervalList([Interval(0,10)]),nodeLabel="I")


nl2=NodeTList([nE,nF,nG,nH])

layer2=Layer(struct,["foret"],Interval(0,10),nl2)

link4= Link(IntervalList([Interval(0,5)]),nE,["foret"],nF,["foret"])
link5= Link(IntervalList([Interval(1,5)]),nE,["foret"],nG,["foret"])
link6= Link(IntervalList([Interval(4,8)]),nE,["foret"],nH,["foret"])


link7=Link(IntervalList([Interval(0,10)]),nA,["plaine"],nE,["foret"])

m=MultiStream(interval,struct,LayerList([layer1,layer2]),LinkList([link1,link2,link3,link4,link5,link6,link7]))

print("l",m.computeLengthEm(layer=["foret"]))
o=m.ordreAretes(layer=["foret"])

print("o",o)
for n in o:
    n.printNodeT()


m.drawMS("exordre2.fig")

#print(m.computeDensity())



