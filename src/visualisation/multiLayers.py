from sortedcollection import *

import scipy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

#matplotlib.use('AGG')

"""
MultiLayer class is usefull to do some extraction from multilayer stream.
"""

class Node:
    def __init__(self,nodeName):
        self.node= nodeName
    def giveNode(self):
        return(self.node)
    def printNode(self):
        print(self.node)

class NodeList :
    """
    class NodeList :
    ====

    :type listOfNode: list[NodeLabel(str)]

    The listOfNodeT contains each layer once, and inside each layer, we find each node once maximum.
    """
    def __init__(self,liste, key=lambda node : node.giveNode()):
        a=[]
        keya=[]
        for i in liste :
            if not(key(i) in keya):
                a.append(i)
                keya.append(key(i))
        self.listOfNode = SortedCollection(iterable=a,key=key)

    def addNode(self,n):
        if self.listOfNode.__contains__(n)==False : 
            self.listOfNode.insert(n)
    def giveListOfNodes(self):
        return(self.listOfNode)
    def giveIndex(self, node):
        return(self.listOfNode.index_label(node))
    def printNodeList(self):
        print("listOfNodes")
        for n in self.listOfNode :
            n.printNode()
    def length(self):
        return(self.listOfNode.__len__())

class LayerNT :
    """
    class LayerNT :
    =====
    :type layerLabel: list[ElemLayer]
    :type nodes: NodeList
    """

    def __init__(self,layerStruct,layerLabel,nodes,checkCorrectL="True", checkCorrectN="True"):
        if checkCorrectL :
            if not(layerStruct.isALayerLabel(layerLabel)):
                print("not possible")
        self.layerLabel=layerLabel
        self.nodes = NodeList([])
        if checkCorrectN :
            for n in nodes.giveListOfNodes() :
                self.nodes.addNode(n)
        else :
            self.nodes=NodeList(nodes)

    def giveLayerLabel(self):
        return(self.layerLabel)
    def giveNodes(self):
        return(self.nodes)
    def giveIndex(self,node):
        return(self.nodes.giveIndex(node))
    def addNode(self,n):
        self.nodes.addNode(n)
    def printLayer(self):
        print("layer"+str(self.layerLabel))
        print("nodes:")
        self.nodes.printNodeList()

class LayerNTList :
    """
    class LayerNTList:
    ======

    :type listOflayers : list[Layer]

    - each layerLabel appears one time max
    - each node appears one time max in each layer
    """
    def __init__(self,listOfLayersNT,key = lambda layer : layer.giveLayerLabel()):
        self.listOfLayersNT = SortedCollection(iterable=listOfLayersNT,key=key)
        self.condensate()

    def condensate(self,start=0):
        i = start
        while(i<(self.listOfLayersNT.__len__())-1):
            if self.listOfLayersNT[i].giveLayerLabel()==self.listOfLayersNT[i+1].giveLayerLabel():
                for n in self.listOfLayersNT[i+1].giveNodes():
                    self.listOfLayersNT[i].addNode(n)
                self.listOfLayersNT.pop(i+1)
            else:
                i=i+1
    def giveLayerList(self):
        return(self.listOfLayersNT)
    def addLayer(self,layer):
        """
        function addLayer(layer)
        ===
        class LayerList
        ---

        :type layer: Layer

        add some node-layers from one layer.
        """
        if self.listOfLayersNT.contains_key(layer):
            i=self.listOfLayersNT.index_key(layer)
            for n in layer.giveNodes().giveListOfNodes():
                self.listOfLayersNT[i].addNode(n)
        else:
            self.listOfLayersNT.insert(layer)
    def giveIndex(self,layerLabel):
        return(self.listOfLayersNT.index_label(layerLabel))
    
    def length(self):
        return(self.listOfLayersNT.__len__())
    def giveLayer(self,i):
        return(self.listOfLayersNT[i])
    def giveLayerFromLabel(self,label):
        #print(label)
        print("ici ?")
        if self.listOfLayersNT.contains_label(label):
            i=self.listOfLayersNT.index_label(label)
            print("ici2")
            return(self.giveLayer(i))
        else:
            print("error : this layer doesn't exist : ",label)
            
    def printLayerList(self):
        print("list of layers :")
        for l in self.listOfLayersNT :
            l.printLayer()

class LinkNT:
    """
    class LinkNT : 
    for now, very simplified.
    
    :type node1/2: node
    :type layerLabel1/2: str 
    
    todo : Find a better indexing ?
    """
    def __init__(self,node1,layerLabel1,node2,layerLabel2):
        if node1.giveNode()>node2.giveNode():
            layerLabel1,layerLabel2=layerLabel2,layerLabel1
            node1,node2=node2,node1
        self.node1=node1
        self.node2=node2
        self.layerLabel1=layerLabel1
        self.layerLabel2=layerLabel2
        #intervals.printIntervals()
    
    def giveNodes(self):
        return([self.node1,self.node2])
    def giveLayers(self):
        return([self.layerLabel1,self.layerLabel2])
    def giveLabel(self):
        return([self.node1.giveNode(),self.node2.giveNode(),self.layerLabel1,self.layerLabel2])
    def printLink(self):
        print("Link : ")
        self.node1.printNode()
        print("from"+str(self.layerLabel1))
        print("--->")
        self.node2.printNode()
        print("from"+str(self.layerLabel2))
        print("endlink")


