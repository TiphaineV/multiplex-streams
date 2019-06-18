# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 15:50:10 2019

@author: Pimprenelle
"""

from visuMultiStream import *
from intervals import *
from structure import *
from elemMSGraph import *
from multiLayers import *

t0=0
tend=24*60*7

print(tend)



def convertToMinutes(day,hour,minutes):
    return((day-1)*24*60+hour*60+minutes)
    
def readCarriers():
    f=open("planes/L_UNIQUE_CARRIERS.csv","r")
    n=0
    liste=[]
    for line in f :
        if n>1:
            line=line.replace("\"",'')
            tab=line.split(",")
            tab[-1]=tab[-1].rstrip("\n")
            code=tab[0]
            name=tab[1]
            liste.append(code)
        n=n+1
    comp=Aspect("carrier",liste)
    return(comp)
    
carriers=readCarriers()

