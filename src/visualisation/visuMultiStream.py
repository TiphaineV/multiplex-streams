from Drawing import *

from sortedcollection import *
from random import uniform
"""
Interval classes
"""

class Interval :
    """
        Describes intervals.

        Interval(t1,t2) gives the corresponding interval with the bounds sorted.
        :type t1: int or float
        :type t2: int of float

    """
    def __init__(self,t1,t2):
        self.t1 = min(t1,t2)
        self.t2 = max(t1,t2)

    def isIn(self,x):
        if x >= (self.t1) and x <= (self.t2) :
            return True
        else :
            return False

    def length(self):
        return (self.t2-self.t1)
    def begining(self):
        return(self.t1)
    def end(self):
        return(self.t2)
    def setBegining(self,b):
        self.t1=b
    def setEnd(self,e):
        self.t2=e

    def intersection(self,int2):
        """
            method intersection(int2)
            ======
            from class interval
            -----

            :type int2: Interval
            :returns: if the two intervals intersect, the intersection. If not, Interval(0,0).
            :rtype: Interval
        """
        if self.isIn(int2.begining()) or self.isIn(int2.end()) :
            return Interval(max(self.t1,int2.begining()),min(self.t2,int2.end()))
        elif int2.isIn(self.begining()) or int2.isIn(self.end()):
            return Interval(max(self.t1,int2.begining()),min(self.t2,int2.end()))
        else :
            return(Interval(0,0))
    def union(self,int2):
        """
            method union(int2)
            =======
            from class interval
            ----

            :type int2: Interval
            :returns: if the two intervals intersect, the union. If not, Interval(0,0).
            :rtype: Interval

        """
        if self.intersection(int2)==Interval(0,0):
            return (Interval(0,0))
        else :
            return(Interval(min(self.begining(),int2.begining()),max(self.end(),int2.end())))

    def contains(self,int2):
        """
            method contains(int2)
            ====
            from class Interval
            ----

            :type int2: Interval
            :returns: true if int2 is inside self, false otherwise
            :rtype: boolean

        """
        if (self.t1 <= int2.begining()) & (self.t2 >= int2.end()):
            return(True)
        else :
            return(False)

    def intervalToString(self):
        return("["+str(self.t1)+","+str(self.t2)+"]")
    def printInterval(self):
        print("["+str(self.t1)+","+str(self.t2)+"]")

class IntervalList :
    """
    class IntervalList :

    :type listOfIntervals: SortedCollection

    list of interval is always sorted (we use for that sorted collection) by the begining of each interval and do not contains overlapping intervals (the function
    condensate interval has been created on this purpose)
    """
    def __init__(self,listOfIntervals,key=lambda interval: interval.begining()):
        self.listOfIntervals = SortedCollection(iterable=listOfIntervals,key=key)
        self.condensateIntervals()

    def giveListOfIntervals(self):
        return(self.listOfIntervals)

    def condensateIntervals(self,index=0):
        """
            method condensateIntervals(self,index=0):
            =====
            class Intervals
            ------

            Simplifies the set of interval to have only separated intervals.

            :type listOfIntervals: list[Intervals]
            :type index: int
            :returns: sorted list of separated interval corresponding to the initial listOfInterval

            :exemple:
            >>> "[[2,4],[7,9],[6,8]]".condensateIntervals()
            [[2,4],[6,9]]
        """
        i=index;
        #print("type i",type(i))
        while i<((self.listOfIntervals.__len__())-1):
            #print(self.listOfIntervals[i].end(),self.listOfIntervals[i+1].begining())
            if self.listOfIntervals[i].end()>=self.listOfIntervals[i+1].begining():
                print("fusion!")
                inte=self.listOfIntervals.pop(i+1)
                self.listOfIntervals[i].setEnd(max(inte.end(),self.listOfIntervals[i].end()))
            else :
                i=i+1


    def addInterval(self,interval):
        #b=interval.begining()
        #self.printIntervals()
        k=self.listOfIntervals.index_key(interval)
        self.listOfIntervals.insert(interval)
        self.condensateIntervals(index=max(k-1,0))

    def printIntervals(self):
        print("list of intervals")
        for i in self.listOfIntervals:
            print(i.intervalToString())
    def intervalListToString(self):
        str=""
        for i in self.listOfIntervals:
            str=str+i.intervalToString()
        return str




"""
Building the structure of the multilayers.
"""

