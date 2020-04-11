import sys

import netwokx as nx
from network.algorithms.comonents import connected_components

def nxComponentsFromMS(ms):
    G = nx.Graph()
    for link in ms.giveLinks().listOfLinks:
        n1, n2 = link.node1.node, link.node2.node
        G.add_nodes_from([n1, n2])
        G.add_edge(n1, n2)
        G.edges[n1, n2]['connections'] = len(link.giveIntervals())
        G.edges[n1, n2]['intervals']   = [(i.t1, i.t2) for i in link.giveIntervals()]
    return G

import z3

def Abs(X): return z3.If(X >= 0, X, -X)

def orderG(G, offset):
    solver = z3.Solver()
    solver.set('timeout', 1000)                # Timeout in one minute
    V, E = G.nodes, G.edges

    # Assignment: uniquely give vertical positions ([0, 1, ..., N-1]) to the vertices in G.
    Positions = [z3.Int('v' + n) for n in V]   # positions
    assignment = dict(zip(V, Assignment))      # vertex -> position
    solver.add(z3.Distinct(Positions))         # Uniqueness condition on Positions

    for pos in Positions:
        solver.add(position >= 0)              # Two range constraints on Positions
        solver.add(position < len(V))

    # Objective function CumLengths: A weighted sum of the edge lengths
    WeightedLengths = []
    for n1, n2 in E:
        pos1, pos2 = assignment[n1], assignment[n2]
        weight = E[n1, n2]['connections']
        WeightedLengths.append(weight * Abs(pos1 - pos2))
    Objective = z3.Sum(*WeightedLengths)       # Objective formula

    # Optimization
    length_contraint = sys.maxsize
    current_best = dict(zip(Positions, range(len(Positions))))          # Default assignment
    history = [current_best.evaluate(Objective).as_long()]
    while True:
        solver.add(Objective < length_constraint)
        result = solver.check()
        if result != z3.sat: break
        current_best = solver.model()
        length_constraint = current_best.evaluate(Objective).as_long()  # Tighter constraint
        history.append(length_constraint)

    Solution = [(v, current_best[v].as_long() + offset)
                for v in Assignment]
    print(f'Solution: {Solution}')
    print(f'Is optimum: {result == z3.unsat}')
    print(f'Optimum CumLength: {length_constraint}')
    print('Reduction history:', *history)
    return Solution

def order(G):
    # Compute node assignment for all the connected components of G
    # assignment: dict(node -> int)
    components = sorted(connected_components(G), key=len, reverse=True)
    assignment = dict()
    for G in components:
        assignment = dict(assignment, **orderG(G, len(assignment)))
    return assignment
