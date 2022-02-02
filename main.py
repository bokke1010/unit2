# Header

import simulate

# Main variables
# p = 0.06
R0 = 4
time_infectious = 5
infection_adjustment = 1.5

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

def interstep(sim:simulate.simulation):
    if not hasattr(sim, "bp"):
        sim.bp = sim.p
    infected = sim.stats[sim.states.index("I")]
    isolated = sim.stats[sim.states.index("C")]
    sim.p = sim.bp / (infection_adjustment * (1+(infected + isolated) / sim.population))
    pass

# Graph setup
graph = simulate.generate_prison()
average_contacts = len(graph.edges) / len(graph.nodes)
p = R0 / (average_contacts * time_infectious)
import networkx as nx

# color_map = [node["color"] for node in graph.nodes.values()]
# nx.draw(graph, node_color=color_map, node_size=120)#, pos=nx.random_layout(graph))

# plt.show()

simulation = simulate.simulation(graph, p, time_infectious, 0.2, 25, 0.05)
simulation.infect(0)
results = simulation.simulate(50, colors, interventions, interstep, True)

