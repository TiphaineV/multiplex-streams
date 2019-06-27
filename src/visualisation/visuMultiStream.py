from Drawing import *

from sortedcollection import *
from random import uniform
from intervals import *
from structure import *
from elemMSGraph import *
from multiLayers import *
import numpy as np
import matplotlib.pyplot as plt

"""
Final structure : MultiStream
"""


class MultiStream :
    """
    class MultiStream :
    ====

    :type T: interval
    :type layerStruct: LayerStruct
    :type layers: LayerList
    :type em: LinkList

    """

    def __init__(self,T,layerStruct,layers,em):
        #todo : coherence checks !!
        self.T=T
        self.layerStruct=layerStruct
        self.layers = layers #todo : create empty layer with good structure, then add the layers in it.
        self.em = em

    def interval(self):
        return(self.T)
    def giveLayers(self):
        return(self.layers)
    def addLayer(self, layer):
        '''
        function addLayer(layer)
        ===
        from class MultiStream :
        ----

        used to :
        - add simple layer without nodes
        - add node in a layer
        '''
        self.layers.addLayer(layer)
    def addLink(self,link,tolerance=0):
        #to do : check intervals coherence
        self.em.addLink(link,tolerance)
    def giveLinks(self):
        return(self.em)
    def printNodes(self):
        print("layers")
        for l in self.layers.giveLayers():
            l.printLayer()
    def printMS(self):
        print("T:",self.T.intervalToString() )
        print("structure")
        print("layers and nodes")
        self.layers.printLayerList()
        print("EM")
        for e in self.em.giveListOfLinks():
            e.printLink()
    def drawMS(self,nameFile2="default.fig",colors="byLayer",neglect=-1,ordonne=False):
        """
            function drawMS :
            =====
            class MultiStream
            ---
            
            :type nameFile2: string
            :type colors: string
            :type neglect: int
            :type ordonne: boolean
            
            draw the mulitlayer into a .fig file.  (name of the file nameFile2)
            If colors = byLayers, the link are colored the same color in each layer, black interlayer.
            If neglect >0, we don't draw the link that last less than neglect.
            If ordonne=true, optimizes the order of the nodes inside each layer
        """
        f=Drawing(alpha=self.T.begining(),omega=self.T.end(),nameFile=nameFile2)
        if colors=="byLayer":
            color={}
        for i in range(self.layers.length()) :
            #f.printLayer() : todo
            lay=self.layers.giveLayer(i).giveLayerLabel()
            newlay=1
            if ordonne==True :
                ordre=self.ordreAretes(lay)
            if colors=="byLayer":
                col=7
                while col==7:
                    col=int(uniform(1,30))
                color[str(lay)]=col
            if ordonne==True :
                for j in ordre:
                    times=[]
                    for k in j.giveIntervals():
                        times.append((k.begining(),k.end()))
                    f.addNode(str(j.giveNode()),times=times,layer=str(lay),newLayer=newlay,write=j.giveNodeLabel())
                    newlay=0
            else :
                for j in self.layers.giveLayer(i).giveNodesT().giveListOfNodes():
                    times=[]
                    for k in j.giveIntervals():
                        times.append((k.begining(),k.end()))
                    f.addNode(str(j.giveNode()),times=times,layer=str(lay),newLayer=newlay,write=j.giveNodeLabel())
                    newlay=0
        for j in self.em.giveListOfLinks():
            for inte in j.giveIntervals():
                b=inte.begining()
                e=inte.end()
                u=str(j.giveNodes()[0].giveNode())
                v=str(j.giveNodes()[1].giveNode())
                lay1=str(j.giveLayers()[0])
                lay2=str(j.giveLayers()[1])
                if colors=="byLayer":
                    if lay1==lay2 : 
                        c = color[lay1]
                    else:
                        c=0
                else :
                    c=int(uniform(1,30))
                if neglect<0:
                    f.addLink( u, v, b, e, layer1=lay1, layer2=lay2,color=c)
                elif e-b>neglect:
                    f.addLink( u, v, b, e, layer1=lay1, layer2=lay2,color=c)
            f.addTimeLine()
        f.closeFile()
    
    
    def extractLayers(self,layerLabels):
        """
        function extractLayers 
        ====
        class MultiStream
        ---
        
        :type layerLabels: list[layerLabel]
        
        creates a MS with nodes and links in the list of layerLabels.
        """
        multi=MultiStream(self.T,self.layerStruct,LayerList([]),LinkList([]))
        for layerLabel in layerLabels:
            layer=self.layers.giveLayerFromLabel(layerLabel)
            if layer !=0:
                multi.addLayer(layer)
        for e in self.em.giveListOfLinks():
            lay1=e.giveLayers()[0]
            lay2=e.giveLayers()[1]
            if lay1 in layerLabels:
                if lay2 in layerLabels:
                    multi.addLink(e)
        return(multi)
    
    def interLayers(self,layerLabels1,layerLabels2):
        """
        function interLayers 
        ====
        class MultiStream
        ---
        
        :type layerLabels1: list[layerLabel]
        :type layerLabels2: list[layerLabel]
        
        creates a MS with nodes and links in the list of layerLabels.
        """
        multi=MultiStream(self.T,self.layerStruct,LayerList([]),LinkList([]))
        for layerLabel in layerLabels1:
            layer=self.layers.giveLayerFromLabel(layerLabel)
            if layer !=0:
                multi.addLayer(layer)
        for layerLabel in layerLabels2:
            layer=self.layers.giveLayerFromLabel(layerLabel)
            if layer !=0:
                multi.addLayer(layer)
        for e in self.em.giveListOfLinks():
            lay1=e.giveLayers()[0]
            lay2=e.giveLayers()[1]
            if lay1 in layerLabels1:
                if lay2 in layerLabels2:
                    multi.addLink(e)
            elif lay1 in layerLabels2:
                if lay2 in layerLabels1:
                    multi.addLink(e)
        return(multi)
        
        
    
    def multit(self,t):
        """
        function multit 
        ===
        class MultiStream
        --
        
        :type t: float
        
        takes a picture of the multi stream at t and return the multilayer associated
        """
        print("multit")
        if self.T.isIn(t):#on vérifie que le temps t demandé est bien dans l'intervalle d'étude
            multi=MultiLayer(self.layerStruct,LayerNTList([]),LinkNTList([]))
            for i in range(self.layers.length()) : 
                lay=self.layers.giveLayer(i).giveLayerLabel() 
                inte = self.layers.giveLayer(i).giveInterval() 
                if inte.isIn(t):#on vérifie que la layer existe au temps t
                    nodel = []
                    for j in self.layers.giveLayer(i).giveNodesT().giveListOfNodes():#on sélectionne les noeuds apparaissant à t
                        intenode=j.giveIntervals2()
                        #intenode.printIntervals()
                        if intenode.isInList(t):
                            nodel.append(Node(j.giveNode()))
                    multi.addLayer(LayerNT(self.layerStruct,lay,NodeList(nodel)))
            for j in self.em.giveListOfLinks():
                if j.giveIntervals2().isInList(t):
                    tab=j.giveLabel()
                    multi.addLink(LinkNT(Node(tab[0]),tab[2],Node(tab[1]),tab[3]))
        else: 
            print(t,"is not accepted")
        return(multi)
        
        
    def extractML(self):
        """
        function extractML
        ====
        class MultiStream
        --
        
        create a multiLayer with all the nodes and links in MultiStream
        """
        print("extracting...")
        multi=MultiLayer(self.layerStruct,LayerNTList([]),LinkNTList([]))
        for i in range(self.layers.length()):
            nodel = []
            lay=self.layers.giveLayer(i).giveLayerLabel() 
            print("layer",lay)
            for j in self.layers.giveLayer(i).giveNodesT().giveListOfNodes():#on sélectionne les noeuds apparaissant à t
                nodel.append(Node(j.giveNode()))
            nu=NodeList(nodel)
            multi.addLayer(LayerNT(self.layerStruct,lay,NodeList(nodel)))
        for j in self.em.giveListOfLinks():
            tab=j.giveLabel()
            multi.addLink(LinkNT(Node(tab[0]),tab[2],Node(tab[1]),tab[3]))    
        return(multi)
    
    def computeDensity(self,typeOfMultiStream="normal"):
        """
        function computeDensity
        ===
        class MultiStream
        ---
        
        :type typeOfMultiStream: str
        
        compute the density of the graph . The length of all links/ the lenght of all possible links.
        """
        durationLinks=0
        durationNodes=0
        for j in self.em.giveListOfLinks():
            durationLinks=durationLinks+j.giveIntervals2().duration()
        for i in self.layers.giveLayers():
            for j in self.layers.giveLayers():
                for k in i.giveNodesT().giveListOfNodes():
                    for l in j.giveNodesT().giveListOfNodes():
                        if i!=j or k!=l:
                            durationNodes=durationNodes+k.giveIntervals2().intersection(l.giveIntervals2()).duration()
        return(2*durationLinks/durationNodes)
    
    def computeDensityBiparti(self,layerlabels1,layerlabels2):
        """
        function computeDensity
        ===
        class MultiStream
        ---
        
        :type typeOfMultiStream: str
        :type layerLabels1: list[layerLabels]
        :type layerLabels2: list[layerLabels]
        
        compute the density of the bipartite graph . The length of all links/ the lenght of all possible links.
        """
        durationLinks=0
        durationNodes=0
        for j in self.em.giveListOfLinks():
            durationLinks=durationLinks+j.giveIntervals2().duration()
        for i in self.layers.giveLayers():
            for j in self.layers.giveLayers():
                if (i.giveLayerLabel() in layerlabels1 and j.giveLayerLabel() in layerlabels2):
                    for k in i.giveNodesT().giveListOfNodes():
                        for l in j.giveNodesT().giveListOfNodes():
                            durationNodes=durationNodes+k.giveIntervals2().intersection(l.giveIntervals2()).duration()
        return(durationLinks/durationNodes)
    
    
    def cut(self,interval):
        m2=MultiStream(interval,self.layerStruct, LayerList([]),LinkList([]))
        for lay in self.layers.giveLayers() :
            int2= lay.giveInterval().intersection(interval)
            if int2 != Interval(0,0):
                m2.addLayer(Layer(self.layerStruct,lay.giveLayerLabel(),int2,NodeTList([])))
                for n in lay.giveNodesT().giveListOfNodes():
                    int3=n.giveIntervals2().intersection(IntervalList([interval]))
                    if int3.duration() != 0:
                        m2.addLayer(Layer(self.layerStruct,lay.giveLayerLabel(),int2,NodeTList([NodeT(n.giveNode(),int3,nodeLabel=n.giveNodeLabel())])))
        for e in self.em.giveListOfLinks():
            intL4=e.giveIntervals2().intersection(IntervalList([interval]))
            n1,n2,ll1,ll2= e.giveLabel()
            nodes=e.giveNodes()
            if intL4.duration() != 0:
                m2.addLink(Link(intL4,nodes[0],ll1,nodes[1],ll2))
        return(m2)
        
    def numberOfNodes(self):
        nnl=0
        nl=0
        for l in self.layers.giveLayers():
            for n in l.giveNodesT().giveListOfNodes():
                nnl=nnl+n.giveIntervals2().duration()
            nl=nl+l.giveInterval().length()
        return(nnl/nl)
    
    def numberOfNodeLayers(self):
        nnl=0
        for l in self.layers.giveLayers():
            for n in l.giveNodesT().giveListOfNodes():
                nnl=nnl+n.giveIntervals2().duration()
        return(nnl/self.T.length())