class LinkNTList:
    """
    class LinkNTList : 
    the list is sorted by the names of node1, then the name of node2, then the layer1, then Layer2.
    
    """
    
    def __init__(self,liste,key=lambda link: link.giveLabel()):
        self.listOfLinks = SortedCollection(iterable=liste,key=key)
    
    def addLink(self,l,tolerance=0):
        if self.listOfLinks.contains_key(l)==False:
            self.listOfLinks.insert(l)
    def giveListOfLinks(self):
        return(self.listOfLinks)
    def printLinkList(self):
        print("list of link")
        for n in self.listOfLinks :
            n.printLink()
    def printListLabels(self):
        for l in self.listOfLinks:
            print(l.giveLabel())
    def length(self):
        return(self.listOfLinks.__len__())

            


class MultiLayer :
    """
    class MultiLayer :
        
    :type layers: LayerNTList
    :type links: LinkNTList
    """
    def __init__(self,struct,layers,links):
        self.layerStruct=struct
        self.layers = layers 
        self.em = links

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
    def printML(self):
        print("layers and nodes")
        self.layers.printLayerList()
        print("EM")
        for e in self.em.giveListOfLinks():
            e.printLink()
    
    def extractLayers(self,layerLabels):
        """
            function extractLayers
            ====
            from class MultiLayer
            --
            
            :type layerLabel: list[layerLabel]
            
            return the layers asked with the nodes and the links included in those layers.
        """
        multi=MultiLayer(self.layerStruct,LayerNTList([]),LinkNTList([]))
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
        
    def drawML(self,nameFile="",names=False):
        """
            draw a multilayer graph. Each circle corresponds to one layer.
        """
        nl=self.layers.length()
        #we create a "big circle" to place the different layers
        pointsLay=[(np.cos(np.pi *2* k /nl),np.sin(np.pi *2* k /nl)) for k in range(nl)] 
        points=[]
        n=0
        fig = plt.figure()
        plt.axis('off')
        plt.gcf().set_size_inches(20, 20)
        nlayer=len(self.layers.giveLayerList())
        texte=[]
        for l in self.layers.giveLayerList():
            npt=l.giveNodes().length()
            pl=[(np.cos(np.pi *2* k /npt),np.sin(np.pi *2* k /npt)) for k in range(npt)]
            points.append([(pointsLay[n][0]+(1/nlayer)*pl[i][0],pointsLay[n][1]+(1/nlayer)*pl[i][1]) for i in range(npt)])
            plt.text((1.2+1/nlayer)*pointsLay[n][0],(1.2+1/nlayer)*pointsLay[n][1],l.giveLayerLabel(),fontsize=50)
            n=n+1
            if names==True:
                textel=[]
                for node in l.giveNodes().giveListOfNodes():
                    textel.append(node.giveNode())
                texte.append(textel)
        npoints=len(points)
        for l in range(len(points)):
            for j in range(len(points[l])):
                plt.plot(points[l][j][0],points[l][j][1],'ko')
                if names==True:
                    plt.text(points[l][j][0]+0.01,points[l][j][1]+0.01,texte[l][j],fontsize=50)
        #print(points)
        #self.em.printLinkList()
        for e in self.em.giveListOfLinks():
            indexLayer1=self.layers.giveIndex(e.giveLabel()[2])
            indexLayer2 = self.layers.giveIndex(e.giveLabel()[3])
            indexNode1 = self.layers.giveLayer(indexLayer1).giveIndex(e.giveNodes()[0].giveNode())
            indexNode2 = self.layers.giveLayer(indexLayer2).giveIndex(e.giveNodes()[1].giveNode())
            #e.printLink()
            #print([points[indexLayer1][indexNode1][0],points[indexLayer2][indexNode2][0]],[points[indexLayer1][indexNode1][1],points[indexLayer2][indexNode2][1]])
            plt.plot([points[indexLayer1][indexNode1][0],points[indexLayer2][indexNode2][0]],[points[indexLayer1][indexNode1][1],points[indexLayer2][indexNode2][1]],'r') 
            #plt.plot([[0,1],[2,3]],'r')
        if nameFile != "":
            plt.savefig(nameFile)
        plt.show()
    
    def computeDensityMulti(self):
        ne = self.em.giveListOfLinks().__len__()
        nnodes=0
        for l in self.layers.giveLayerList():
            nnodes=nnodes+l.giveNodes().giveListOfNodes().__len__()
        return(2*ne/(nnodes*(nnodes-1)))
    
    def computeDensityMultiBiparti(self,layerlabels1,layerlabels2):
        ne = self.em.giveListOfLinks().__len__()
        nnodes1=0
        nnodes2=0
        for i in self.layers.giveLayerList():
            if (i.giveLayerLabel() in layerlabels1):
                nnodes1=nnodes1+i.giveNodes().giveListOfNodes().__len__()
            elif (i.giveLayerLabel() in layerlabels2):
                nnodes2=nnodes2+i.giveNodes().giveListOfNodes().__len__()
        return(ne/(nnodes1*nnodes2))

    def computeIntrication(self):
        n=self.layers.length()
        mat=np.zeros((n,n))
        i1=0
        j1=0
        ne=self.em.length()
        N=0
        for i in self.layers.giveLayerList():
            j1=0
            for j in self.layers.giveLayerList():
                if i1==j1:
                    mat[i1][i1]=i.giveNodes().length()
                    N=N+mat[i1][i1]
                else:
                    #rechercher combien on a dans l'intersection
                    s=0
                    for nodesi in i.giveNodes().giveListOfNodes():
                        print("nodei",nodesi)
                        if nodesi.contains_key(nodesi.giveNode()):
                            s=s+1
                    mat[i1][j1]=s
                j1=j1+1
            i1=i1+1   
        matc=np.zeros((n,n))
        for i in range(n):
            for j in range(n):
                if i==j:
                    matc[i][i]=mat[i][i]/N
                else :
                    matc[i][j]=mat[i][j]/mat[j][j]
        return(matc)