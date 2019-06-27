# -*- coding: utf-8 -*-
"""
Created on Tue May 21 16:26:51 2019

@author: Pimprenelle
"""

from visuMultiStream import *
from intervals import *
from structure import *
from elemMSGraph import *
from multiLayers import *


#A CORRIGER : ECRITURE DES LIENS EN ENTIER...!
t0=1385982020
scale = 500
interval = Interval(0,(1386345580-t0)/scale)
interval.printInterval()
"""
Times are taken in seconds, from 1385982020 to 1386345580.
Measures are taken each 20s.

We suppress 1385982020 to each measure of time and divide by 1000.
"""

classe=Aspect("annee",["MP","MP*1","MP*2","2BIO1","2BIO2","2BIO3","PSI*","PC","PC*"])
sexe = Aspect("sexe",["F","M","U"])
typeOfRel = Aspect("relation",["face_to_face","facebook","friendship","diaries"])

lycee = LayerStruct([typeOfRel,classe,sexe])




def readNodes(typen=["face_to_face"]):
    
    f= open("lycee/metadata_2013.txt","r")
    n=0
    liste={}
    liste2={}
    for line in f :
        n=n+1
        tab=line.split("\t")
        for ty in typen :
            layer=Layer(lycee,[ty,tab[1],tab[2][0]],interval,NodeTList([NodeT(tab[0],IntervalList([interval]))]))
            m.addLayer(layer)
        liste[tab[0]]=tab[2][0]
        liste2[tab[0]]=tab[1]
    f.close()
    return(liste,liste2)

def chercherAttribut(liste,numero):
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
    fl = open("lycee/High-School_data_2013.csv","r")
    n=0
    ni=[0]
    ti=[0]
    for line in fl:
        n=n+1
        if n<200000:
            tab=line.split(" ")
            tab[4]=tab[4].rstrip('\n')
            int1=Interval((int(tab[0])-t0)/scale,(int(tab[0])+20-t0)/scale)
            node1=tab[1]
            node2=tab[2]
            c1=tab[3]
            c2 = tab[4]
            layer1=["face_to_face",c1,liste[node1]]
            layer2=["face_to_face",c2,liste[node2]]
            link=Link((IntervalList([int1])),NodeT(node1,IntervalList([interval])),layer1,NodeT(node2,IntervalList([interval])),layer2)
            m.addLink(link,tolerance=0.2)
            #link.printLink()
            t=int1.begining()
            if ti[len(ti)-1]==t:
                ni[len(ti)-1]=ni[len(ti)-1]+1
            else:
                ti.append(t)
                ni.append(1)
    return(ti,ni)


def readLinks2(liste,liste2):
    fl = open("lycee/Facebook-known-pairs_data_2013.csv")
    n= 0
    print("readlink2...")
    for line in fl:
        n=n+1
        if n<1000000000000:
            tab=line.split(" ")
            tab[2]=tab[2].rstrip('\n')
            #print(tab)
            if tab[2]=='1':
                node1=tab[0]
                node2=tab[1]
                layer1=["facebook",liste2[node1],liste[node1]]
                layer2=["facebook",liste2[node2],liste[node2]]
                I=IntervalList([interval])
                link=Link(I,NodeT(node1,I),layer1,NodeT(node2,I),layer2)
                m.addLink(link)
                #print("linkfb")
                #link.printLink()

def readLinks3(liste,liste2):
    fl= open("lycee/Friendship-network_data_2013.csv")
    n=0
    print("readlink3...")
    for line in fl:
        n=n+1
        if n<1000000000000:
            tab=line.split(" ")
            tab[1]=tab[1].rstrip('\n')
            print(tab)
            node1=tab[0]
            node2=tab[1]
            layer1=["friendship",liste2[node1],liste[node1]]
            layer2=["friendship",liste2[node2],liste[node2]]
            I=IntervalList([interval])
            link=Link(I,NodeT(node1,I),layer1,NodeT(node2,I),layer2)
            m.addLink(link)
    print("link3done")

def layerWithCommonPoint(layerStruct,aspect,elemLayer):
    liste=[[]]
    i=0
    ind=0
    for asp in layerStruct.giveAspects() :
        if asp.nameAspect()==aspect :
            i=ind
        else:
            ind=ind+1
    j=0
    for asp in layerStruct.giveAspects() :
        print(len(liste))
        for k in range(len(liste)-1,-1,-1):
            a=liste.pop(k)
            for elemLayeri in asp.giveElemLayer():
                if j==i:
                    if elemLayeri==elemLayer:
                         a.append(elemLayeri)
                         liste.append(a)
                         a=a.copy()
                         a.pop()
                else:
                    a.append(elemLayeri)
                    liste.append(a)
                    a=a.copy()
                    a.pop()
        j=j+1
    return(liste)

def densityHourPerHour(multistream,step):
    inte=multistream.interval()
    b=inte.begining()
    e=inte.end()
    dlist=[]
    tlist=[]
    while b<e :
        print(b)
        mext=m.cut(Interval(b,b+step))
        tlist.append(b)
        dlist.append(mext.computeDensity())
        b=b+step
    return(tlist,dlist)



