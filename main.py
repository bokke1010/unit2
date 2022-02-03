# Header

import simulate

# Main variables
# p = 0.06
R0 = 4
time_infectious = (6,8)
time_exposed = (6,12) # Incubation period is 12-14 days
infection_adjustment = 1.5
lethality_adjustment = 4

colors = {
    "S": "blue",
    "E": "orange",
    "I": "red",
    "C": "gray",
    "R": "gold",
    "D": "black"
}

def test_func(G):
    print(len(G.nodes))

interventions = {
    1: test_func
}

def interstep(sim:simulate.simulation):
    if not hasattr(sim, "base_p"):
        sim.base_p = sim.p
    if not hasattr(sim, "base_lethality"):
        sim.base_lethality = sim.lethality
    
    infected = sim.stats[sim.states.index("I")]
    isolated = sim.stats[sim.states.index("C")]
    sim.p = sim.base_p / (1 + (infection_adjustment * (infected + isolated) / sim.population))
    sim.lethality = sim.base_lethality * (1 + (lethality_adjustment * infected / sim.population))
    pass

# Graph setup
graph = simulate.generate_prison()
average_contacts = len(graph.edges) / len(graph.nodes)
p = R0 / (average_contacts * (time_infectious[0] + time_infectious[1])/2)

# import networkx as nx
# color_map = [node["color"] for node in graph.nodes.values()]
# nx.draw(graph, node_color=color_map, node_size=120)#, pos=nx.random_layout(graph))


simulation = simulate.simulation(graph, p, time_infectious, time_exposed, 0.3, 30, 0.05)
simulation.infect(0)
results = simulation.simulate(150, colors, interventions, interstep, True)

