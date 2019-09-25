# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 10:16:32 2019

@author: Pimprenelle
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from pylab import *

def normaliser(mat):
    s=[]
    n=len(mat)
    matrice=mat.copy()
    for i in range(n):
        sommel=0
        for j in range(n):
            sommel=sommel+matrice[i][j]
        print("somm",sommel)
        s.append(sommel)
        for j in range(n):
            matrice[i][j]=matrice[i][j]/sommel
    plt.plot(s,'ro')
    plt.show()
    print(s)
    return([matrice,s])
    
def valeurPropreMax(matrice,iterations):
    """
        Compute the maximum eigenvalue and its eigenvector of matrice.
        the more iterations is high, the more accurate is the result.
    """
    n=len(matrice)
    x=np.transpose(np.array([1 for i in range(n)]))
    A=np.copy(matrice)
    for i in range(iterations):
        x=np.dot(A,x)
        x=x/np.linalg.norm(x,2)
    valp=np.linalg.norm(np.dot(A,x),2)/np.linalg.norm(x,2)
    return(valp,x)

def compareOrders(vect1,vect2):
    v=[]
    x=linspace(0,len(vect1),len(vect1))
    for i in range(len(vect1)):
        v.append(vect2.index(vect1[i]))
    plt.plot(vect1,v,'o')
    plt.plot(x)
    plt.show()