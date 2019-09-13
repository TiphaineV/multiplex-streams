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



class MultiStream :
    """
    class MultiStream :
    ====

    :type T: interval
    :type layerStruct: LayerStruct
    :type layers: LayerList
    :type em: LinkList

    """

    def __init__(self,T,layerStruct,layers,em,nodes=[],directed=False):
        #todo : coherence checks !!
        self.T=T
        self.layerStruct=layerStruct
        self.layers = layers #todo : create empty layer with good structure, then add the layers in it.
        self.em = em
        self.nodes=nodes
        self.directed=directed

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
    def addLink(self,link,tolerance=0,cond=1):
        #to do : check intervals coherence
        self.em.addLink(link,tolerance,cond)
    def giveLinks(self):
        return(self.em)
    def printNodes(self):
        print("layers")
        for l in self.layers.giveLayers():
            l.printLayer()
    def printMS(self):
        print("T:",self.T.intervalToString() )
        print("structure")
        self.layerStruct.printLayerStruct()
        print("layers and nodes")
        self.layers.printLayerList()
        print("EM")
        for e in self.em.giveListOfLinks():
            e.printLink()
    def drawMS(self,nameFile2="default.fig",colors="byLayer",neglect=-1,ordonne=False,colL={}):
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
                    f.addNode(str(j.giveNode()),times=times,layer=str(lay),newLayer=0,write=j.giveNodeLabel(),color=j.color)
                    print("j.color",j.color)
                    newlay=0
            else :
                for j in self.layers.giveLayer(i).giveNodesT().giveListOfNodes():
                    times=[]
                    for k in j.giveIntervals():
                        times.append((k.begining(),k.end()))
                    f.addNode(str(j.giveNode()),times=times,layer=str(lay),newLayer=0,write=j.giveNodeLabel(),color=j.color)
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
                    c=j.color
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

    def comupteIntricationMatrixBurtMS(self):
        """ attention incomplet: N à changer, cf multilayers"""
        n=self.layers.length()
        mat=np.zeros((n,n))
        matIntervales=[[[]for i in range(n)]for i in range(n)]
        i1=0
        j1=0
        ne=self.em.length()
        N=0
        ind=0
        liste=[]
        em2=self.em.giveListOfLinks().copy()
        while em2.__len__()!=0:
            link=em2[0]
            em2.remove(link)
            N=N+link.giveIntervals2().duration()
            if link.giveLabel()[2]==link.giveLabel()[3]:
                n1=link.giveLabel()[0]
                n2=link.giveLabel()[1]
                indice=self.layers.giveIndex(link.giveLabel()[2])
                mat[indice][indice]=mat[indice][indice]+link.giveIntervals2().duration()
                liste=[]
                for link2 in em2:
                    if (link2.giveLabel()[0]==n1 and link2.giveLabel()[1]==n2) or(link2.giveLabel()[0]==n2 and link2.giveLabel()[1]==n1):
                        if link2.giveLabel()[2]==link2.giveLabel()[3]:
                            link2.printLink()
                            indice2=self.layers.giveIndex(link2.giveLabel()[2])
                            nnodescroises=link2.giveIntervals2().intersection(link.giveIntervals2()).duration()
                            mat[indice][indice2]=mat[indice][indice2]+nnodescroises
                            mat[indice2][indice]=mat[indice2][indice]+nnodescroises
                            liste.append(link2)
        print(mat)
        matc=np.zeros((n,n))
        for i in range(n):
            for j in range(n):
                if i==j:
                    matc[i][i]=mat[i][i]/N
                else :
                    matc[i][j]=mat[i][j]/mat[j][j]
        return(matc)
        
    def computeCovMatrix(self):
        """ attention incomplet: N à changer, cf multilayers"""
        n=self.layers.length()
        mat=np.zeros((n,n))
        matIntervales=[[[]for i in range(n)]for i in range(n)]
        i1=0
        j1=0
        ne=self.em.length()
        N=0
        ind=0
        liste=[]
        em2=self.em.giveListOfLinks().copy()
        while em2.__len__()!=0:
            link=em2[0]
            em2.remove(link)
            N=N+link.giveIntervals2().duration()
            if link.giveLabel()[2]==link.giveLabel()[3]:
                n1=link.giveLabel()[0]
                n2=link.giveLabel()[1]
                indice=self.layers.giveIndex(link.giveLabel()[2])
                mat[indice][indice]=mat[indice][indice]+link.giveIntervals2().duration()
                liste=[]
                for link2 in em2:
                    if (link2.giveLabel()[0]==n1 and link2.giveLabel()[1]==n2) or(link2.giveLabel()[0]==n2 and link2.giveLabel()[1]==n1):
                        if link2.giveLabel()[2]==link2.giveLabel()[3]:
                            link2.printLink()
                            indice2=self.layers.giveIndex(link2.giveLabel()[2])
                            nnodescroises=link2.giveIntervals2().intersection(link.giveIntervals2()).duration()
                            mat[indice][indice2]=mat[indice][indice2]+nnodescroises
                            mat[indice2][indice]=mat[indice2][indice]+nnodescroises
                            liste.append(link2)
        print(mat)
        matc=np.zeros((n,n))
        for i in range(n):
            for j in range(n):
                if i==j:
                    matc[i][i]=mat[i][i]/N-(mat[i][i]/N)**2
                else :
                    matc[i][j]=mat[i][j]/N-mat[j][j]*mat[i][i]/(N*N)
        return(matc)
        
    def elemLayerDensitiesMat(self,aspect):
        n=len(aspect.giveElemLayer())
        mat=np.zeros((n,n))
        listeElemLay= aspect.giveElemLayer().copy()
        for i in range(len(listeElemLay)):
            asp=listeElemLay[i]
            labs=layerWithCommonPoint(self.layerStruct,aspect.nameAspect(),asp)
            subgraph=self.extractLayers(labs)
            dens=subgraph.computeDensity()
            mat[i][i]=dens
            for j in range(i+1,len(listeElemLay)):
                asp2=listeElemLay[j]
                labs2=layerWithCommonPoint(self.layerStruct,aspect.nameAspect(),asp2)
                subgraph=self.interLayers(labs,labs2)
                dens2=subgraph.computeDensityBiparti(labs,labs2)
                mat[i][j]=dens2
                mat[j][i]=dens2
        return([mat,listeElemLay])
    
    def elemLayerDensitiesMatDiag0(self,aspect):
        n=len(aspect.giveElemLayer())
        mat=np.zeros((n,n))
        listeElemLay= aspect.giveElemLayer().copy()
        for i in range(len(listeElemLay)):
            asp=listeElemLay[i]
            labs=layerWithCommonPoint(self.layerStruct,aspect.nameAspect(),asp)
            subgraph=self.extractLayers(labs)
            dens=subgraph.computeDensity()
            mat[i][i]=0
            for j in range(i+1,len(listeElemLay)):
                asp2=listeElemLay[j]
                labs2=layerWithCommonPoint(self.layerStruct,aspect.nameAspect(),asp2)
                subgraph=self.interLayers(labs,labs2)
                dens2=subgraph.computeDensityBiparti(labs,labs2)
                mat[i][j]=dens2
                mat[j][i]=dens2
        return([mat,listeElemLay])
    
    def giveListForForemost(self):
        return(self.em.giveListForForemost())
    
    def foremostPath(self,nodeLab,s,t0=0):
        t=[-1 for i in self.nodes]
        #print(self.nodes)
        t[self.nodes.index(nodeLab)]=t0
        while s.__len__()>0:
            l0=s.pop(0)
            lab=l0.giveLabel()
            time=l0.popInterval(0)
            #print("link",lab)
            #print("dist",t[self.nodes.index(lab[0])], t[self.nodes.index(lab[0])],time.begining())
            if t[self.nodes.index(lab[0])]>=0 and t[self.nodes.index(lab[0])]<=time.begining():#si on peut prendre cet avion
                #print("on peut pprendre cet avion:")
                if t[self.nodes.index(lab[1])]>=time.end() or t[self.nodes.index(lab[1])]==-1:
                    #print("avion selectionne")
                    t[self.nodes.index(lab[1])]=time.end()
            #print("l0",l0.giveIntervals())
            if l0.giveIntervals().__len__()>0:
                s.insert(l0)
        return(t)
        
    def giveListForLastDept(self):
        return(self.em.giveListForLastDept())
    
    def lastDeptPath(self,nodeLab,s,t0=0):
        t=[-1 for i in self.nodes]
        t[self.nodes.index(nodeLab)]=t0
        while s.__len__()>0:
            l0=s.pop(0)
            lab=l0.giveLabel()
            time=l0.popInterval(0)
            #l0.printLink()
            #time.printInterval()
            if t[self.nodes.index(lab[1])]>=0 and t[self.nodes.index(lab[1])]>=time.end(): #si on peut prendre cet avion
                if t[self.nodes.index(lab[0])]<=time.begining() or t[self.nodes.index(lab[0])]==-1: #si il améliore le score
                    t[self.nodes.index(lab[0])]=time.begining()
            if l0.giveIntervals().__len__()>0:
                s.insert(l0)
        return(t)
        
    def findWindows(self,node,to):
        s1=self.giveListForForemost()
        s2=self.giveListForLastDept()
        endWindows=self.foremostPath(node,s1,t0=to)
        beginingWindows=self.lastDeptPath(node,s2,t0=to)
        windows=[]
        for i in range(len(beginingWindows)):
            windows.append([beginingWindows[i],endWindows[i]])
        return(windows)

    def enumShortestPath(self,source,target):
        #a finir
        s=self.em.giveListForEnum()
        tab=[[]for i in range(len(self.nodes))]
        deptAndArr=[[]for i in range(len(self.nodes))]
        encadr=[[] for i in range(len(self.nodes))]
        while len(s)!= 0:
            l0=s.pop(0)
            lab=l0.giveLabel()
            time=l0.popInterval(0)
            if lab[0]==source:
                tab[self.nodes.index(lab[1])].append([lab[1]])
                deptAndArr[self.nodes.index(lab[1])].append([])
            elif len(tab[self.nodes.index(lab[0])])>0:
                return()
        return()
    
    def avionsSuivants(self,source,time,sizeWindows):
        noeudsAtteints=[[]for i in range(len(self.nodes))]
        nlay=len(self.layers.giveLayers())
        compUtilisees=[ [] for i in range(nlay)]
        for i in self.em.giveListOfLinks():
            lab=i.giveLabel()
            if lab[0]==source:
                for tps in i.giveIntervals():
                    if tps.begining()>=time and tps.begining()<=time+sizeWindows:
                        noeudsAtteints[self.nodes.index(lab[1])].append(tps.begining())
                        print(lab[2])
                        print(self.layers.giveLayers().index_label(lab[2]))
                        ind=self.layers.giveLayers().index_label(lab[2])
                        compUtilisees[ind].append(tps.begining())
        return(noeudsAtteints,compUtilisees)
    
    def tmpsTransition(self,source):
        tpsL=[]
        for i in self.em.giveListOfLinks():
            lab=i.giveLabel()
            if lab[1]==source:
                for tps in i.giveIntervals():
                    tpsL.append(tps)
        return(tpsL)
    
    def calculProba(self,source,noeudsAtteints,compUtilisees,t0,sizeWindows):
        probaNodes=[ 0 for i in range(len(self.nodes))]
        pN=0
        nlay=len(self.layers.giveLayers())
        probaLay=[ 0 for i in range(nlay)]
        pL=0
        for i in range(len(probaNodes)):
            for j in range(len(noeudsAtteints[i])):
                probaNodes[i]=probaNodes[i]+sizeWindows-(noeudsAtteints[i][j]-t0)
                pN=pN+sizeWindows-(noeudsAtteints[i][j]-t0)
        for i in range(len(probaLay)):
            for j in range(len(compUtilisees[i])):
                probaLay[i]=probaLay[i]+sizeWindows-(compUtilisees[i][j]-t0)
                pL=pL+sizeWindows-(compUtilisees[i][j]-t0)
        for i in range(len(probaNodes)):
            if pN!=0:
                probaNodes[i]=probaNodes[i]/pN
            else:
                probaNodes[self.nodes.index(source)]=1
        for i in range(len(probaLay)):
            if pL!=0:
                probaLay[i]=probaLay[i]/pL
        return(probaNodes,probaLay)
    
    def calculMatriceProbaTransition(self,t0,sizeWindows):
        matNodes=[[[]for j in range(len(self.nodes))] for i in range(len(self.nodes))]
        nLay=len(self.layers.giveLayers())
        matLay=[[[] for j in range(nLay)] for i in range(len(self.nodes))]
        for i in range(len(self.nodes)):
            nAtteints,compUtilisees=self.avionsSuivants(self.nodes[i],t0,sizeWindows)
            pNodes,pLay=self.calculProba(self.nodes[i],nAtteints,compUtilisees,t0,sizeWindows)
            for j in range(len(self.nodes)):
                matNodes[i][j]=pNodes[j]
            for k in range(nLay):
                matLay[i][k]=pLay[k]
        return(matNodes,matLay)
        
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
    