class Aspect :
    """
    class Aspect
    ====

    :type name: string
    :type elemLayer: undefined

    fixed during the time.
    """
    def __init__(self,name,elemLayer):
        self.name=name
        self.elemLayer = elemLayer

    def nameAspect(self):
        return(self.name)

    def giveElemLayer(self):
        return(self.elemLayer)
    def printAspect(self):
        print(self.name," : ", self.elemLayer)
    def aspectToString(self):
        stri=""
        stri=stri +str(self.name) +" : " + str(self.elemLayer)
        return(stri)


class LayerStruct :
    """
    type LayerStruct
    ====

    :type aspects: list[Aspect]

    doesn't move with time. Used to vizualisation and check coherence of the graph.
    """

    def __init__(self,aspects):
        self.aspects=aspects

    def addAspect(self, aspect):
        self.aspects.append(aspect)

    def printLayerStruct(self):
        for i in self.aspects :
            i.printAspect()

    def buildLayer(self):
        aspect2 = self.aspects.copy()
        def buildLayerRec(listOfAspects):
            if len(listOfAspects)==0:
                return([[]])
            else :
                elemLayers=(listOfAspects.pop()).listElemLayer()
                layers = buildLayerRec(listOfAspects)
                lengthLayersList = len(layers)
                for j in range(lengthLayersList) :
                    l=layers.pop(0)
                    for j in elemLayers :
                        l.append(j)
                        layers.append(l.copy())
                        l.pop()
                return(layers)
        return(buildLayerRec(aspect2))

    def buildLayerT(self,interval):
        layers = self.buildLayer()
        layersT=[]
        for l in layers :
            layersT.append(LayerT(l,interval))
        return(layersT)
    def isALayerLabel(self,layerLabel):
        for l in range(len(layerLabel)):
            if not(layerLabel[l] in (self.aspects[l]).giveElemLayer()):
                return False
        return True









"""
Graph contents
"""


class NodeT :
    """
    class NodeT :
    =====

    :type node: node
    :type intervals: IntervalList

    """
    def __init__(self,node,intervals):
        self.node=node
        self.intervals = intervals
        self.intervals.condensateIntervals()
    def giveIntervals(self):
        return(self.intervals.giveListOfIntervals())
    def giveNode(self):
        return(self.node)
    def addInterval(self,interval):
        self.intervals.addInterval(interval)
    def printNodeT(self):
        print("node : "+ str(self.node)+ ", intervals : "+self.intervals.intervalListToString() )


class NodeTList :
    """
    class NodeTList :
    ====

    :type listOfNodeT: list[NodeT]

    The listOfNodeT contains each layer once, and inside each layer, we find each node once, in which the intervals are sorted and not overlapping
    """
    def __init__(self,liste,key=lambda nodeT: nodeT.giveNode()):
        self.listOfNodeT = SortedCollection(iterable=liste,key=key)

    def addNodeT(self,n):
        if self.listOfNodeT.__contains__(n):
            i = self.listOfNodeT.index(n)
            for inter in n.giveIntervals():
                self.listOfNodeT[index].addInterval(inter)
        else :
            self.listOfNodeT.insert(n)
    def giveListOfNodes(self):
        return(self.listOfNodeT)
    def printNodeTList(self):
        print("listOfNodes")
        for n in self.listOfNodeT :
            n.printNodeT()

class Layer :
    """
    class Layer :
    =====
    :type layerLabel: list[ElemLayer]
    :type interval: Interval
    :type nodesT: NodeTList
    """

    def __init__(self,layerStruct,layerLabel,interval,nodesT,checkCorrectL="True", checkCorrectN="True"):
        if checkCorrectL :
            if not(layerStruct.isALayerLabel(layerLabel)):
                print("not possible")
        self.layerLabel=layerLabel
        self.interval = interval
        self.nodesT = NodeTList([])
        if checkCorrectN :
            for n in nodesT.giveListOfNodes() :
                self.nodesT.addNodeT(n)
        else :
            self.nodesT=NodeTList(nodesT)

    def giveLayerLabel(self):
        return(self.layerLabel)
    def giveInterval(self):
        return(self.interval)
    def giveNodesT(self):
        return(self.nodesT)
    def addNodeT(self,n):
        self.nodesT.addNodeT(n)
    def setInterval(self,inter):
        self.interval=inter
    def printLayer(self):
        print("layer"+str(self.layerLabel))
        print("interval")
        self.interval.printInterval()
        print("nodes:")
        self.nodesT.printNodeTList()