m=MultiStream(interval,lycee,LayerList([]),LinkList([]))

liste,liste2 = readNodes()
ti,ni=readLinks(liste)
#readLinks2(liste,liste2)
#readLinks3(liste,liste2)



#
mp=layerWithCommonPoint(lycee,"annee","MP")


#llfb=layerWithCommonPoint(lycee,"relation","facebook")
#llfs=layerWithCommonPoint(lycee,"relation","friendship")
#
#llf=layerWithCommonPoint(lycee, "sexe", "F")
#llh = layerWithCommonPoint(lycee,"sexe","M")
#
#
#m=m.extractLayers(mp)
#m=m.cut(Interval(0,40))

m.printNodes()

aretesordo=m.computeLengthEm(layer=["face_to_face","MP","U"])
#print(m.ordreAretes(layer=["face_to_face","MP","U"]))
print("ordre")
o=m.ordreAretes(layer=['face_to_face','MP','U'])

for i in aretesordo:
    print(m.giveLinks().giveListOfLinks()[i[1]].printLink())


for n in o:
    n.printNodeT()
    
m.drawMS("drawordomp.fig")

#dessin
#axes = plt.gca()
#axes.grid(True)
#axes.xaxis.set_ticks(range(0, 750, 10), minor = True)
#axes.xaxis.grid(True, which = 'both', color = 'red', zorder = 0)
#plt.gcf().set_size_inches(20, 20)
#plt.plot(ti,ni)
#plt.show()



#readLinks2(liste,liste2)