#tentative de représentation optimale du graphe en chantier
        
    def computeLengthEm(self,layer=""):
        """
            compute the duration of the links, sorts it and return a list of all the durations and the links
        """
        liste=[]
        i=0
        for e in self.em.giveListOfLinks():
            if layer=="":
                liste.append([e.giveLength(),i])
                i=i+1
            elif e.giveLayers()[0]==e.giveLayers()[1] and e.giveLayers()[0]==layer:
                liste.append([e.giveLength(),i])
                i=i+1
            else:
                i=i+1
        liste.sort()
        liste.reverse()
        return(liste)
    
    def ordreAretes(self,layer=""):
        liste=self.computeLengthEm(layer=layer)
        ordre=[]
        for i in range(len(liste)):
            arete=self.em.giveListOfLinks()[liste[i][1]]
            noeud1,noeud2=arete.giveNodes()[0],arete.giveNodes()[1]
            i1=-1
            i2=-1
            pi=0
            for p in ordre:
                for n in p:
                    if n.giveNode()==noeud2.giveNode():
                        i2=pi
                    if n.giveNode()==noeud1.giveNode():
                        i1=pi
                pi=pi+1
            if i1==-1 and i2==-1:
                print("a")
                ordre.append([noeud1,noeud2])
            elif i1==-1:
                print("b")
                ordre[i2]=ajouter(ordre[i2],noeud2,noeud1)
            elif i2==-1:
                print("c")
                ordre[i1]=ajouter(ordre[i1],noeud1,noeud2)
            elif i1!=i2 :
                print("d")
                nouv=joindre(ordre[i1],noeud1,ordre[i2],noeud2)
                elem1=ordre[i1]
                elem2=ordre[i2]
                ordre.remove(elem1)
                ordre.remove(elem2)
                ordre.append(nouv)
            else:
                print("e")
        ordref=[]
        for o in ordre :
            ordref=ordref+o
        return(ordref)


