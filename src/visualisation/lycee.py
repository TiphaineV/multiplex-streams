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
t0=1385982020
scale = 500
interval = Interval(0,(1386345580-t0)/scale)
"""
Times are taken in seconds, from 1385982020 to 1386345580.
Measures are taken each 20s.

We suppress 1385982020 to each measure of time and divide by 1000.
"""

classe=Aspect("annee",["MP","MP*1","MP*2","2BIO1","2BIO2","2BIO3","PSI*","PC","PC*","MP"])
sexe = Aspect("sexe",["F","M","U"])
typeOfRel = Aspect("relation",["face_to_face","facebook","frienship","diaries"])

lycee = LayerStruct([typeOfRel,classe,sexe])


m=MultiStream(interval,lycee,LayerList([]),LinkList([]))

def readNodes():
    f= open("lycee/metadata_2013.txt","r")
    n=0
    liste={}
    liste2=[]
    for line in f :
        n=n+1
        tab=line.split("\t")
        #print(tab)
        #print([tab[1][0],tab[1][1],tab[2][0]])
        layer=Layer(lycee,["face_to_face",tab[1],tab[2][0]],interval,NodeTList([NodeT(tab[0],IntervalList([interval]))]))
        m.addLayer(layer)
        liste[tab[0]]=tab[2][0]
    f.close()
    return(liste,liste2)

def chercherAttribut(liste,numero):
    i=0
    j=len(liste)
    k=0
    while i<j-1:
        k=(i+j)//2
        #print(liste[k][0],"sexe")
        if liste[k][0]>numero:
            j=k
        elif liste[k][0]<numero:
            i=k
        else:
            break
    return(liste[k][1])


def readLinks(liste):
    fl = open("lycee/High-School_data_2013.csv","r")
    n=0
    for line in fl:
        n=n+1
        if n<100000:
            tab=line.split(" ")
            tab[4]=tab[4].rstrip('\n')
            int1=Interval((int(tab[0])-t0)/scale,(int(tab[0])+20-t0)/scale)
            node1=tab[1]
            node2=tab[2]
            c1=tab[3]
            c2 = tab[4]
            layer1=["face_to_face",c1,liste[node1]]
            layer2=["face_to_face",c2,liste[node2]]
            link=Link((IntervalList([int1])),NodeT(node1,IntervalList([interval])),layer1,NodeT(node2,IntervalList([interval])),layer2)
            m.addLink(link,tolerance=0.2)
            #link.printLink()


liste,liste2 = readNodes()
readLinks(liste)
#m.printMS()
#m.drawMS(nameFile2="lycee.fig")
m2=m.extractLayers([["face_to_face","MP","F"],["face_to_face","MP","M"],["face_to_face","MP*1","M"],["face_to_face","MP*1","F"]])
#m2.drawMS(nameFile2="ftfMPF.fig",colors="random")
ml=m2.multit(16.)
ml.drawML()
print("drax")
m3=m2.extractML()
m3.drawML()
print(m.computeDensity())
