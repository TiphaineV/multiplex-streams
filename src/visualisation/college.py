from visuMultiStream import *


#A CORRIGER : ECRITURE DES LIENS EN ENTIER...!

interval = Interval(8.67,41.14)
"""
j'ai divisé le temps par 3600
"""

niveau=Aspect("niveau",["1","2","3","4","5","T"])#T:teacher
option = Aspect("option",["A","B","e"])#e:teacher
sexe = Aspect("sexe",["F","M","U"])#U: unknown

college = LayerStruct([niveau,option,sexe])

m=MultiStream(interval,college,LayerList([]),[])

#m=MultiStream(interval,[],college)

def readNodes():
    f= open("data/metadata_primaryschool.txt","r")
    n=0
    liste=[]
    for line in f :
        n=n+1
        tab=line.split("\t")
        indiv=int(tab[0])
        niv = tab[1][0]
        opt= tab[1][1]
        sex = tab[2][0]
        node=NodeT(indiv,IntervalList([interval]))
        layer=Layer(college,[niv,opt,sex],interval,NodeTList([node]),checkCorrectL="True", checkCorrectN="True")
        m.addLayer(layer)
        #layert=LayerT([tab[1][0],tab[1][1],tab[2][0]],interval)
        #nodelayert=NodeLayerT(tab[0],layert,[interval])
        #m.addNode(tab[0])
        #m.simpleAddNodeLayerT(nodelayert)
        liste.append([int(tab[0]),tab[2][0]])
    f.close()
    return(liste)



def chercherSexe(liste,numero):
    i=0
    j=len(liste)
    while i<j-1:
        k=(i+j)//2
        #print(liste[k][0],"sexe")
        if liste[k][0]>numero:
            j=k
        elif liste[k][0]<numero:
            i=k
        else:
            return(k)
    return("error : not found")

def readLinks(liste):
    fl = open("data/primaryschool.csv","r")
    n=0
    for line in fl:
        n=n+1
        if n<10:
            tab=line.split("\t")
            int1=Interval((int(tab[0])-20)/3600,int(tab[0])/3600)
            labNode1=int(tab[1])
            labNode2=int(tab[2])
            layerLabel1 = [tab[3][0],tab[3][1],chercherSexe(liste,labNode1)]
            layerLabel2 = [tab[4][0],tab[4][1],chercherSexe(liste,labNode2)]
            m.addLink(Link(interval,NodeT(labNode1,IntervalList([interval])),layerLabel1,NodeT(labNode2,IntervalList([interval])),layerLabel2))
            

liste = readNodes()
readLinks(liste)
m.printMS()
m.drawMS(nameFile2="college2.fig")
