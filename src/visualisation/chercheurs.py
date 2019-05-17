from visuMultiStream import *


int1 = Interval(0,10)
int2 = Interval(11,15)
int3 = Interval(9,13)
int5= Interval(5,8)
int6=Interval(20,25)
int4 = int3.intersection(int1)
int1.contains(int5)

listOf=[int1,int2,int3,int4,int5,int6]
l=sortIntervals(listOf)

printListIntervals(listOf)
condensateIntervals(listOf)
printListIntervals(listOf)
addInterval(listOf,Interval(18.3,19))
printListIntervals(listOf)


uni = Aspect("Université",["Polytechnique","Todai","Paris6"] )
dept = Aspect("departement",["mathematiques","biologie","informatique","mecanique"])
poste = Aspect("Poste",["stagiaire","these","post-doc","chercheur"])
print(uni.nameAspect())
print(uni.listElemLayer())
dept.printAspect()
print(dept.aspectToString())

layers = Layers([uni,dept])
layers.addAspect(poste)
print("***************layers : *****************")
layers.printLayers()
print("*************end***************")
listeLayers = layers.buildLayer()
#print(listeLayers)
layerT=layers.buildLayerT(Interval(0,10))
#for l in layerT :
 #   l.printLayerT()

layT = layerT.pop()
layT.printLayerT()
n=NodeLayerT("chercheurA",layT,[Interval(0,11),Interval(3,4),Interval(1,2),Interval(6,9)])
n.printNodeLayerT()
#n.addtime([Interval(5,6),Interval(4,7)])
n.printNodeLayerT()

m=MultiStream(Interval(0,10),["p1","p2"],layers)
nlt=NodeLayerT("p1",layT,[Interval(6,7)])
nlt2=NodeLayerT("p2",layT,[Interval(6,9)])
m.addNodeLayerT(nlt)
m.addNodeLayerT(nlt2)
m.addLink(Link(nlt,nlt2,Interval(6,7)))
m.printMS()

m.draw(nameFile2="chercheurs.fig")
