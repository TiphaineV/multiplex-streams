# coding: utf-8
# TODO
# Nettoyage vieux code / Commentaires code
# Documentation
# Remplacer les self.f.writelines("\n"+...\n)
# Gestion des erreurs (noeud non ajout�...)


#l'aspect discret n'est pas géré pour le multilayer
import sys


def drange(start, stop, step):
    r = start
    while r <= stop:
        yield r
        r += step

class Drawing:

    alpha = 0.0
    omega = 0.0
    discrete = -1

    time_unit = 500
    node_unit = 600
    offset_x = 3450
    offset_y = 2250

    num_node_intervals = 0
    #�Is incremented by one if time marks are used too
    num_time_intervals = 0
    num_parameters = 0
    totalval_parameters = 0

    first_node = ""

    nodes = {}
    node_cpt = 1
    
    layers={}
    layer_cpt=1
    
    colors = {}
    color_cpt = 31


    def __init__(self, alpha=0.0, omega=10.0, time_width=500, discrete=0,nameFile="default"):
        self.f= open(nameFile,"w")
        self.f.writelines("#FIG 3.2  Produced by xfig version 3.2.5b\n\
Landscape\n\
Center\n\
Inches\n\
Letter\n\
100.00\n\
Single\n\
-2\n\
1200 2\n""")

        self.alpha = float(alpha)
        self.omega = float(omega)
        self.time_unit = time_width
        self.discrete = discrete

        self.linetype = 2

        # Useful predefined colors
        self.addColor("grey", "#888888")



    def setLineType(def_linetype):
        self.linetype = def_linetype

    def addColor(self, name, hex):
        self.color_cpt += 1
        self.colors[name] = self.color_cpt

        self.f.writelines("\n"+"0 " + str(self.color_cpt) + " " + str(hex))

    def addNode(self, u, times=[], color=0, linetype=None,layer="layer0",newLayer=0,write=""):
        if self.discrete > 0:
            self.addDiscreteNode(u,layer, times, color)
        else:
            self.addContinuousNode(u,layer, newLayer, write, times, color, linetype)

    def addDiscreteNode(self, u, times=[], color="grey", width=1):

        if color in self.colors:
            color = self.colors[color]

        if self.node_cpt == 1:
            self.first_node = u

        self.node_cpt += 1
        self.nodes[u] = self.node_cpt

        self.f.writelines("\n"+"4 0 " + str(color) + " 50 -1 0 30 0.0000 4 135 120 " + str(self.offset_x + int(self.alpha * self.time_unit) - 400) + " " + str(self.offset_y + 125 + int(self.node_cpt * self.node_unit)) + " " + str(u) + "\\001")


        if len(times) == 0:
            for i in drange(self.alpha, self.omega, self.discrete):
                self.f.writelines("\n"+"1 3 0 " + str(width) + " " + str(color) + " " + str(color) + " 49 -1 20 0.000 1 0.0000 " + str(self.offset_x + int(i * self.time_unit)) + " " + str(self.offset_y + self.nodes[u]*self.node_unit) + " 45 45 -6525 -2025 -6480 -2025")
        else:
            for (i,j) in times:
                for x in drange(i, j, self.discrete):
                    self.f.writelines("\n"+"1 3 0 " + str(width) + " " + str(color) + " " + str(color) + " 49 -1 20 0.000 1 0.0000 " + str(self.offset_x + int(x * self.time_unit)) + " " + str(self.offset_y + self.nodes[u]*self.node_unit) + " 45 45 -6525 -2025 -6480 -2025")



    def addContinuousNode(self, u, layer, newLayer,write, times=[], color=0, linetype=None):
        """ nodeId : identifiant du noeud
            times : suite d'intervalles de temps ou le noeud est actif
            layer : etiquette de la layer en string
            newLayer : indique si on passe à une nouvelle layer
        """

        if linetype is None:
            linetype = self.linetype

        if color in self.colors:
            color = self.colors[color]

        if self.node_cpt == 1:
            self.first_node = u

        self.node_cpt += 1
        self.layer_cpt += newLayer # = 0 if the layer is not new, 1 if the layer is new
        
        self.nodes[u+layer] = self.node_cpt
        self.layers[layer] = self.layer_cpt
        
        if write!="":
            u=write
        
        sizestr = len(u)
        sizeLayer=len(str(layer))
        
        self.f.writelines("\n"+"4 0 " + str(color) + " 50 -1 0 10 0.0000 4 135 120 " + str(self.offset_x + int(self.alpha * self.time_unit) - 100*sizestr) + " " + str(self.offset_y + 125 + int(self.node_cpt * self.node_unit)+int(self.layer_cpt * self.node_unit)) + " " + str(u) + "\\001")
        
        if newLayer :
            self.f.writelines("\n"+"4 0 " + str(color) + " 50 -1 0 10 0.0000 4 135 120 " + str(self.offset_x + int(self.alpha * self.time_unit) - 100*sizeLayer) + " " + str(self.offset_y + 125 + int((self.node_cpt -1)* self.node_unit) +int(self.layer_cpt * self.node_unit)) + " " + str(layer) + "\\001")
        
        if len(times) == 0:
            self.f.writelines("\n"+"""2 1 """ + str(linetype) + """ 2 """ + str(color) + """ 7 50 -1 -1 6.000 0 0 7 0 0 2\n \
          """ + str(self.offset_x + int(self.alpha * self.time_unit)) + """ """ + str(self.offset_y + int(self.node_cpt * self.node_unit)) + """ """ + str(self.offset_x + int(self.omega * self.time_unit)) + """ """ + str(self.offset_y + int(self.node_cpt * self.node_unit)))
        else:
            for (i,j) in times:
                self.f.writelines("\n"+"""2 1 """ + str(linetype) + """ 2 """ + str(color) + """ 7 50 -1 -1 6.000 0 0 7 0 0 2\n \
          """ + str(self.offset_x + int(i* self.time_unit)) + """ """ + str(self.offset_y + int(self.node_cpt * self.node_unit)++int(self.layer_cpt * self.node_unit)) + """ """ + str(self.offset_x + int(j * self.time_unit)) + """ """ + str(self.offset_y + int(self.node_cpt * self.node_unit)++int(self.layer_cpt * self.node_unit)))

   #def printLayer(self,layerLabel):
    #    self.f.writelines("\n"+"4 0 " + str(color) + " 50 -1 0 12 0.0000 4 135 120 " + str(self.offset_x + int(self.alpha * self.time_unit) - 100*sizestr) + " " + str(self.offset_y + 125 + int(self.node_cpt * self.node_unit)) + " " + str(layerLabel) + "\\001")
    
    
    def addLink(self, u, v, b, e, curving=0.0, color=0, height=0.5, width=3, layer1="layer0", layer2="layer0"):
        if self.discrete > 0:
            self.addDiscreteLink(u, v, b, e, curving, color, height, width)
        else:
            self.addContinuousLink(u, v, layer1,layer2, b, e, curving, color, height, width)

    def addDiscreteLink(self, u, v, b, e, curving=0.0, color=0, height=0.5, width=3):
        if color in self.colors:
            color = self.colors[color]
        if self.nodes[u] > self.nodes[v]:
            (u,v) = (v,u)
        for i in drange(b,e, self.discrete):
            # Draw circles for u and v
            self.f.writelines("\n"+"1 3 0 " + str(width) + " " + str(color) + " " + str(color) + " 49 -1 20 0.000 1 0.0000 " + str(self.offset_x + int(i * self.time_unit)) + " " + str(self.offset_y + self.nodes[u]*self.node_unit) + " 45 45 -6525 -2025 -6480 -2025")
            self.f.writelines("\n"+"1 3 0 " + str(width) + " " + str(color) + " " + str(color) + " 49 -1 20 0.000 1 0.0000 " + str(self.offset_x + int(i * self.time_unit)) + " " + str(self.offset_y + self.nodes[v]*self.node_unit) + " 45 45 -6525 -2025 -6480 -2025")

            # Link them
            x1, y1 = self.offset_x + int(i * self.time_unit), self.offset_y + self.nodes[u]*self.node_unit
            x2 = self.offset_x + int((i + curving) * self.time_unit)
            y2 = int((self.offset_y + self.nodes[v]*self.node_unit) - 0.5 * (self.nodes[v]-self.nodes[u]) * self.node_unit)
            x3 = self.offset_x + int(i * self.time_unit)
            y3 = self.offset_y + self.nodes[v]*self.node_unit

            sys.stdout.write("3 2 0 " + str(width) + " " + str(color) + " 7 50 -1 -1 0.000 0 0 0 3\n")
            sys.stdout.write("%s %s %s %s %s %s\n" % (x1, y1, x2, y2, x3, y3))
            sys.stdout.write("0.000 -1.000 0.000\n")



            #self.f.writelines("\n 3 2 0 " + str(width) + " " + str(color) + " 7 50 -1 -1 0.000 0 0 0 3\n")
            #self.f.writelines(" %s %s %s %s %s %s\n" % (x1, y1, x2, y2, x3, y3))
            #self.f.writelines(" 0.000 -1.000 0.000\n")
            numnodes = abs(self.nodes[u] - self.nodes[v])


    def addContinuousLink(self, u, v,layer1,layer2, b, e, curving=0.0, color=0, height=0.5, width=3):
        if color in self.colors:
            color = self.colors[color]
        #print("dictionnaire",self.nodes)
        if self.nodes[u+layer1] > self.nodes[v+layer2]:
            (u,v) = (v,u)
            (layer1,layer2)=(layer2,layer1)
        # Draw circles for u and v
       # print("ajout")
        self.f.writelines("\n"+"1 3 0 " + str(width) + " " + str(color) + " " + str(color) + " 49 -1 20 0.000 1 0.0000 " + str(self.offset_x + int(b * self.time_unit)) + " " + str(self.offset_y + self.nodes[u+layer1]*self.node_unit +int(self.layers[layer1] * self.node_unit) ) + " 45 45 -6525 -2025 -6480 -2025")
        self.f.writelines("\n"+"1 3 0 " + str(width) + " " + str(color) + " " + str(color) + " 49 -1 20 0.000 1 0.0000 " + str(self.offset_x + int(b * self.time_unit)) + " " + str(self.offset_y + self.nodes[v+layer2]*self.node_unit + int(self.layers[layer2] * self.node_unit)) + " 45 45 -6525 -2025 -6480 -2025")

        # Link them
        x1 = self.offset_x + int(b * self.time_unit)
        y1 = self.offset_y + self.nodes[u+layer1]*self.node_unit + self.layers[layer1]*self.node_unit
        x2 = self.offset_x + int((b + curving) * self.time_unit)
        y2 = int((self.offset_y + self.nodes[v+layer2]*self.node_unit + self.layers[layer2]*self.node_unit) - 0.5 * (self.nodes[v+layer2]+ self.layers[layer1]-self.nodes[u+layer1]-self.layers[layer1]) * self.node_unit)
        x3 = self.offset_x + int(b * self.time_unit)
        y3 = self.offset_y + self.nodes[v+layer2]*self.node_unit+ self.layers[layer2]*self.node_unit
        

        #sys.stdout.write("\n 3 2 0 " + str(width) + " " + str(color) + " 7 50 -1 -1 0.000 0 0 0 3\n")
        #sys.stdout.write("%s %s %s %s %s %s\n" % (x1, y1, x2, y2, x3, y3))
        #sys.stdout.write("0.000 -1.000 0.000\n")

        self.f.writelines("\n 3 2 0 " + str(width) + " " + str(color) + " 7 50 -1 -1 0.000 0 0 0 3\n")
        self.f.writelines(str(x1)+" "+ str(y1)+" "+str( x2)+" "+ str(y2)+" "+ str(x3)+" "+str(y3)+"\n")
        self.f.writelines("0.000 -1.000 0.000\n")

        numnodes = abs(self.nodes[u+layer1]+self.layers[layer1] - self.nodes[v+layer2]-self.layers[layer2])

        # Add duration
        self.f.writelines("\n"+"2 1 0 " + str(width) + " " + str(color) + " 7 50 -1 -1 0.000 0 0 -1 0 0 2")
        self.f.writelines("\n"+str(self.offset_x + int((b + curving) * self.time_unit)) + " " + str(self.offset_y + int(self.nodes[u+layer1]*self.node_unit +self.layers[layer1]*self.node_unit + (numnodes*self.node_unit*height))) + " " + str(self.offset_x + int(e * self.time_unit)) + " " + str(self.offset_y + (self.nodes[v+layer2]+self.layers[layer2])*self.node_unit - (numnodes*self.node_unit*(1-height))))

    def addNodeCluster(self, u, times=[], color=0, width=200):

        margin = int(width / 2)

        if color in self.colors:
            color = self.colors[color]

        if len(times) == 0:
            times = [(self.alpha, self.omega)]

        for (i,j) in times:
            (x1, y1) = ( self.offset_x + int(i * self.time_unit), self.offset_y + int(self.nodes[u]*self.node_unit) - margin )
            (x2, y2) = ( self.offset_x + int(j * self.time_unit), self.offset_y + int(self.nodes[u]*self.node_unit) - margin )
            (x3, y3) = ( self.offset_x + int(j * self.time_unit), self.offset_y + int(self.nodes[u]*self.node_unit) + margin )
            (x4, y4) = ( self.offset_x + int(i*self.time_unit), self.offset_y + int(self.nodes[u]*self.node_unit) + margin )

            self.f.writelines("\n"+"2 2 0 0 0 " + str(color) + " 51 -1 20 0.000 0 0 -1 0 0 5")
            self.f.writelines("\n"+str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2) + " " + str(x3) + " " + str(y3) + " " + str(x4) + " " + str(y4) + " " + str(x1) + " " + str(y1))

    def addParameter(self, letter, value, color=0, width=1):
        if color in self.colors:
            color = self.colors[color]

        #�Place at top? Confusing with time intervals...
        pos_segment_y = self.offset_y + (self.nodes[self.first_node] * self.node_unit) - (150 * self.num_time_intervals) - 400
        # Place at bottom instead? Then needs to be written last.
        # pos_segment_y = self.offset_y + self.node_cpt * self.node_unit + 2*self.node_unit

        if self.num_parameters == 0:
            paramoffset = 0
        else:
            paramoffset = 200

        self.f.writelines("\n"+"2 1 " + str(color) + " " + str(width) + " 0 7 50 -1 -1 0.000 0 0 -1 1 1 2")
        self.f.writelines("\n"+"13 1 1.00 60.00 120.00")
        self.f.writelines("\n"+"13 1 1.00 60.00 120.00")
        self.f.writelines("\n"+str(self.offset_x + (self.totalval_parameters * self.time_unit  + (self.num_parameters * paramoffset))) + " " + str(pos_segment_y) + " " + str(self.offset_x + int(value * self.time_unit) + (self.totalval_parameters * self.time_unit + (self.num_parameters * paramoffset))) + " " + str(pos_segment_y))

        valtocenter = int(value * self.time_unit / 2) - (200 + (50 * max(int(value) - 2, 0)))

        self.f.writelines("\n"+"4 0 0 50 -1 32 14 0.0000 4 180 375 " + str(self.offset_x + (self.totalval_parameters * self.time_unit + int(self.num_parameters * paramoffset)) + valtocenter)  + " " + str(pos_segment_y - 150)  + " " + str(letter) + " = " + str(value) + "\\001")
        self.totalval_parameters += value
        self.num_parameters += 1

    def addNodeIntervalMark(self, u, v, color=0, width=1):
        if color in self.colors:
            color = self.colors[color]

        pos_segment_x = self.offset_x - (150 * self.num_node_intervals) - 600

        self.f.writelines("\n"+"2 1 " + str(color) + " " + str(width) + " 0 7 50 -1 -1 0.000 0 0 -1 1 1 2")
        self.f.writelines("\n"+"13 1 1.00 60.00 120.00")
        self.f.writelines("\n"+"13 1 1.00 60.00 120.00")
        self.f.writelines("\n"+str(pos_segment_x) + " " + str(self.offset_y + self.nodes[u] * self.node_unit) + " " + str(pos_segment_x) + " " + str(self.offset_y + self.nodes[v] * self.node_unit))
        self.num_node_intervals += 1


    def addTimeNodeMark(self, t, v, color=0, width=2, depth=49):
        if color in self.colors:
            color = self.colors[color]

        self.f.writelines("\n"+"2 1 0 "+ str(width) + " " + str(color) + " 7 " + str(depth) + " -1 -1 0.000 0 0 -1 0 0 2")
        self.f.writelines("\n"+str(self.offset_x + int(t * self.time_unit) - 50 ) + " " + str(self.offset_y + self.nodes[v]*self.node_unit - 50) + " " + str(self.offset_x + int(t * self.time_unit) + 50 ) + " " + str(self.offset_y + self.nodes[v]*self.node_unit + 50))

        self.f.writelines("\n"+"2 1 0 "+ str(width) + " " + str(color) + " 7 " + str(depth) + " -1 -1 0.000 0 0 -1 0 0 2")
        self.f.writelines("\n"+str(self.offset_x + int(t * self.time_unit) - 50 ) + " " + str(self.offset_y + self.nodes[v]*self.node_unit + 50) + " " + str(self.offset_x + int(t * self.time_unit) + 50 ) + " " + str(self.offset_y + self.nodes[v]*self.node_unit - 50))

    def addTimeIntervalMark(self, b, e, color=0, width=1):
        pos_segment_y = self.offset_y + (self.nodes[self.first_node] * self.node_unit) - (100 * self.num_time_intervals) - 200

        self.f.writelines("\n"+"2 1 0 1 0 7 50 -1 -1 0.000 0 0 -1 1 1 2")
        self.f.writelines("\n"+"13 1 1.00 60.00 120.00")
        self.f.writelines("\n"+"13 1 1.00 60.00 120.00")
        self.f.writelines("\n"+str(self.offset_x + b * self.time_unit) + " " + str(pos_segment_y) + " " + str(self.offset_x + (e * self.time_unit)) + " " + str(pos_segment_y))
        self.num_time_intervals += 1

    def addPath(self, path, start, end, gamma=0, color=0, width=1, depth=51):

        if color in self.colors:
            color = self.colors[color]

        t0 = path[0][0]
        u0 = path[0][1]
        xi = self.offset_x + int(start * self.time_unit)
        yi = self.offset_y + self.nodes[u0] * self.node_unit

        xj = self.offset_x + int((t0) * self.time_unit)
        yj = self.offset_y + self.nodes[u0] * self.node_unit


        coords = [(xi,yi), (xj,yj)]

        for (t,u,v) in path:
            xi = self.offset_x + int(t * self.time_unit)
            yi = self.offset_y + self.nodes[u] * self.node_unit

            xj = self.offset_x + int((t + gamma) * self.time_unit)
            yj = self.offset_y + self.nodes[v] * self.node_unit

            coords.append((xi,yi))
            coords.append((xj,yj))

        tk = path[-1][0]
        vk = path[-1][2]
        xi = self.offset_x + int(tk * self.time_unit)
        yi = self.offset_y + self.nodes[vk] * self.node_unit

        xj = self.offset_x + int((end) * self.time_unit)
        yj = self.offset_y + self.nodes[vk] * self.node_unit
        coords.append((xi,yi))
        coords.append((xj,yj))

        self.f.writelines("\n"+"2 1 0 " + str(width) + " " + str(color) + " 7 " + str(depth) + " -1 -1 0.000 0 0 -1 0 0 " + str(len(coords)))
        self.f.writelines("\n"+" ".join([ " ".join(map(str, i)) for i in coords ] ))

    def addRectangle(self, u, v, b, e, width=100, depth=51, color=0, border="", bordercolor=0, borderwidth=2):