#llftf = layerWithCommonPoint(lycee, "relation", "face_to_face")
"""
m1=m.cut(Interval(0,40))
m2=m.cut(Interval(140,210))
m3=m.cut(Interval(315,380))
m4=m.cut(Interval(490,560))
m5=m.cut(Interval(660,730))






dhommes=[]
dfemmes=[]
dinter=[]
dtot=[]

dmlhL=[]
dmlfL=[]
dmlL=[]
dmlhfL=[]

print("number of nodes=",m.numberOfNodeLayers())
print("number of womens=",m.extractLayers(llf).numberOfNodeLayers())
print("number of mens",m.extractLayers(llh).numberOfNodeLayers())




#jour1
mu=m1

mf=mu.extractLayers(llf)
mh=mu.extractLayers(llh)
mhf=mu.interLayers(llh,llf)


df=mf.computeDensity()
dh=mh.computeDensity()



print("j1 nn", mf.numberOfNodeLayers())

dhf = mhf.computeDensityBiparti(llf,llh)
#
dtt=mu.computeDensity()

print("jour1")
print("densite totale",dtt)

print("femmes",df)
print("hommes",dh)
print("femmes/hommes",dhf)

print("fml",)

dhommes.append(dh)
dfemmes.append(df)
dinter.append(dhf)
dtot.append(dtt)


mlf=mf.extractML()
mlh=mh.extractML()
ml=mu.extractML()
mlhf=mhf.extractML()

dmlhf=mlhf.computeDensityMultiBiparti(llf,llh)
dmlf=mlf.computeDensityMulti()
dmlh=mlh.computeDensityMulti()
dml=ml.computeDensityMulti()

print("interval",mu.interval().intervalToString(),mu.interval().printInterval())

dmlhfL.append(dmlhf)
dmlfL.append(dmlf)
dmlhL.append(dmlh)
dmlL.append(dml)

ml.drawML()

#jour 2
mu=m2

mf=mu.extractLayers(llf)
mh=mu.extractLayers(llh)
mhf=mu.interLayers(llh,llf)


df=mf.computeDensity()
dh=mh.computeDensity()
#
dhf = mhf.computeDensityBiparti(llf,llh)
#
dtt=mu.computeDensity()

print("jour2")
print("densite totale",dtt)

print("femmes",df)
print("hommes",dh)
print("femmes/hommes",dhf)

dhommes.append(dh)
dfemmes.append(df)
dinter.append(dhf)
dtot.append(dtt)

mlf=mf.extractML()
mlh=mh.extractML()
ml=mu.extractML()
mlhf=mhf.extractML()

dmlhf=mlhf.computeDensityMultiBiparti(llf,llh)
dmlf=mlf.computeDensityMulti()
dmlh=mlh.computeDensityMulti()
dml=ml.computeDensityMulti()

dmlhfL.append(dmlhf)
dmlfL.append(dmlf)
dmlhL.append(dmlh)
dmlL.append(dml)

ml.drawML()
#
#
#jour 3
mu=m3

mf=mu.extractLayers(llf)
mh=mu.extractLayers(llh)
mhf=mu.interLayers(llh,llf)


df=mf.computeDensity()
dh=mh.computeDensity()
#
dhf = mhf.computeDensityBiparti(llf,llh)
#
dtt=mu.computeDensity()
#
#
#multi.drawML("mhf")
#
print("jour3")
print("densite totale",dtt)

print("femmes",df)
print("hommes",dh)
print("femmes/hommes",dhf)

dhommes.append(dh)
dfemmes.append(df)
dinter.append(dhf)
dtot.append(dtt)

mlf=mf.extractML()
mlh=mh.extractML()
ml=mu.extractML()
mlhf=mhf.extractML()

dmlhf=mlhf.computeDensityMultiBiparti(llf,llh)
dmlf=mlf.computeDensityMulti()
dmlh=mlh.computeDensityMulti()
dml=ml.computeDensityMulti()

dmlhfL.append(dmlhf)
dmlfL.append(dmlf)
dmlhL.append(dmlh)
dmlL.append(dml)


#jour 4
mu=m4

mf=mu.extractLayers(llf)
mh=mu.extractLayers(llh)
mhf=mu.interLayers(llh,llf)


df=mf.computeDensity()
dh=mh.computeDensity()
#
dhf = mhf.computeDensityBiparti(llf,llh)
#
dtt=mu.computeDensity()
#
#
#multi.drawML("mhf")
#
print("jour4")
print("densite totale",dtt)

print("femmes",df)
print("hommes",dh)
print("femmes/hommes",dhf)

dhommes.append(dh)
dfemmes.append(df)
dinter.append(dhf)
dtot.append(dtt)

mlf=mf.extractML()
mlh=mh.extractML()
ml=mu.extractML()
mlhf=mhf.extractML()

dmlhf=mlhf.computeDensityMultiBiparti(llf,llh)
dmlf=mlf.computeDensityMulti()
dmlh=mlh.computeDensityMulti()
dml=ml.computeDensityMulti()

dmlhfL.append(dmlhf)
dmlfL.append(dmlf)
dmlhL.append(dmlh)
dmlL.append(dml)


#jour 5
mu=m5

mf=mu.extractLayers(llf)
mh=mu.extractLayers(llh)
mhf=mu.interLayers(llh,llf)


df=mf.computeDensity()
dh=mh.computeDensity()
#
dhf = mhf.computeDensityBiparti(llf,llh)
#
dtt=mu.computeDensity()
#
#
#multi.drawML("mhf")
#
print("jour5")
print("densite totale",dtt)

print("femmes",df)
print("hommes",dh)
print("femmes/hommes",dhf)

dhommes.append(dh)
dfemmes.append(df)
dinter.append(dhf)
dtot.append(dtt)

mlf=mf.extractML()
mlh=mh.extractML()
ml=mu.extractML()
mlhf=mhf.extractML()

dmlhf=mlhf.computeDensityMultiBiparti(llf,llh)
dmlf=mlf.computeDensityMulti()
dmlh=mlh.computeDensityMulti()
dml=ml.computeDensityMulti()

dmlhfL.append(dmlhf)
dmlfL.append(dmlf)
dmlhL.append(dmlh)
dmlL.append(dml)


t=[1,2,3,4,5]
#plt.figure(figsize=(15,10))
lh=plt.plot(t,dhommes,"r--",label='hommes')
plt.plot(t,dfemmes,"bs", label='femmes')
plt.plot(t,dinter,"g^",label='inter femmes/hommes')
plt.plot(t,dtot,'k',label='total')
plt.legend()
plt.show()

print("multilayer")

lh=plt.plot(t,dmlhL,"r--",label='hommes')
plt.plot(t,dmlfL,"bs", label='femmes')
plt.plot(t,dmlhfL,"g^",label='inter femmes/hommes')
plt.plot(t,dmlL,'k',label='total')
plt.legend()
plt.show()
"""
#
#print("ftf")
#mftf= m.extractLayers(llftf)
#
#
#tabf=[]
#tabh=[]
#tabhf=[]
#tabtot=[]
#
#tabtot.append(mftf.computeDensity())
#tabf.append(mftf.extractLayers(llf).computeDensity())
#tabh.append(mftf.extractLayers(llh).computeDensity())
#tabhf.append(mftf.interLayers(llf,llh).computeDensityBiparti(llf,llh))
#
#print("llfb")
#mfb=m.extractLayers(llfb)
#
#mfb.printNodes()
#
#tabtot.append(mfb.computeDensity())
#tabf.append(mfb.extractLayers(llf).computeDensity())
#tabh.append(mfb.extractLayers(llh).computeDensity())
#tabhf.append(mfb.interLayers(llf,llh).computeDensityBiparti(llf,llh))
#
#print("friendship")
#mfs = m.extractLayers(llfs)
#
#mfsl=mfs.extractML()
#
#mfsl.drawML()
#
#tabtot.append(mfs.computeDensity())
#tabf.append(mfs.extractLayers(llf).computeDensity())
#tabh.append(mfs.extractLayers(llh).computeDensity())
#tabhf.append(mfs.interLayers(llf,llh).computeDensityBiparti(llf,llh))
#
#t=["face to face","facebook","friendship"]
#
#plt.yscale('log')
#lh=plt.plot(t,tabh,"r--",label='hommes')
#plt.plot(t,tabf,"bs", label='femmes')
#plt.plot(t,tabhf,"g^",label='inter femmes/hommes')
#plt.plot(t,tabtot,'k',label='total')
#plt.legend()
#plt.show()