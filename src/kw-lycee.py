import library.nbtool as nbtool
import parser.lycee as lycee
from parser.lycee import *

# Networkx for graph manipulation
import networkx as nx

# Z3 for optimization
import z3

# Bokeh for drawing
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import *
import webbrowser

# Read the dataset

#Lycee = MultiStream(interval, LYCEE, LayerList([]), LinkList([]))
liste, liste2 = readNodes(Lycee, ['face_to_face', 'facebook', 'friendship'])
ti, ni = readLinks(Lycee, liste)
readLinks2(Lycee, liste, liste2)   # read facebook links
readLinks3(Lycee, liste, liste2)   # read friendship links

# Layer definitions

_math_physics = layerWithCommonPoint(LYCEE, 'annee', 'MP')
_girls        = layerWithCommonPoint(LYCEE, 'sexe', 'F')
_f2f          = layerWithCommonPoint(LYCEE, 'typeOfRel', 'face_to_face')

mp_girls = Lycee.extractLayers(_math_physics).extractLayers(_girls).extractLayers(_f2f)

#mp_girls = Lycee.extract(annee='MP', sexe='F', typeOfRel='face_to_face')

# Conversion to NetworkX

G_mp_girls = nx.Graph()

for link in mp_girls.giveLinks().listOfLinks:
    n1, n2 = link.node1.node, link.node2.node
    G_mp_girls.add_nodes_from([n1, n2])
    G_mp_girls.add_edge(n1, n2)
    G_mp_girls.edges[n1, n2]['connections'] = len(link.giveIntervals())
    G_mp_girls.edges[n1, n2]['intervals'] = [(interval.t1, interval.t2) for interval in link.giveIntervals()]

# Optimization

def Abs(x): return z3.If(x >= 0, x, -x)

solver = z3.Solver()
solver.set('timeout', 1000)
V = G_mp_girls.nodes
E = G_mp_girls.edges

print(f'V: {len(V)}, E: {len(E)}')

# `Assignment` uniquely give vertical positions ([0, 1, ..., N-1]) to the nodes.
Assignment = [z3.Int('v' + n) for n in V]
assignment = dict(zip(V, Assignment))
for position in Assignment:
    solver.add(position >= 0)
    solver.add(position < len(V))
solver.add(z3.Distinct(Assignment))

# Objective function `Distance`: A weighted sum of the edge distances
Distance = z3.Sum([Abs(assignment[n1] - assignment[n2]) for n1, n2 in E])

history = []
max_distance = 1 << 31

print('Distance optimizer started...')
while True:
    solver.add(Distance < max_distance)
    print(max_distance)
    result = solver.check()
    if result != z3.sat: break
    current_best = solver.model()
    max_distance = current_best.evaluate(Distance)
    history.append(max_distance.as_long())

Solution = [(v, current_best[v].as_long()) for v in Assignment]
print(f'Solution: {Solution}')
print(f'Distance: {max_distance.as_long()}')
print(f'Optimum: {result == z3.unsat}')
print(f'History: {history}')

# Links

vs = [str(v) for v, _ in Solution]
print(vs)

position = dict(zip(V, Solution))
edges = []
for i in E:
    #v1, v2 = ['v' + str(v) for v in i]
    v1, v2 = i
    pos1, pos2 = position[v1], position[v2] # [position[v] for v in i]
    v1, v2 = 'v' + str(v1), 'v' + str(v2)
    intervals = E[i]['intervals']
    edges += [(v1, v2, pos1[1], pos2[1], t1, t2) for (t1, t2) in intervals]

v1, v2, y1, y2, x1, x2 = [[e[i] for e in edges] for i in range(6)]

# Visualization

links = [([x1, x1], [v1, v2]) for v1, v2, x1, x2 in zip(v1, v2, x1, x2)]
# print(links[0])
x, v = [x for x, _ in links], [[v for v in vpair] for _, vpair in links]

# print(f'edge0: {edges[0]}, links0: {links[0]}, v1: {v1[0]}, v2: {v2[0]}, x0: {x[0]}, y0: {v[0]}')

HTML = 'outputs/lycee-girls.html'
output_file(HTML)

TOOLTIPS = [
    ('(x, y)', '($x, $y)')
]

#p = figure(plot_width=800, plot_height=250, x_range=(0, 100), tools='xpan,wheel_zoom,box_zoom,reset', tooltips=TOOLTIPS)
p = figure(plot_width=800, plot_height=250, x_range=(0, 100), y_range=vs,
           tools='xpan,wheel_zoom,box_zoom,reset')
p.circle(x1, v1, size=5)
p.circle(x1, v2, size=5)
p.multi_line(x, v, width=2)
show(p)

webbrowser.open_new(HTML)
