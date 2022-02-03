from time import time
import networkx as nx
import matplotlib.pyplot as plt
from random import choice, random, randint

def generate_prison():
    G = nx.Graph()
    
    guard_population, low_s_population, med_s_population, high_s_population = 150, 140, 120, 80
    guard_contacts, low_s_contacts, med_s_contacts, high_s_contacts = 6, 6, 4, 2
    guard_p, low_s_p, med_s_p, high_s_p = 0.18, 0.14, 0.10, 0.08
    guard_low_mix, guard_med_mix, guard_high_mix = 1.2, 1.8, 2.4

    low_s = nx.watts_strogatz_graph(low_s_population, low_s_contacts, low_s_p)
    med_s = nx.watts_strogatz_graph(med_s_population, med_s_contacts, med_s_p)
    high_s = nx.watts_strogatz_graph(high_s_population, high_s_contacts, high_s_p)
    guards = nx.watts_strogatz_graph(guard_population, guard_contacts, guard_p)

    colors = ["green", "orange", "red", "blue"]
    for i, subgraph in enumerate([low_s, med_s, high_s, guards]):
        for node in subgraph.nodes.values():
            node["color"] = colors[i]

    G = nx.disjoint_union_all([guards, low_s, med_s, high_s])
    for i in range(guard_population):
        l_start = guard_population
        m_start = l_start + low_s_population
        h_start = m_start + med_s_population
        h_end = h_start + high_s_population
        for j in range(l_start, m_start):
            if random() < guard_low_mix / guard_population:
                G.add_edge(i, j)
        for j in range(m_start, h_start):
            if random() < guard_med_mix / guard_population:
                G.add_edge(i, j)
        for j in range(h_start, h_end):
            if random() < guard_high_mix / guard_population:
                G.add_edge(i, j)
    return G

class simulation:

    states = ["S", "E", "I", "R", "C", "D"]

    def __init__(self, G, p=0.5, time_infected=(2,3), time_exposed=(2,3), solitary_response=0, solitary_capacity=0, lethality=0):
        self.graph:nx.Graph = G
        self.population:int = len(G.nodes)
        self.p:float = p
        self.time_exposed:int = time_exposed
        self.time_infected:int = time_infected
        self.solitary_response:float = solitary_response
        self.solitary_capacity:int = solitary_capacity
        self.lethality:float = lethality
        self.isolated:int = 0

        for node in self.graph.nodes.values():
            node["state"] = "S"
            node["time"] = 0

        self.stats:tuple = self.state_stats()

    def infect(self, node = "Random"):
        if node == "Random":
            node = choice(self.graph.nodes.keys())
        self.graph.nodes[node]["state"] = "I"

    def _step(self):
        infectable = []
        for i, node in self.graph.nodes.items():
            node["time"] -= 1
            if node["state"] in ["C", "I"]:
                if node["state"] == "I":
                    for nb in self.graph[i]:
                        infectable.append(nb)
                    if random() < self.solitary_response and self.isolated < self.solitary_capacity:
                        node["state"] = "C"
                        self.isolated += 1
                if node["time"] == 0:
                    if node["state"] == "C":
                        self.isolated -= 1
                    if random() < self.lethality:
                        node["state"] = "D"
                    else:
                        node["state"] = "R"
            elif node["state"] == "E":
                if node["time"] == 0:
                    node["state"] = "I"
                    node["time"] = randint(*self.time_infected)
        for i in infectable:
            node = self.graph.nodes[i]
            if node["state"] == "S" and random() < self.p:
                node["state"] = "E"
                node["time"] = randint(*self.time_exposed)

    def draw_colored(self, colors: dict):
        color_map = [colors[node["state"]] for node in self.graph.nodes.values()]
        nx.draw(self.graph, node_color=color_map)
        plt.show()

    def _count_state(self, state):
        return sum(map(lambda x : x["state"] == state, self.graph.nodes.values()))

    def state_stats(self):
        return tuple(self._count_state(state) for state in self.states)

    def simulate(self, T:int, colors:dict, interventions:dict = {}, interstep = None, graph_states:bool = False) -> list :

        data = [self.stats]

        for t in range(T):
            if t in interventions:
                interventions[t](self.graph)
            self._step()
            self.stats = self.state_stats()
            data.append(self.stats)
            if interstep != None:
                interstep(self)


        if graph_states:
            plot_data = list(zip(*data))
            for i, state in enumerate(self.states):
                plt.plot(plot_data[i], color = colors[state], label=state)
                plt.legend()
            plt.show()
            self.draw_colored(colors)
        return data