# -*- coding: utf-8 -*-
"""
Created on Thu May 30 07:08:30 2019

@author: Pimprenelle
"""

# -*- coding: utf-8 -*-
"""
Created on Tue May 21 16:26:51 2019

@author: Pimprenelle
"""

from visuMultiStream import *
from intervals import *
from structure import *
from elemMSGraph import *
from multiLayers import *


#A CORRIGER : ECRITURE DES LIENS EN ENTIER...!
t0=0
tend=2*3600+60*9+36
scale = 10
interval = Interval(0,(tend-t0)/scale)
"""
Times are taken in seconds, from 1385982020 to 1386345580.
Measures are taken each 20s.

We suppress 1385982020 to each measure of time and divide by 1000.
"""

typeNode=Aspect("type of node",["caption","character","face","keyword","location"])



class Scene :
    
    def __init__(self,label,interval):
        self.label=label
        self.interval=interval
    
    def giveLabel(self):
        return(self.label)
    def giveInterval(self):
        return(self.interval)

def makeScenes():
    f=open("starWars/SW1/NODES/scene_timestamps.csv","r")
    scenes=SortedCollection([], key=lambda scene : scene.giveLabel())
    n=0
    for line in f :
        if n>1:
            line=line.replace("\"",'')
            tab=line.split(",")
            tab[-1]=tab[-1].rstrip("\n")
            sceneLabel=int(tab[0])
            t1,t2=tab[1],tab[2]
            t1tab,t2tab=t1.split(":"),t2.split(":")
            b=(int(t1tab[0].rstrip("\""))*3600 + int(t1tab[1])*60 + int(t1tab[2]))/scale
            e=(int(t2tab[0])*3600 + int(t2tab[1])*60 + int(t2tab[2]))/scale
            #print("scene",sceneLabel,"int",b,",",e)
            sce=Scene(sceneLabel,Interval(b,e))
            scenes.insert(sce)
        n=n+1
    return(scenes)
        
        


def readNodes(typeN):#marche pour tout sauf caption
    f= open("starWars/SW1/NODES/"+typeN+"_nodes.csv","r")
    n=0
    for line in f :
        if n>0:
            line=line.replace("\"",'')
            tab=line.split(",")
            tab[-1]=tab[-1].rstrip("\n")
            layer=Layer(layerS,[typeN], interval,NodeTList([NodeT(tab[0],IntervalList([interval]),nodeLabel=tab[1])]))
            m.addLayer(layer)
        n=n+1
    f.close()

def readKW():
    f=open("starWars/SW1/NODES/keyword_nodes.csv","r")
    n=0
    l=[]
    dicokw=dict()
    for line in f :
        if n>0:
            line=line.replace("\"",'')
            tab=line.split(",")
            l.append(tab[0])
            dicokw[tab[0]]=tab[1]
        n=n+1
    f.close()
    return(l,dicokw)



def readLinks(typeN1,typeN2,sc):
    fl = open("starWars/SW1/EDGES/"+typeN1+"_"+typeN2+"_edges.csv","r")
    n=0
    for line in fl:
        n=n+1
        if n<10000 and n>1:
            line=line.replace("\"",'')
            tab=line.split(",")
            tab[-1]=tab[-1].rstrip('\n')
            scenelab=int(tab[2])
            int1=(sc[sc.index_label(scenelab)]).giveInterval()
            node1Index=tab[0]
            node2Index=tab[1]
            layer1=[typeN1]
            layer2=[typeN2]
            link=Link((IntervalList([int1])),NodeT(node1Index,IntervalList([interval])),layer1,NodeT(node2Index,IntervalList([interval])),layer2)
            m.addLink(link,tolerance=0.2)
            #link.printLink()

def readLinksInLayer(interval,kw,sc):
    fl = open("starWars/SW1/EDGES/character_keyword_edges.csv","r")
    n=0
    dico=dict()
    asp=Aspect("keyword",kw)
    struct=LayerStruct([asp])
    m=MultiStream(interval,struct,LayerList([]),LinkList([]))
    for line in fl:
        n=n+1
        if n>1:
            line=line.replace("\"",'')
            tab=line.split(",")
            intNode=sc[sc.index_label(int(tab[2]))].giveInterval()
            node = NodeT((tab[0]),IntervalList([intNode]))
            layer=Layer(struct,[tab[1]],interval,NodeTList([node]))
            print("readnode")
            node.printNodeT()
            m.addLayer(layer)
    for l in m.giveLayers().giveLayers():
        for n in l.giveNodesT().giveListOfNodes():
            for k in l.giveNodesT().giveListOfNodes():
                if n.giveNode()<k.giveNode():
                    interval1=n.giveIntervals2()
                    interval2=k.giveIntervals2()
                    interval3= interval1.intersection(interval2)
                    if interval3.duration() != 0:
                        link=Link(interval3,n,l.giveLayerLabel(),k,l.giveLayerLabel())
                        m.addLink(link,tolerance=0.2)
    return(m)
                



def readLinks2(liste,liste2):
    fl = open("lycee/Facebook-known-pairs_data_2013.csv")
    n= 0
    print("readlink2...")
    for line in fl:
        n=n+1
        if n<10000:
            tab=line.split(" ")
            tab[2]=tab[2].rstrip('\n')
            print(tab)
            if tab[2]=='1':
                node1=tab[0]
                node2=tab[1]
                layer1=["facebook",liste2[node1],liste[node1]]
                layer2=["facebook",liste2[node2],liste[node2]]
                I=IntervalList([interval])
                link=Link(I,NodeT(node1,I),layer1,NodeT(node2,I),layer2)
                m.addLink(link)
                print("linkfb")
                #link.printLink()




sc=makeScenes()
kw,dicokw=readKW() 

KW=Aspect("keyword",kw)
struct=LayerStruct([kw])
m=MultiStream(interval,struct,LayerList([]),LinkList([]))

#readNodes("character")

#readLinks("character","keyword",sc)

#m.drawMS("charakw.fig")

print("sc len",sc.__len__())

m1=readLinksInLayer(interval,kw,sc)
#m1.printMS()


print("************************************************")
m1.printMS()
m1.drawMS("starintric.fig")
m2=m1.extractML()
m2.cleanML()
m2.drawML("coucheskw")

matIntric=m2.computeIntricationMatrixBurt()



fichier=open("matriceadjsw","w")
for l in matIntric:
    fichier.write(str(l))
    fichier.write('\n')
fichier.close()

print(valeurPropreMax(matIntric,100))




#m2.drawML()
#m1.drawMS("multiplexSW.fig")

#sc.printsort()
#readNodes("character")
#readNodes("face")
#readNodes("keyword")
#readNodes("location")
#readLinks("character","character",sc)
#m.printMS()
#m.drawMS("sw.fig")

