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

sg.addNode("F1",[(0,10)])
sg.addNode("F2",[(0,8)])
sg.addNode("M1",[(4,10)])

sg.addLink("F1","F2",2,6)
sg.addLink("F2","M1",4,8)

sg.addTimeLine()
sg.closeFile()





t0=0
tend=10
scale = 1
interval = Interval(0,(tend-t0)/scale)

mil = Aspect("milieu",["plain","mountain"])


rel = Aspect("type_de_relation",["Collaboration","fight"])

struct= LayerStruct([mil,rel])

nA = NodeT("F1",IntervalList([Interval(4,10)]),nodeLabel="F1")
nB = NodeT("F2",IntervalList([Interval(0,0)]),nodeLabel="F2")
nC = NodeT("M1",IntervalList([Interval(0,2),Interval(4,8)]),nodeLabel="M1")
nD = NodeT("M2",IntervalList([Interval(0,10)]),nodeLabel="M2")

nl=NodeTList([nA,nB,nC,nD])

layer1=Layer(struct,["plain","Collaboration"],Interval(0,10),nl)

link1= Link(IntervalList([Interval(1,2),Interval(6,7)]),nD,["plain","Collaboration"],nC,["plain","Collaboration"])
link2= Link(IntervalList([Interval(5,8)]),nA,["plain","Collaboration"],nC,["plain","Collaboration"])
#linkplus= Link(IntervalList([Interval(4,8)]),nA,["plain","Collaboration"],nB,["plain","Collaboration"])


nA2 = NodeT("F1",IntervalList([Interval(0,4)]),nodeLabel="F1")
nB2 = NodeT("F2",IntervalList([Interval(0,10)]),nodeLabel="F2")
nC2 = NodeT("M1",IntervalList([Interval(2,4),Interval(8,10)]),nodeLabel="M1")
nD2 = NodeT("M2",IntervalList([Interval(0,0)]),nodeLabel="M2")

nl2=NodeTList([nA2,nB2,nC2,nD2])
layer2=Layer(struct,["mountain","Collaboration"],Interval(0,10),nl2)

link3= Link(IntervalList([Interval(1,2),Interval(3,4)]),nA2,["mountain","Collaboration"],nB2,["mountain","Collaboration"])
linkplus2= Link(IntervalList([Interval(2,3),Interval(8,9)]),nC2,["mountain","Collaboration"],nB2,["mountain","Collaboration"])
interlink= Link(IntervalList([Interval(9,10)]),nC,["mountain","Collaboration"],nA2,["plain","Collaboration"])
#link4= Link(IntervalList([Interval(5,8)]),nD2,["mountain","Collaboration"],nC2,["mountain","Collaboration"])


m=MultiStream(interval,struct,LayerList([layer1,layer2]),LinkList([link1,link2,link3,linkplus2,interlink]))

m.drawMS("exrap.fig")

print(m.computeDensity())

print("l",m.computeLengthEm())
o=m.ordreAretes()

for n in o:
    n.printNodeT()

mt4=m.cut(Interval(7,7.1))
ml=mt4.extractML()
ml.drawML(names=True)

matriceIntrication=m.comupteIntricationMatrixBurtMS()
print(valeurPropreMax(matriceIntrication,100))

print(m.elemLayerDensitiesMat(mil))