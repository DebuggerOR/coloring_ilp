

from pulp import LpMinimize, LpProblem, LpStatus, lpSum, LpVariable
import networkx as nx
import matplotlib.pyplot as plt

def graph1():
    # 12 vars x_ij = 1 iff vertex i has color j
    # 3 vars y_i = 1 iff at color i is used

    # the graph:
    # 1-2-3
    #   |/
    #   4

    # minimize the sum of y_i
    # subject to:
    # 1. the sums x_i1 + x_i2 + x_i3 = 1
    # 2. the sums x_1j + x_2j <= 1 etc.
    # 3. x_ij <= c_j

    model = LpProblem(name="ilp-coloring", sense=LpMinimize)

    x11 = LpVariable(name="x11", cat='Binary')
    x12 = LpVariable(name="x12", cat='Binary')
    x13 = LpVariable(name="x13", cat='Binary')
    x21 = LpVariable(name="x21", cat='Binary')
    x22 = LpVariable(name="x22", cat='Binary')
    x23 = LpVariable(name="x23", cat='Binary')
    x31 = LpVariable(name="x31", cat='Binary')
    x32 = LpVariable(name="x32", cat='Binary')
    x33 = LpVariable(name="x33", cat='Binary')
    x41 = LpVariable(name="x41", cat='Binary')
    x42 = LpVariable(name="x42", cat='Binary')
    x43 = LpVariable(name="x43", cat='Binary')

    c1 = LpVariable(name="c1", cat='Binary')
    c2 = LpVariable(name="c2", cat='Binary')
    c3 = LpVariable(name="c3", cat='Binary')

    # for each var
    model += (x11 + x12 + x13 == 1)
    model += (x21 + x22 + x23 == 1)
    model += (x31 + x32 + x33 == 1)
    model += (x41 + x42 + x43 == 1)

    # for each edge for each color
    model += (x11 + x21 <= 1)
    model += (x12 + x22 <= 1)
    model += (x13 + x23 <= 1)

    model += (x21 + x31 <= 1)
    model += (x22 + x32 <= 1)
    model += (x23 + x33 <= 1)

    model += (x31 + x41 <= 1)
    model += (x32 + x42 <= 1)
    model += (x33 + x43 <= 1)

    model += (x21 + x41 <= 1)
    model += (x22 + x42 <= 1)
    model += (x23 + x43 <= 1)

    # for each node and color
    model += (x11 <= c1)
    model += (x21 <= c1)
    model += (x31 <= c1)
    model += (x41 <= c1)

    model += (x12 <= c2)
    model += (x22 <= c2)
    model += (x32 <= c2)
    model += (x42 <= c2)

    model += (x13 <= c3)
    model += (x23 <= c3)
    model += (x33 <= c3)
    model += (x43 <= c3)

    model += c1 + c2 + c3
    print(model)

    status = model.solve()


def graph2():
    G = nx.Graph()
    #edges = [(1,2),(2,3),(3,4),(4,5),(5,1),(6,8),(7,9),(8,10),(9,6),(1,6),(2,7),(3,8),(4,9),(5,10)]
    #edges = [(1,2),(2,3),(3,4),(4,1),(2,4),(5,6),(6,7),(7,8),
    #         (8,9),(9,10),(10,5),(1,5),(1,10),(1,9),(4,9),(4,8),(3,8),(3,7),(3,6),(2,6),(2,5),(12,5),(11,9),(12,6),
    #         (12,10),(11,10),(11,8),(11,7),(11,12),(12,7)]
    edges=[(1,2),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5),(3,3),(3,4),(3,5),(4,4),(4,5)]
    G.add_edges_from(edges)

    # init model and vars
    model = LpProblem(name="ilp-coloring", sense=LpMinimize)

    colors = ['red','blue','yellow','green']
    nodes = list(G.nodes())

    node_vars = [[None for j in range(len(colors))] for i in range(len(nodes))]

    for node in nodes:
        for i in range(len(colors)):
            node_vars[node-1][i] = LpVariable(name='x'+str(node) + str(i+1), cat='Binary')

    color_vars = [None for j in range(len(colors))]
    for c in range(len(colors)):
        color_vars[c] = LpVariable(name='c' + str(c+1), cat='Binary')

    # add constrains
    for node in nodes:
        model += (node_vars[node-1][0] + node_vars[node-1][1] + node_vars[node-1][2] + node_vars[node-1][3] == 1)

    for e in list(G.edges()):
        x1,x2 = e[0]-1, e[1]-1
        model += (node_vars[x1][0] + node_vars[x2][0] <= 1)
        model += (node_vars[x1][1] + node_vars[x2][1] <= 1)
        model += (node_vars[x1][2] + node_vars[x2][2] <= 1)
        model += (node_vars[x1][3] + node_vars[x2][3] <= 1)

    for node in nodes:
        for i in range(len(colors)):
            model += (node_vars[node-1][i] <= color_vars[i])

    model += lpSum(color_vars)
    status = model.solve()

    node_colors = []
    for node in nodes:
        for i in range(len(colors)):
            if node_vars[node - 1][i].value() == 1:
                node_colors.append(colors[i])

    # draw graph
    pos = nx.circular_layout(G)
    nx.draw_networkx_nodes(G,pos,node_color=node_colors)
    nx.draw_networkx_labels(G,pos)
    nx.draw_networkx_edges(G, pos)

    plt.show()


if __name__ == '__main__':
    graph2()







