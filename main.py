# Header

import simulate

# Main variables
p = 0.2
time_infectious = 12

colors = {
    "S": "blue",
    "I": "red",
    "C": "yellow",
    "R": "gold",
    "D": "gray"
}

def test_func(G):
    print(len(G.nodes))

interventions = {
    1: test_func
}

# Graph setup
graph = simulate.generate_prison()

# import networkx as nx

# color_map = [node["color"] for node in graph.nodes.values()]
# nx.draw(graph, node_color=color_map)
# plt.show()

simulation = simulate.simulation(graph, p, time_infectious)
simulation.infect(0)
results = simulation.simulate(200, colors, interventions, True)