class LayerList :
    """
    class LayerList:
    ======

    :type listOflayers : list[Layer]

    - each layerLabel appears one time max
    - each node appears one time max in each layer
    """
    def __init__(self,listOfLayers,key = lambda layer : layer.giveLayerLabel()):
        self.listOfLayers = SortedCollection(iterable=listOfLayers,key=key)
        self.condensate()

    def condensate(self,start=0):
        i = start
        while(i<(self.listOfLayers.__len__())-1):
            if self.listOfLayers[i].giveLayerLabel()==self.listOfLayers[i+1].giveLayerLabel():
                for n in self.listOfLayers[i+1].giveNodes():
                    self.listOfLayers[i].addNode(n)
                self.listOfLayers.pop(i+1)
            else:
                i=i+1
    def addLayer(self,layer):
        """
        function addLayer(layer)
        ===
        class LayerList
        ---

        :type layer: Layer

        add some node-layers from one layer.
        """
        if self.listOfLayers.contains_key(layer):
            i=self.listOfLayers.index_key(layer)
            self.listOfLayers[i].setInterval(layer.giveInterval().union(self.listOfLayers[i].giveInterval()))
            for n in layer.giveNodesT().giveListOfNodes():
                self.listOfLayers[i].addNodeT(n)
        else:
            self.listOfLayers.insert(layer)
    
    def length(self):
        return(self.listOfLayers.__len__())
    def giveLayer(self,i):
        return(self.listOfLayers[i])
    def printLayerList(self):
        print("list of layers :")
        for l in self.listOfLayers :
            l.printLayer()

    

class Link:
    """
    class Link : 
    for now, very simplified.
    
    :type intervals: intervalList
    :type node1/2: nodeT
    :type layerLabel1/2: str ?
    
    todo : Find a better indexing ?
    """
    def __init__(self,intervals,node1,layerLabel1,node2,layerLabel2):
        if node1.giveNode()>node2.giveNode():
            layerLabel1,layerLabel2=layerLabel2,layerLabel1
            node1,node2=node2,node1
        self.intervals=intervals
        self.node1=node1
        self.node2=node2
        self.layerLabel1=layerLabel1
        self.layerLabel2=layerLabel2
        #intervals.printIntervals()
    
    def giveIntervals(self):
        return(self.intervals.giveListOfIntervals())
    def addInterval(self,i):
        self.intervals.addInterval(i)
    def giveNodes(self):
        return([self.node1,self.node2])
    def giveLayers(self):
        return([self.layerLabel1,self.layerLabel2])
    def giveLabel(self):
        return([self.node1.giveNode(),self.node2.giveNode(),self.layerLabel1,self.layerLabel2])
    def printLink(self):
        print("Link : ")
        self.node1.printNodeT()
        print("from"+str(self.layerLabel1))
        print("--->")
        self.node2.printNodeT()
        print("from"+str(self.layerLabel2))
        print("endlink")


class LinkList:
    """
    class LinkList : 
    the list is sorted by the names of node1, then the name of node2, then the layer1, then Layer2.
    
    """
    
    def __init__(self,liste,key=lambda link: link.giveLabel()):
        self.listOfLinks = SortedCollection(iterable=liste,key=key)
    
    def addLink(self,l):
        if self.listOfLinks.contains_key(l):
            #print("la liste")
            #self.printListLabels()
            #print("l'element")
            #print(l.giveLabel())
            i = self.listOfLinks.index_key(l)
            for inter in l.giveIntervals():
                #print("-------cond")
                #print("type link",type(self.listOfLinks[i]))
                #self.listOfLinks[i].printLink()
                #inter.printInterval()
                self.listOfLinks[i].addInterval(inter)
        else : 
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
    def addLink(self,link):
        #to do : check intervals coherence
        self.em.addLink(link)
    def printMS(self):
        print("T:",self.T.intervalToString() )
        print("structure")
        print("layers and nodes")
        self.layers.printLayerList()
        print("EM")
        for e in self.em:
            e.printLink()
    def drawMS(self,nameFile2="default.fig"):
        f=Drawing(alpha=self.T.begining(),omega=self.T.end(),nameFile=nameFile2)
        for i in range(self.layers.length()) :
            #f.printLayer() : todo
            lay=self.layers.giveLayer(i).giveLayerLabel()
            newlay=1
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
                #print("lay1",lay1)
                lay2=str(j.giveLayers()[1])
                #inte.printInterval()
                f.addLink( u, v, b, e, layer1=lay1, layer2=lay2,color=int(uniform(1,20)))
        f.closeFile()