#je comprends pas l'intéret de cette fonction
        margin = int(width/2)

        if color in self.colors:
            color = self.colors[color]
        if bordercolor in self.colors:
            bordercolor = self.colors[bordercolor]

        # Print border lrtb (if any)
        if "l" in border:
            self.f.writelines("\n"+"2 1 0 " + str(borderwidth) + " " + str(bordercolor) + " 7 48 -1 -1 0.000 0 0 -1 0 0 2")
            self.f.writelines("\n"+str(self.offset_x + int(b * self.time_unit)) + " " + str(self.offset_y + self.nodes[u] * self.node_unit - margin) + " " + str(self.offset_x + int(b * self.time_unit)) + " " + str(self.offset_y + self.nodes[v] * self.node_unit + margin) + "\n")
        if "r" in border:
            self.f.writelines("\n"+"2 1 0 " + str(borderwidth) + " " + str(bordercolor) + " 7 48 -1 -1 0.000 0 0 -1 0 0 2")
            self.f.writelines("\n"+str(self.offset_x + int(e * self.time_unit)) + " " + str(self.offset_y + self.nodes[u] * self.node_unit - margin) + " " + str(self.offset_x + int(e * self.time_unit)) + " " + str(self.offset_y + self.nodes[v] * self.node_unit + margin) + "\n")
        if "t" in border:
            self.f.writelines("\n"+"2 1 0 " + str(borderwidth) + " " + str(bordercolor) + " 7 48 -1 -1 0.000 0 0 -1 0 0 2")
            self.f.writelines("\n"+str(self.offset_x + int(b * self.time_unit)) + " " + str(self.offset_y + self.nodes[u] * self.node_unit - margin) + " " + str(self.offset_x + int(e * self.time_unit)) + " " + str(self.offset_y + self.nodes[u] * self.node_unit - margin))
        if "b" in border:
            self.f.writelines("\n"+"2 1 0 " + str(borderwidth) + " " + str(bordercolor) + " 7 48 -1 -1 0.000 0 0 -1 0 0 2")
            self.f.writelines("\n"+str(self.offset_x + int(b * self.time_unit)) + " " + str(self.offset_y + self.nodes[v] * self.node_unit + margin) + " " + str(self.offset_x + int(e * self.time_unit)) + " " + str(self.offset_y + self.nodes[v] * self.node_unit + margin))

        if color > -1:
            # Print rectangle
            self.f.writelines("\n"+"2 2 0 0 0 " + str(color) + " " + str(depth) + " -1 20 0.000 0 0 -1 0 0 5")
            #self.f.writelines("\n"+str(self.offset_x + int(b * self.time_unit)) + " " + str(self.offset_y + int(self.nodes[u]*self.node_unit) - margin) + " " + str(self.offset_x + int(e * self.time_unit)) + " " + str(self.offset_y + int(self.nodes[u]*self.node_unit) - margin) + " " + str(self.offset_x + int(e * self.time_unit)) + " " + str(self.offset_y + int(self.nodes[v]*self.node_unit) + margin) + " " + str(self.offset_x + int(b*self.time_unit)) + " " + str(self.offset_y + int(self.nodes[v]*self.node_unit) + margin) + " " + str(self.offset_x + int(b*self.time_unit)) + " " + str(self.offset_y + int(self.nodes[u]*self.node_unit) - margin) )

    def addTime(self, t, label="", width=1, font=12, color=0):
        # Possibilite de changer le type de ligne, la couleur, etc.
        if self.num_time_intervals == 0:
            self.num_time_intervals = 1

        if color in self.colors:
            color = self.colors[color]

        linetype = 1

        self.f.writelines("\n"+"""2 1 """ + str(linetype) + """ """ + str(width) + """  """ + str(color) + """ 7 50 -1 -1 2.000 0 0 7 0 0 2\n \
          """ + str(self.offset_x + int(t * self.time_unit)) + """ """ + str(self.offset_y + int(2 * self.node_unit - 150)) + """ """ + str(self.offset_x + int(t * self.time_unit)) + """ """ + str(self.offset_y + int(self.node_cpt * self.node_unit + 300)))

        # Add label if any
        self.f.writelines("\n"+"4 0 " + str(color) + " 50 -1 0 " + str(font) + " 0.0000 4 135 120 " + str(self.offset_x + int(t * self.time_unit) - (2 * font * len(label))) + " " + str(self.offset_y - 175 + int(2 * self.node_unit)) + " " + str(label) + "\\001")

    def addTimeLine(self, ticks=1, marks=None):
        timeline_y = self.node_cpt * self.node_unit + self.layer_cpt*self.node_unit + int(self.node_unit / 2)

        vals = []
        i = self.alpha
        while i < self.omega:
            if (i).is_integer():
                vals.append((int(i),int(i)))
            else:
                vals.append((i,i))
            i = i+ticks

        if marks is not None:
            # Ajouter/remplacer les valeurs (t, v)
            for (t,v) in marks:
                found = False
                for x in range(0, len(vals)):
                    if vals[x][0] == t:
                        vals[x] = (t,v)
                        found = True
                if not found:
                    vals.append((t,v))

        # Time arrow
        if self.discrete > 0:
            start, end = self.omega - 0.5, self.omega
        else:
            start, end = self.alpha, self.omega

        self.f.writelines("\n"+"2 1 0 1 0 7 50 -1 -1 0.000 0 0 -1 1 0 2")
        self.f.writelines("\n"+"1 1 1.00 60.00 120.00")
        self.f.writelines("\n"+str(self.offset_x + int(start * self.time_unit)) + " " + str(self.offset_y + timeline_y) + " " + str(self.offset_x + int(end * self.time_unit)) + " " + str(self.offset_y + timeline_y))

        # Time ticks
        for (i,j) in vals:
            self.f.writelines("\n"+"2 1 0 1 0 7 50 -1 -1 0.000 0 0 -1 0 0 2")
            self.f.writelines("\n"+str(self.offset_x + int(i * self.time_unit)) + " " + str(self.offset_y + timeline_y) + " " + str(self.offset_x + int(i * self.time_unit)) + " " + str(self.offset_y + timeline_y + 30))
            if i < self.omega - 1:
                self.f.writelines("\n"+"4 1 0 50 -1 0 20 0.0000 4 135 120 " + str(self.offset_x + int(i * self.time_unit)) + " " + str(self.offset_y + timeline_y + 250) + " " + str(j) + "\\001")

        # Write "time"
        self.f.writelines("\n"+"4 2 0 50 -1 0 20 0.0000 4 135 120 " + str(self.offset_x + int(self.omega * self.time_unit)) + " " + str(self.offset_y + timeline_y + 250) + " time\\001")

        
    def closeFile(self):
        self.f.close()

    #pimprenelle : je n'ai pas compris à quoi sert (et ça bloquait !) donc je le retire ...
    #def __del__(self):
        # Adds white rectangle in background around first node (for EPS bounding box)
        #self.addRectangle(self.first_node, self.first_node, self.alpha, self.omega, width=300,depth=60, color=7)

# main