#    def computeStrength(self):
#        a=[]
#        for i in self.layers.giveLayers() :
#            tab=i.computeStrengthBetweenNodes(self.em)
#            a.append(tab)
#        return(a)

def indice(liste,elem1):
    i=0
    ind=0
    for n in liste:
        if n.giveNode()==elem1.giveNode():
            ind=i
        i=i+1
    return(ind)
        
def ajouter(liste,elem1,elem2):
    """
    element1 is on liste, elem2 is to add to list, but at the to or at the bottom ?
    """
    index1=indice(liste,elem1)
    if index1>=len(liste)/2:
        liste.append(elem2)
    else:
        liste.insert(0,elem2)
    return(liste)

def joindre(liste1,elem1,liste2,elem2):
    index1=indice(liste1,elem1)
    index2=indice(liste2,elem2)
    if index1<len(liste1)/2:
        liste1.reverse()
    if index2>len(liste2)/2:
        liste2.reverse()
    return(liste1+liste2)
    

def minimizeStrength(f):
    n=len(f)
    print("f",f)
    pos=[i for i in range(0,n)]#!!! chaque case indique la position du noeud
    grad=[0 for i in range(0,n)]
    fx=0
    for i in range(0,n):
        g=0
        for j in range(0,n):
            #print("i",pos[i],"j",pos[j],"f[pos(i)][pos(j)]",f[pos[i]][pos[j]],"dif",(pos[i]-pos[j])*((pos[i]-pos[j])**2-1))
            g=g+2*f[i][j]*(pos[i]-pos[j])
            fx=fx+f[i][j]*(pos[i]-pos[j])**2
        print("gi",g,"i",pos[i])
        grad[i]=g
    oldfx=fx+1
    print("--",fx)
    print("***",grad)
    while fx<oldfx:
        print("fx",fx)
        oldfx=fx
        oldpos=pos
        noeudDepl1,move=findDepl(grad,pos)
        print("gradient",grad)
        print("deplacement",findDepl(grad,pos))
        noeudDepl2=pos.index(pos[noeudDepl1]+move)
        pos[noeudDepl1],pos[noeudDepl2]=pos[noeudDepl2],pos[noeudDepl1]
        fx=0
        print("po",pos)
        for i in range(0,n):
            g=0
            for j in range(0,n):
                print("i",pos[i],"j",pos[j],"f[i][j]",f[i][j],"dif",(pos[i]-pos[j]))
                g=g+2*f[i][j]*(pos[i]-pos[j])
                fx=fx+f[i][j]*(pos[i]-pos[j])**2
                print((pos[i]-pos[j])**2)
            print("gi",g)
            print("fx",fx)
            grad[i]=g
        print("fxold",oldfx)
        print("fxend=",fx)
    return(oldpos)

