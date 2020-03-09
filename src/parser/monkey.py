#!/usr/bin/env python
# coding: utf-8

# # Drawing multilayer stream graphs

# ## Import the library
# 
# The different elements are on the same folder
# 


from library.Drawing import *


from library.visuMultiStream import *
from library.intervals import *
from library.structure import *
from library.elemMSGraph import *
from library.multiLayers import *


# ## Set the time

t0=0
tend=20
scale = 1
interval = Interval(0,(tend-t0)/scale)


# # Set the layers

mil = Aspect("milieu",["plain","mountain"])
rel = Aspect("type_de_relation",["Collaboration","Fight"])


struct= LayerStruct([mil,rel])


# ## Set the nodes
# - in plain, collaboration

nA = NodeT("F1",IntervalList([Interval(4,10),Interval(12,20)]),nodeLabel="F1",color="orange")
nB = NodeT("F2",IntervalList([Interval(10,20)]),nodeLabel="F2",color="orange")
nC = NodeT("M1",IntervalList([Interval(0,2),Interval(4,8),Interval(15,19)]),nodeLabel="M1",color="orange")
nD = NodeT("M2",IntervalList([Interval(0,10)]),nodeLabel="M2",color="orange")

nl=NodeTList([nA,nB,nC,nD])

layer1=Layer(struct,["plain","Collaboration"],Interval(0,20),nl)


# - mountain, collaboration

nA2 = NodeT("F1",IntervalList([Interval(0,4),Interval(10,12)]),nodeLabel="F1",color=13)
nB2 = NodeT("F2",IntervalList([Interval(0,10)]),nodeLabel="F2",color=13)
nC2 = NodeT("M1",IntervalList([Interval(2,4),Interval(8,15)]),nodeLabel="M1",color=13)
nD2 = NodeT("M2",IntervalList([Interval(10,20)]),nodeLabel="M2",color=13)

nl2=NodeTList([nA2,nB2,nC2,nD2])
layer2=Layer(struct,["mountain","Collaboration"],Interval(0,20),nl2)


# - plain, fight

nA3 = NodeT("F1",IntervalList([Interval(4,10),Interval(12,20)]),nodeLabel="F1",color=19)
nB3 = NodeT("F2",IntervalList([Interval(10,20)]),nodeLabel="F2",color=19)
nC3 = NodeT("M1",IntervalList([Interval(0,2),Interval(4,8),Interval(15,19)]),nodeLabel="M1",color=19)
nD3 = NodeT("M2",IntervalList([Interval(0,10)]),nodeLabel="M2",color=19)

nl3=NodeTList([nA3,nB3,nC3,nD3])
layer3=Layer(struct,["plain","Fight"],Interval(0,20),nl3)


# - mountain, fight

nA4 = NodeT("F1",IntervalList([Interval(0,4),Interval(10,12)]),nodeLabel="F1",color=15)
nB4 = NodeT("F2",IntervalList([Interval(0,10)]),nodeLabel="F2",color=15)
nC4 = NodeT("M1",IntervalList([Interval(2,4),Interval(8,15)]),nodeLabel="M1",color=15)
nD4 = NodeT("M2",IntervalList([Interval(10,20)]),nodeLabel="M2",color=15)

nl4=NodeTList([nA4,nB4,nC4,nD4])
layer4=Layer(struct,["mountain","Fight"],Interval(0,10),nl4)


# ## Set the links

link1= Link(IntervalList([Interval(6,7)]),nD,["plain","Collaboration"],nC,["plain","Collaboration"],color="orange")
link2= Link(IntervalList([Interval(15,17)]),nA,["plain","Collaboration"],nC,["plain","Collaboration"],color="orange")
link3= Link(IntervalList([Interval(1,2),Interval(3,4)]),nA2,["mountain","Collaboration"],nB2,["mountain","Collaboration"],color=13)
linkplus2= Link(IntervalList([Interval(2,4)]),nC2,["mountain","Collaboration"],nB2,["mountain","Collaboration"],color=13)
link22= Link(IntervalList([Interval(11,12),Interval(13,14)]),nC2,["mountain","Collaboration"],nD2,["mountain","Collaboration"],color=13)
link31= Link(IntervalList([Interval(1,2)]),nD3,["plain","Fight"],nC3,["plain","Fight"],color=19)
link32= Link(IntervalList([Interval(5,8)]),nA3,["plain","Fight"],nC3,["plain","Fight"],color=19)
link43= Link(IntervalList([Interval(1,2),Interval(3,4)]),nA4,["mountain","Fight"],nB4,["mountain","Fight"],color=15)
link42= Link(IntervalList([Interval(8,9)]),nC4,["mountain","Fight"],nB4,["mountain","Fight"],color=15)
link43= Link(IntervalList([Interval(4,5)]),nB4,["mountain","Fight"],nC4,["mountain","Fight"],color=15)


# ## Construction of the multilayer stream graph

m=MultiStream(interval,struct,LayerList([layer1,layer2,layer3,layer4]),LinkList([link1,link2,link3,linkplus2,link31,link32,link42,link22,link43]))


# ## Drawing of the multilayer stream graph

# - if your colors are already definded, put colors="def"
# - if not you can set colors="byLayer" (default value) and it will be colored randomly according to the different layers

#m.drawMS("outputs/exraplong3.fig",colors="def")


# ## How to deal with a .fig file

# - reading:
#     - on windows you can download "Winfig"
# - export: 
#     - on windows, winfig doesn't work. But you can now use Linux realy easily on windows (https://docs.microsoft.com/en-us/windows/wsl/install-win10)!
#     - on linux: use `fig2dev [-Lpng/-Lpdf according to the format you want] [your fig file] -> [the new file]`
#     

# The result should like this : example_jupyter.png
