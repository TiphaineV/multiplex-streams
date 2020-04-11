# Datas
# Datas are imported from SocioPattern website : http://www.sociopatterns.org/datasets/high-school-contact-and-friendship-networks/

import functools
import types

from library.visuMultiStream import *
from library.intervals import *
from library.structure import *
from library.elemMSGraph import *
from library.multiLayers import *
from library.matrices import *

'''
Note) Function definitions are mostly compatible with Pimprenelle's work.  However, this version removes implicit references to a global variable "m" and adds a parameter "m" that explicitly takes a MS-graph of consideration.  -- kw
'''

'''
Times are taken in seconds, from 1385982020 to 1386345580.
Measures are taken each 20s.

We suppress 1385982020 to each measure of time and divide by 1000.
'''

# Build the multilayer stream graph

t0, t1 = 1385982020, 1386345580
scale = 500

interval = Interval(0, (t1 - t0)/scale)

# We build the multilayer graph :

classe    = Aspect("annee",    ["MP", "MP*1", "MP*2", "PSI*", "PC", "PC*", "2BIO1", "2BIO2", "2BIO3"])
sexe      = Aspect("sexe",     ["F", "M", "U"])
typeOfRel = Aspect("relation", ["face_to_face", "facebook", "friendship", "diaries"])

LYCEE = LayerStruct([typeOfRel, classe, sexe])

## Read the nodes (students). 

def set_prefix(path):
    global _prefix_
    _prefix_ = path

def readNodes(m, typen=["face_to_face"]):
    
    with open("data/lycee/metadata_2013.txt","r") as f:
        n=0
        liste={}
        liste2={}
        for line in f :
            n=n+1
            tab=line.split("\t")
            for ty in typen :
                layer=Layer(LYCEE, [ty,tab[1],tab[2][0]],interval,NodeTList([NodeT(tab[0],IntervalList([interval]))]))
                m.addLayer(layer)
            liste[tab[0]]=tab[2][0]
            liste2[tab[0]]=tab[1]
    return(liste,liste2)


## Read the links face to face

# Some informations are missing (sex and class), they are in liste1, liste2.

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

def readLinks(m, liste):
    with open("data/lycee/High-School_data_2013.csv","r") as fl:
        n=0
        ni=[0]
        ti=[0]
        for line in fl:
            n=n+1
            if n<200000:
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
                t=int1.begining()
                if ti[len(ti)-1]==t:
                    ni[len(ti)-1]=ni[len(ti)-1]+1
                else:
                    ti.append(t)
                    ni.append(1)
    return(ti,ni)


## Read the links facebook

def readLinks2(m, liste,liste2):
    with open("data/lycee/Facebook-known-pairs_data_2013.csv") as fl:
        n= 0
        print("readlink2...", flush=True)
        for line in fl:
            n=n+1
            if n<1000000000000:
                tab=line.split(" ")
                tab[2]=tab[2].rstrip('\n')
                #print(tab)µ
                if tab[2]=='1':
                    node1=tab[0]
                    node2=tab[1]
                    layer1=["facebook",liste2[node1],liste[node1]]
                    layer2=["facebook",liste2[node2],liste[node2]]
                    I=IntervalList([interval])
                    link=Link(I,NodeT(node1,I),layer1,NodeT(node2,I),layer2)
                    m.addLink(link)
                    #print("linkfb")
                    #link.printLink()


## Read the links friendship

def readLinks3(m, liste,liste2):
    with open("data/lycee/Friendship-network_data_2013.csv") as fl:
        n=0
        print("readlink3...", flush=True)
        for line in fl:
            n=n+1
            if n<1000000000000:
                tab=line.split(" ")
                tab[1]=tab[1].rstrip('\n')
                node1=tab[0]
                node2=tab[1]
                layer1=["friendship",liste2[node1],liste[node1]]
                layer2=["friendship",liste2[node2],liste[node2]]
                I=IntervalList([interval])
                link=Link(I,NodeT(node1,I),layer1,NodeT(node2,I),layer2)
                m.addLink(link)
        print("link3 done", flush=True)

# Study the multilayer stream graph :

def layerWithCommonPoint(layerStruct,aspect,elemLayer):
    liste=[[]]
    i=0
    ind=0
    for asp in layerStruct.giveAspects() :
        if asp.nameAspect()==aspect :
            i=ind
        else:
            ind=ind+1
    j=0
    for asp in layerStruct.giveAspects() :
        for k in range(len(liste)-1,-1,-1):
            a=liste.pop(k)
            for elemLayeri in asp.giveElemLayer():
                if j==i:
                    if elemLayeri==elemLayer:
                         a.append(elemLayeri)
                         liste.append(a)
                         a=a.copy()
                         a.pop()
                else:
                    a.append(elemLayeri)
                    liste.append(a)
                    a=a.copy()
                    a.pop()
        j=j+1
    return(liste)

Lycee = MultiStream(interval, LYCEE, LayerList([]), LinkList([]))
def _extract_(self, **params):
    print(params.items())
    functools.reduce(lambda key, spec: self.extractLayers(layerWithCommonPoint(LYCEE, key, spec)), params.items())
Lycee.extract = types.MethodType(_extract_, Lycee)
