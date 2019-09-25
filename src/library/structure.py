# -*- coding: utf-8 -*-
"""
Created on Wed May 22 15:01:22 2019

@author: Pimprenelle
"""


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
    def giveAspects(self):
        return(self.aspects)
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