def fonction(pos,f):
    n=len(pos)
    eps=0.1
    fx=0
    for i in range(0,n):
        for j in range(0,n):
            fx=fx+f[i][j]*((pos[i]-pos[j])**2-1)**2
            fx=fx+0.01*1/(pos[i]-pos[j]+eps)**2
    return fx

def gradient(pos,f):
    n=len(pos)
    g=[0]
    eps=0.1
    for i in range(1,n):
        gi=0
        for j in range(0,n):
            gi=gi+4*f[i][j]*(pos[i]-pos[j])*((pos[i]-pos[j])**2-1)
            gi=gi-0.01*1/(pos[i]-pos[j]+eps)**3
        g.append(gi)
    return(g)

def descentGrad(fonction,f,der,posini,iterations):
    h=0.01
    n=len(posini)
    pos=posini
    listefi=[]
    for i in range(0,iterations):
        affiche(pos)
        fi=fonction(pos,f)
        grad=der(pos,f)
        pos=[pos[j]-h*grad[j] for j in range(0,n)]
        listefi.append(fi)
    return(pos,listefi)

def affiche(liste):
    n=len(liste)
    tab=[i for i in range(0,n)]
    plt.plot(tab,liste,'ro')
    plt.show()
    
def findDepl(liste,pos):
    n=len(liste)
    m=0
    nm=0
    M=0
    nM=0
    ancm=0
    ancnm=0
    ancM=0
    ancnM=0
    print("lenliste",len(liste))
    p=0
    for i in range(0,len(liste)):
        print("liste",liste[i])
        if liste[i]>M:
            ancM=M
            ancnM=nM
            nM=i
            M=liste[i]
        elif liste[i]<=m:
            ancm=m
            ancnm=m
            nm = i 
            m=liste[i]
    if abs(M)>=abs(m) and pos[nM]>0:
        print("cas1")
        print("M",M,"depl",nM,nM-1)
        return(nM,-1)
    elif abs(M)<abs(m) and pos[nm]<n-1:
        print("cas2")
        print("m",m,"depl",nm,+1)
        return(nm,+1)
    elif abs(M)>=abs(m) :
        if abs(ancM)<abs(m) and pos[nm]<n-1:
            print("cas3")
            return(nm,+1)
    else:
        if abs(ancm)<abs(M) and pos[nM]>0:
            print("cas4")
            return(nM,-1)
    if abs(ancm)>abs(ancM):
        print("cas5")
        return(ancnM,-1)
    else :
        print("cas6")
        return(ancnm,+1)

def donnerOrdre(pos):
    n=len(pos)
    pos2=pos.copy()
    pos2.sort()
    posfin=[]
    for i in range(0,n):
        ind=pos.index(pos2[i])
        posfin.append(ind)
    return posfin
    