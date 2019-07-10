from sortedcollection import *
import random
import scipy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
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
    def removeLayer(self,layer):
        self.listOfLayersNT.remove(layer)
    

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
    def addLink(self,l):
        if self.listOfLinks.contains_key(l)==False:
            self.listOfLinks.insert(l)
    def addLinks(self,links):
        for l in links.giveListOfLinks():
            self.addLink(l)
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
    def addLink(self,link):
        self.em.addLink(link)
    def addLinks(self,links):
        self.em.addLinks(links)
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
            plt.plot([points[indexLayer1][indexNode1][0],points[indexLayer2][indexNode2][0]],[points[indexLayer1][indexNode1][1],points[indexLayer2][indexNode2][1]],'r') 
            #plt.plot([[0,1],[2,3]],'r')
        if nameFile != "":
            plt.savefig(nameFile+".pdf")
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

    def computeIntricationMatrixBurt(self):
        n=self.layers.length()    
        mat=np.zeros((n,n))
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
            N=N+1
            if link.giveLabel()[2]==link.giveLabel()[3]:
                n1=link.giveLabel()[0]
                n2=link.giveLabel()[1]
                indice=self.layers.giveIndex(link.giveLabel()[2])
                mat[indice][indice]=mat[indice][indice]+1
                liste=[]
                for link2 in em2:
                    if (link2.giveLabel()[0]==n1 and link2.giveLabel()[1]==n2) or(link2.giveLabel()[0]==n2 and link2.giveLabel()[1]==n1):
                        if link2.giveLabel()[2]==link2.giveLabel()[3]:
                            link2.printLink()
                            indice2=self.layers.giveIndex(link2.giveLabel()[2])
                            mat[indice][indice2]=mat[indice][indice2]+1
                            mat[indice2][indice]=mat[indice2][indice]+1
                            liste.append(link2)
        matc=np.zeros((n,n))
        for i in range(n):
            for j in range(n):
                if i==j:
                    matc[i][i]=mat[i][i]/N
                else :
                    matc[i][j]=mat[i][j]/mat[j][j]
        return(matc)
    def cleanML(self):
        layersVides=[]
        for lay in self.layers.giveLayerList():
            lien=False
            for e in self.em.giveListOfLinks():
                if e.giveLayers()[0]==lay.giveLayerLabel():
                    lien=True
                    break
            if lien==False:
                layersVides.append(lay)
        for l in layersVides:
            self.layers.removeLayer(l)
        print("ML graph cleaned")
    def matriceAdjacenceL(self,layerLabel):
        lay=self.layers.giveLayerFromLabel(layerLabel)
        nl=lay.giveNodes().length()
        listeNoeuds= (lay.giveNodes().giveListOfNodes())
        matAdj=np.zeros((nl,nl))
        for e in self.em.giveListOfLinks():
            if e.giveLayers()[0]==e.giveLayers()[1] and e.giveLayers()[0]==layerLabel:
                listeNoeuds.printsort()
                print(e.giveNodes()[0].printNode())
                print(e.giveNodes()[1].printNode())
                n1=listeNoeuds.index_label(e.giveNodes()[0].giveNode())
                n2=listeNoeuds.index_label(e.giveNodes()[1].giveNode())
                matAdj[n1][n2]=1
                matAdj[n2][n1]=1
        return(matAdj)
    
    def fichierTulip(self,nameFile=""):
        """
        !!! fonctionne pour le moment uniquement sur des partitions des noeuds couches !
        """
        file=open(nameFile+".tlp","w")
        file.write("(tlp \"2.0\")\n")
        file.write("(date \"12-15-2008\")\n")
        file.write("(author \"pp\") \n")
        file.write("(comments \"graph multilayer\")\n")
        file.write(";(nodes <node_id> <node_id> ...)\n")
        file.write("(nodes ")
        for lay in self.layers.giveLayerList():
            for nod in lay.giveNodes().giveListOfNodes():
                file.write(str(nod.giveNode())+" ")
        file.write(")\n")
        file.write(";(edge <edge_id> <source_id> <target_id>)\n")
        i=0
        for edge in self.em.giveListOfLinks():
                i=i+1
                file.write("(edge ")
                file.write(str(i)+" ")
                file.write(str(edge.giveNodes()[0].giveNode())+" "+str(edge.giveNodes()[1].giveNode()))
                file.write(")\n")
        file.write("(property  0 color \"viewColor\" ")
        for lay in self.layers.giveLayerList():
            couleur1 = random.randint(0,255)
            couleur2 = random.randint(0,255)
            couleur3 = random.randint(0,255)
            couleur4 = 255
            for nod in lay.giveNodes().giveListOfNodes():
                file.write("(node ")
                file.write(str(nod.giveNode())+" ")
                file.write("\"("+str(couleur1)+","+str(couleur2)+","+str(couleur3)+","+str(couleur4)+ ")\"")
                file.write(")\n")
        file.write(")")
        file.write("(property  0 size \"viewSize\"\n (default \"(2,2,2)\" \"(2,2,2)\"")
        file.close()
        print("done")

def valeurPropreMax(matrice,iterations):
    n=len(matrice)
    x=np.array([1 for i in range(n)])
    q=0
    A=np.eye(n)
    for i in range(iterations):
        A=np.dot(A,matrice)
    Anx=np.dot(A,x)
    vectpropre=Anx/np.linalg.norm(Anx,2)
    matx=np.dot(matrice,vectpropre)
    normevectpropre=np.linalg.norm(vectpropre)
    valeurPropre=np.linalg.norm(matx)/normevectpropre
    return(valeurPropre,vectpropre)