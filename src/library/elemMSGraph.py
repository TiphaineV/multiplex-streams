# -*- coding: utf-8 -*-
"""
Created on Wed May 22 15:02:31 2019

@author: Pimprenelle
"""

from library.sortedcollection import *
from library.intervals import *
import numpy as np

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
    def __init__(self,node,intervals,nodeLabel="",color=0):
        self.node=node
        self.intervals = intervals
        self.intervals.condensateIntervals()
        self.nodeLabel=nodeLabel
        self.color=color
    def giveIntervals(self):
        """
        function giveIntervals()
        from NodeT
        
        return the list of intervals of type SortedCollection
        """
        return(self.intervals.giveListOfIntervals())
    def giveIntervals2(self):
        """
        function giveIntervals()
        from NodeT
        
        return the list of intervals of type IntervalList
        """
        return(self.intervals)
    def giveNode(self):
        return(self.node)
    def giveNodeLabel(self):
        return(self.nodeLabel)
    def addInterval(self,interval):
        self.intervals.addInterval(interval)
    def printNodeT(self):
        print("node : "+ str(self.node)+ str(self.nodeLabel)+ ", intervals : "+self.intervals.intervalListToString() )


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
            index = self.listOfNodeT.index(n)
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
    def length(self):
        return(self.listOfNodeT.__len__())

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
        
    def computeStrengthBetweenNodes(self,links):
        n=self.nodesT.giveListOfNodes().__len__()
        f=[[0 for i in range(0,n)]for j in range(0,n)]
        nInteract=SortedCollection([], key = lambda elem  : elem[0])
        for i in links.giveListOfLinks():# we build a list of the times of begining of interaction and the number of simultaneus interactions at this time.
            for j in i.giveIntervals():
                b=j.begining()
                if nInteract.contains_label(b):
                    nInteract[nInteract.index_label(b)][1]=nInteract[nInteract.index_label(b)][1]+1
                else :
                    nInteract.insert([b,1])
        #filling the strenghs matrixes
        for i in links.giveListOfLinks():
            node1,node2,label1,label2=i.giveLabel()
            n1,n2= self.nodesT.giveListOfNodes().index_label(node1),self.nodesT.giveListOfNodes().index_label(node2)
            if label1==label2 and label1==self.layerLabel :
                for j in i.giveIntervals():
                    b=j.begining()
                    f[n1][n2]=f[n1][n2] + nInteract[nInteract.index_label(b)][1]
        return(f)
                
    
        
        

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
    def giveLayers(self):
        return(self.listOfLayers)
        
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
    def giveLayerFromLabel(self,label):
        if self.listOfLayers.contains_label(label):
            i=self.listOfLayers.index_label(label)#ecrit ?
            return(self.giveLayer(i))
        else:
            return(0)
            
    def printLayerList(self):
        print("list of layers :")
        for l in self.listOfLayers :
            l.printLayer()

    def giveIndex(self,label):
        return(self.listOfLayers.index_label(label))
    def removeLayer(self,layer):
        self.listOfLayers.remove(layer)
    
