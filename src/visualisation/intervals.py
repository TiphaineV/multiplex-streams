# -*- coding: utf-8 -*-
"""
Created on Wed May 22 14:59:05 2019

@author: Pimprenelle
"""

from sortedcollection import *

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

    def condensateIntervals(self,index=0,tolerance=0,superpos=0):
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
            if self.listOfIntervals[i].end()>=(self.listOfIntervals[i+1].begining()-tolerance):
                #print("fusion")
                #self.listOfIntervals[i].printInterval()
                #self.listOfIntervals[i+1].printInterval()
                print("condddd")
                inte=self.listOfIntervals.pop(i+1)
                self.listOfIntervals[i].setEnd(max(inte.end(),self.listOfIntervals[i].end()))
            else :
                i=i+1


    def addInterval(self,interval,tolerance=0.1,cond=1):
        #b=interval.begining()
        #self.printIntervals()
        k=self.listOfIntervals.index_key(interval)
        self.listOfIntervals.insert(interval)
        if cond==1:
            self.condensateIntervals(index=max(k-1,0),tolerance=tolerance)

    def printIntervals(self):
        print("list of intervals")
        for i in self.listOfIntervals:
            print(i.intervalToString())
   
    def intervalListToString(self):
        str=""
        for i in self.listOfIntervals:
            str=str+i.intervalToString()
        return str
    
    def isInList(self,t):
        """
            function isInList
            ====
            from IntervalList
        
            :type t: float
            
            return if t is in one of the intervals of the list
        """
        k=self.listOfIntervals.indexInsertLabel(t)
        if k==0:
            print("k=0")
            return(self.listOfIntervals[0].begining()==t)
        if k<(self.listOfIntervals).__len__():
            if self.listOfIntervals[k].begining()==t :
                return True
        else :
            return(self.listOfIntervals[k-1].isIn(t))
    
    def duration(self):
        """
            function duration
            ===
            class IntervalList
        
            return the sum of the size of the intervals.
        """
        d=0
        for i in self.listOfIntervals:
            d=d+i.length()
        return(d)
    
    def intersection(self,interList2):
        """
            function intersection
            =====
            from class IntervalList
            ---
        
            :type inuterList2: IntervalList
            
            returns the IntervalList of the intersection of all the intervals of the 2 lists.
        """
        l=IntervalList([])
        for i1 in interList2.giveListOfIntervals():
            for i2 in self.listOfIntervals:
                i3=i1.intersection(i2)
                if i3 != Interval(0,0):
                    l.addInterval(i3)
        return(l)
        
