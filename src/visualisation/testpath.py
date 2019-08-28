# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 10:08:16 2019

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




t0=0
tend=10
scale = 1
interval = Interval(0,(tend-t0)/scale)

mil = Aspect("milieu",["plaine"])

struct= LayerStruct([mil])

nA = NodeT("A",IntervalList([Interval(0,10)]),nodeLabel="A")
nB = NodeT("B",IntervalList([Interval(0,10)]),nodeLabel="B")
nC = NodeT("C",IntervalList([Interval(0,10)]),nodeLabel="C")
nD = NodeT("D",IntervalList([Interval(0,10)]),nodeLabel="D")

nl=NodeTList([nA,nB,nC,nD])

layer1=Layer(struct,["plaine"],Interval(0,10),nl)

link1= Link(IntervalList([Interval(1,2),Interval(8,9)]),nA,["plaine"],nB,["plaine"])
link2= Link(IntervalList([Interval(3,4),Interval(6,7)]),nB,["plaine"],nC,["plaine"])
link3= Link(IntervalList([Interval(1,2),Interval(8,9)]),nC,["plaine"],nD,["plaine"])

link4= Link(IntervalList([Interval(1,2),Interval(8,9)]),nB,["plaine"],nA,["plaine"])
link5= Link(IntervalList([Interval(3,4),Interval(6,7)]),nC,["plaine"],nB,["plaine"])
link6= Link(IntervalList([Interval(1,2),Interval(8,9)]),nD,["plaine"],nC,["plaine"])

nodes=["A","B","C","D"]


m=MultiStream(interval,struct,LayerList([layer1]),LinkList([link1,link2,link3]),nodes=nodes)




#m.drawMS("expath.fig")

em=m.giveLinks()
s=em.giveListForForemost()
t=m.foremostPath("A",s,t0=2)
#print(m.computeDensity())

s2=m.giveListForLastDept()

t2=m.lastDeptPath("C",s2,t0=6)

wind=m.findWindows("C",to=5)

m.enumShortestPath("A","B")

t=m.avionsSuivants("A",0,5)

m1,m2=m.calculMatriceProbaTransition(0,5)

print(np.array(m1))

for i in range(len(m1)):
    for j in range(len(m1)):
        print(m1[i][j]*0.9)
        m1[i][j]=(m1[i][j]*0.9)
        m1[i][j]=m1[i][j]+0.1/4

m1=np.transpose(np.array(m1))
valp,vectp=valeurPropreMax(m1,100)
#pb= liste d"intervalles vides


