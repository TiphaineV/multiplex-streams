# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 10:42:31 2019

@author: Pimprenelle
"""


from Drawing import *


from visuMultiStream import *
from intervals import *
from structure import *
from elemMSGraph import *
from multiLayers import *


kwlist=["E","C","D","L"]


keyword=Aspect("keywords",kwlist)

keywordst=LayerStruct([keyword])

noeuds=NodeList([Node("A1"),Node("A2"),Node("A3"),Node("A4")])

mlgraph=MultiLayer(keywordst,LayerNTList([]),LinkNTList([]))

for k in kwlist:
    lay1=LayerNT(keywordst,k,noeuds,checkCorrectL="True", checkCorrectN="True")
    mlgraph.addLayer(lay1)

print("linkE")
linksE=LinkNTList([LinkNT(Node("A1"),"E",Node("A3"),"E"),LinkNT(Node("A2"),"E",Node("A1"),"E"),LinkNT(Node("A2"),"E",Node("A3"),"E")])
print("LinkC")
linksC=LinkNTList([LinkNT(Node("A2"),"C",Node("A1"),"C"),LinkNT(Node("A2"),"C",Node("A3"),"C"),LinkNT(Node("A1"),"C",Node("A3"),"C")])

linksD=LinkNTList([LinkNT(Node("A1"),"D",Node("A4"),"D"),LinkNT(Node("A4"),"D",Node("A3"),"D"),LinkNT(Node("A1"),"D",Node("A3"),"D")])

linksL=LinkNTList([LinkNT(Node("A3"),"L",Node("A4"),"L")])

mlgraph.addLinks(linksE)

mlgraph.addLinks(linksC)
mlgraph.addLinks(linksD)
mlgraph.addLinks(linksL)

mlgraph.drawML(names=True)
m=mlgraph.computeIntricationMatrixBurt()

print(m)

print(valeurPropreMax(m,100))
