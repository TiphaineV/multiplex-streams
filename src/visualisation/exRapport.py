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


rel = Aspect("type_de_relation",["Collaboration","Combat"])

struct= LayerStruct([mil,rel])

nA = NodeT("A",IntervalList([Interval(4,10)]),nodeLabel="A")
nB = NodeT("B",IntervalList([Interval(0,0)]),nodeLabel="B")
nC = NodeT("C",IntervalList([Interval(0,8)]),nodeLabel="C")
nD = NodeT("D",IntervalList([Interval(0,10)]),nodeLabel="D")

nl=NodeTList([nA,nB,nC,nD])

layer1=Layer(struct,["plaine","Collaboration"],Interval(0,10),nl)

link1= Link(IntervalList([Interval(2,6)]),nD,["plaine","Collaboration"],nC,["plaine","Collaboration"])
link2= Link(IntervalList([Interval(4,8)]),nA,["plaine","Collaboration"],nD,["plaine","Collaboration"])

nA2 = NodeT("A",IntervalList([Interval(4,5), Interval(7,8)]),nodeLabel="A")
nB2 = NodeT("B",IntervalList([Interval(0,10)]),nodeLabel="B")
nC2 = NodeT("C",IntervalList([Interval(3,8)]),nodeLabel="C")
nD2 = NodeT("D",IntervalList([Interval(0,0)]),nodeLabel="D")

nl2=NodeTList([nA2,nB2,nC2,nD2])
layer2=Layer(struct,["foret","Collaboration"],Interval(0,10),nl2)

link3= Link(IntervalList([Interval(4,5),Interval(7,8)]),nA2,["foret","Collaboration"],nB2,["foret","Collaboration"])
link4= Link(IntervalList([Interval(5,8)]),nB2,["foret","Collaboration"],nC2,["foret","Collaboration"])


m=MultiStream(interval,struct,LayerList([layer1,layer2]),LinkList([link1,link2,link3,link4]))

m.drawMS("exrap.fig")

print(m.computeDensity())

print("l",m.computeLengthEm())
o=m.ordreAretes()

for n in ordreAretes():
    n.printNodeT()

mt4=m.cut(Interval(7,7.1))
ml=mt4.extractML()
ml.drawML(names=True)