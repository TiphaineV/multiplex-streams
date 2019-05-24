from Drawing import *

from sortedcollection import *
from random import uniform
from intervals import *
from structure import *
from elemMSGraph import *
from multiLayers import *


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
    def printMS(self):
        print("T:",self.T.intervalToString() )
        print("structure")
        print("layers and nodes")
        self.layers.printLayerList()
        print("EM")
        for e in self.em.giveListOfLinks():
            e.printLink()
    def drawMS(self,nameFile2="default.fig",colors="byLayer",neglect=-1):
        """
            function drawMS :
            =====
            class MultiStream
            ---
            
            :type nameFile2: string
            :type colors: string
            :type neglect: int
            
            draw the mulitlayer into a .fig file.  (name of the file nameFile2)
            If colors = byLayers, the link are colored the same color in each layer, black interlayer.
            If neglect >0, we don't draw the link that last less than neglect.
        
        """
        f=Drawing(alpha=self.T.begining(),omega=self.T.end(),nameFile=nameFile2)
        if colors=="byLayer":
            color={}
        for i in range(self.layers.length()) :
            #f.printLayer() : todo
            lay=self.layers.giveLayer(i).giveLayerLabel()
            newlay=1
            if colors=="byLayer":
                col=7
                while col==7:
                    col=int(uniform(1,30))
                color[str(lay)]=col
            for j in self.layers.giveLayer(i).giveNodesT().giveListOfNodes():
                times=[]
                for k in j.giveIntervals():
                    times.append((k.begining(),k.end()))
                f.addNode(str(j.giveNode()),times=times,layer=str(lay),newLayer=newlay)
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
            multi.addLayer(layer)
            for e in self.em.giveListOfLinks():
                lay1=e.giveLayers()[0]
                lay2=e.giveLayers()[1]
                if lay1 in layerLabels:
                    if lay2 in layerLabels:
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
            for j in self.layers.giveLayer(i).giveNodesT().giveListOfNodes():#on sélectionne les noeuds apparaissant à t
                nodel.append(Node(j.giveNode()))
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
                        durationNodes=durationNodes+k.giveIntervals2().intersection(l.giveIntervals()).duration()
        return(durationLinks/durationNodes)
                
            
    