class Link:
    """
    class Link : 
    for now, very simplified.
    
    :type intervals: intervalList
    :type node1/2: nodeT
    :type layerLabel1/2: str ?
    
    todo : Find a better indexing ?
    """
    def __init__(self,intervals,node1,layerLabel1,node2,layerLabel2,delta=0,directed=1,color=0):
        if directed==0:
            if node1.giveNode()>node2.giveNode():
                layerLabel1,layerLabel2=layerLabel2,layerLabel1
                node1,node2=node2,node1
        self.intervals=intervals
        self.node1=node1
        self.node2=node2
        self.layerLabel1=layerLabel1
        self.layerLabel2=layerLabel2
        self.color=color
        #intervals.printIntervals()
    
    def copy(self):
        print("copy")
        #self.intervals.printIntervals()
        liste=self.intervals.giveListOfIntervals()
        temps=IntervalList([])
        for t in liste:
            temps.addInterval(Interval(t.begining(),t.end()),tolerance=0,cond=0)
        l=Link(temps,self.node1,self.layerLabel1,self.node2,self.layerLabel2,directed=1)
        return(l)
    
    def copyReverse(self):
        liste=self.intervals.giveListOfIntervals()
        temps=IntervalList([],key=lambda interval: [-interval.end(),-interval.begining()])
        for t in liste:
            temps.addInterval(Interval(t.begining(),t.end()),tolerance=0,cond=0)
        l=Link(temps,self.node1,self.layerLabel1,self.node2,self.layerLabel2,directed=1)
        return(l)
    
    def copyShortest(self):
        liste=self.intervals.giveListOfIntervals()
        temps=IntervalList([],key=lambda interval: [interval.length(),interval.begining()])
        for t in liste:
            temps.addInterval(Interval(t.begining(),t.end()),tolerance=0,cond=0)
        l=Link(temps,self.node1,self.layerLabel1,self.node2,self.layerLabel2,directed=1)
        return(l)
        
    def giveIntervals(self):
        return(self.intervals.giveListOfIntervals())
        """
        function giveIntervals()
        from Link
        
        return the list of intervals of type SortedCollection
        """
    def giveIntervals2(self):
        return(self.intervals)
        """
        function giveIntervals()
        from Link
        
        return the list of intervals of type IntervalList
        """
    def popInterval(self,index):
        p=self.intervals.pop(index)
        return(p)
    def addInterval(self,i,tolerance=0,cond=1):
        self.intervals.addInterval(i,tolerance,cond=cond)
    def giveLength(self):
        return(self.intervals.duration())
    def giveNodes(self):
        return([self.node1,self.node2])
    def giveLayers(self):
        return([self.layerLabel1,self.layerLabel2])
    def giveLabel(self):
        return([self.node1.giveNode(),self.node2.giveNode(),self.layerLabel1,self.layerLabel2])
    def printLink(self):
        print("Link : ")
        self.node1.printNodeT()
        print(","+str(self.layerLabel1))
        print("--->")
        self.node2.printNodeT()
        print(","+str(self.layerLabel2))
        print("intervalLinks")
        self.intervals.printIntervals()
        print("endlink")
        
    

class LinkList:
    """
    class LinkList : 
    the list is sorted by the names of node1, then the name of node2, then the layer1, then Layer2.
    
    """
    
    def __init__(self,liste,key=lambda link: link.giveLabel(),directed=1):
        self.listOfLinks = SortedCollection(iterable=liste,key=key)
    
    def addLink(self,l,tolerance=0,cond=1):
        if self.listOfLinks.contains_key(l):
            i = self.listOfLinks.index_key(l)
            for inter in l.giveIntervals():
                self.listOfLinks[i].addInterval(inter,tolerance=tolerance,cond=cond)
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
    
    def length(self):
        return(self.listOfLinks.__len__())
    
    def giveIndex(self,label):
        return(self.listOfLinks.index_label(label))
    
    def countLinks(self):
        leng=0
        for i in self.listOfLinks:
            leng=leng+i.giveIntervals().__len__()
        return(leng)
    def giveListForForemost(self):
        #print("couqsdjkh")
        #self.listOfLinks[0].printLink()
        #print("jdmslfhswkdjhslwkjdhlwjdkhw")
        #print("len",len(self.listOfLinks))
        s=SortedCollection([], key=lambda link: [link.giveIntervals()[0].begining(),link.giveLabel()])
        for li in self.listOfLinks:
            #li.printLink()
            li2=li.copy()
            #print("ccccccccccccccccccccccccccccccccccccccccccccccccccc")
            #li2.printLink()
            s.insert(li2)
        print("given")
        return(s)
            
    def giveListForLastDept(self):
        s=SortedCollection([], key=lambda link: [-link.giveIntervals()[0].end(),link.giveLabel()])
        for li in self.listOfLinks:
            li2=li.copyReverse()
            s.insert(li2)
        print("given")
        return(s)
    
    def giveListForEnum(self):
        s=SortedCollection([],key=lambda link: [link.giveIntervals()[0].length(),link.giveLabel(),link.giveIntervals()[0].begining()])
        for li in self.listOfLinks:
            li.printLink()
            li2=li.copyShortest()
            li2.printLink()
            s.insert(li2)
        print("enum sorted")
        return(s)