# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 10:16:32 2019

@author: Pimprenelle
"""
import matplotlib
import matplotlib.pyplot as plt

def normaliser(matrice):
    s=[]
    n=len(matrice)
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
    return(matrice)