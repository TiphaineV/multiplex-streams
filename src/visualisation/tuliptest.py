# -*- coding: utf-8 -*-


# To cancel the modifications performed by the script
# on the current graph, click on the undo button.

from tulip import *
from math import *
from random import *
from collections import deque

# the updateVisualization() function can be called
# during script execution to update the opened views

# the main(graph) function must be defined
# to run the script on the current graph
def dfs(n, graph):
    marker = graph.getIntegerProperty("see");
    marker.setNodeValue(n, marker.getNodeValue(n) + 1)
    if (marker.getNodeValue(n) > 1):
        return
    color = graph.getColorProperty("viewColor");
    color.setNodeValue(n, tlp.Color(0, 255, 0 , 255));
    updateVisualization(False)
    for ni in graph.getInOutNodes(n):
        dfs(ni, graph)
    color.setNodeValue(n, tlp.Color(0, 128, 128 , 255));
#====================================
def bfs(n, graph):
    marker = graph.getIntegerProperty("see");
    color = graph.getColorProperty("viewColor");
    fifo = deque([])
    fifo.append(n)
    while(len(fifo) > 0):
        n = fifo.popleft()
        color.setNodeValue(n, tlp.Color(0, 128, 128 , 255));
        for ni in graph.getInOutNodes(n):
            marker.setNodeValue(ni, marker.getNodeValue(ni) + 1)
            if (marker.getNodeValue(ni) < 2):
                color.setNodeValue(ni, tlp.Color(0, 255, 0 , 255));
                fifo.append(ni);
        updateVisualization()
#========================================
def main(graph) :    
    # insert your script code here
    color = graph.getColorProperty("viewColor");
    marker = graph.getIntegerProperty("see");
    marker.setAllNodeValue(0)
    color.setAllNodeValue(tlp.Color(255,0,0,125));
    updateVisualization(False)
    bfs(graph.getOneNode(), graph);

