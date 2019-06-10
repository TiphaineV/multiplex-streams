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

sg.addNode("MB",[(0,10)])
sg.addNode("YYA",[(0,8)])
sg.addNode("MAP",[(4,10)])

sg.addLink("MB","YYA",2,6)
sg.addLink("YYA","MAP",4,8)

sg.addTimeLine()
sg.closeFile()


t0=0
tend=10
scale = 1
interval = Interval(0,(tend-t0)/scale)

conf = Aspect("conf",["ECCS13","Workshop in Oxford","NetSci13"])


rel = Aspect("rel",["Talk to each other","Went to a talk by the other"])

struct= LayerStruct([conf,rel])

nmap = NodeT("0",IntervalList([Interval(4,10)]),nodeLabel="MAP")
nmb = NodeT("1",IntervalList([Interval(0,10)]),nodeLabel="MB")
nyya = NodeT("2",IntervalList([Interval(0,8)]),nodeLabel="YYA")
nac = NodeT("3",IntervalList([Interval(0,0)]),nodeLabel="AC")

nl=NodeTList([nmap,nmb,nyya,nac])

layer1=Layer(struct,["ECCS13","Talk to each other"],Interval(0,10),nl)

link1= Link(IntervalList([Interval(2,6)]),nmb,["ECCS13","Talk to each other"],nyya,["ECCS13","Talk to each other"])
link2= Link(IntervalList([Interval(4,8)]),nyya,["ECCS13","Talk to each other"],nmap,["ECCS13","Talk to each other"])

nmap2 = NodeT("0",IntervalList([Interval(4,5), Interval(7,8)]),nodeLabel="MAP")
nac2 = NodeT("3",IntervalList([Interval(0,10)]),nodeLabel="AC")
nyya2 = NodeT("2",IntervalList([Interval(3,8)]),nodeLabel="YYA")
nmb2 = NodeT("1",IntervalList([Interval(0,0)]),nodeLabel="MB")

nl2=NodeTList([nmap2,nac2,nyya2,nmb2])
layer2=Layer(struct,["Workshop in Oxford","Talk to each other"],Interval(0,10),nl2)

link3= Link(IntervalList([Interval(4,5),Interval(7,8)]),nmap2,["Workshop in Oxford","Talk to each other"],nac2,["Workshop in Oxford","Talk to each other"])
link4= Link(IntervalList([Interval(5,8)]),nac2,["Workshop in Oxford","Talk to each other"],nyya2,["Workshop in Oxford","Talk to each other"])


m=MultiStream(interval,struct,LayerList([layer1,layer2]),LinkList([link1,link2,link3,link4]))

m.drawMS("exrap.fig")