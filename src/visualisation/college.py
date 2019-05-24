from visuMultiStream import *


#A CORRIGER : ECRITURE DES LIENS EN ENTIER...!

interval = Interval(312.2-300.,1481.2-300.)
"""
Times are taken in seconds, from 31220 to 148120.
Measures are taken each 20s.

We divide by 100 and put a 300 offset.
"""

niveau=Aspect("niveau",["1","2","3","4","5","T"])
option = Aspect("option",["A","B","e"])
sexe = Aspect("sexe",["F","M","U"])

college = LayerStruct([niveau,option,sexe])

nodelayers=[]

m=MultiStream(interval,college,LayerList([]),LinkList([]))

def readNodes():
    f= open("data/metadata_primaryschool.txt","r")
    n=0
    liste=[]
    for line in f :
        n=n+1
        tab=line.split("\t")
        #print([tab[1][0],tab[1][1],tab[2][0]])
        layer=Layer(college,[tab[1][0],tab[1][1],tab[2][0]],interval,NodeTList([NodeT(tab[0],IntervalList([interval]))]))
        m.addLayer(layer)
        liste.append([tab[0],tab[2][0]])
    f.close()
    return(liste)

def chercherSexe(liste,numero):
    i=0
    j=len(liste)
    k=0
    while i<j-1:
        k=(i+j)//2
        #print(liste[k][0],"sexe")
        if liste[k][0]>numero:
            j=k
        elif liste[k][0]<numero:
            i=k
        else:
            break
    return(liste[k][1])

def readLinks(liste):
    fl = open("data/primaryschool.csv","r")
    n=0
    for line in fl:
        n=n+1
        if n<100:
            tab=line.split("\t")
            int1=Interval((int(tab[0]))/100-300,(int(tab[0])+20)/100-300)
            node1=tab[1]
            node2=tab[2]
            layer1=[tab[3][0],tab[3][1],chercherSexe(liste,node1)]
            layer2=[tab[4][0],tab[4][1],chercherSexe(liste,node2)]
            link=Link((IntervalList([int1])),NodeT(node1,IntervalList([interval])),layer1,NodeT(node2,IntervalList([interval])),layer2)
            m.addLink(link)
            #link.printLink()
liste = readNodes()
readLinks(liste)
#m.printMS()
m.drawMS(nameFile2="college.fig")
