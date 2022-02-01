from time import time
import networkx as nx
import matplotlib.pyplot as plt
from random import choice, random

def generate_prison():
    G = nx.Graph()
    
    guard_population, low_s_population, med_s_population, high_s_population = 100, 70, 110, 70
    guard_contacts, low_s_contacts, med_s_contacts, high_s_contacts = 6, 6, 4, 2
    guard_p, low_s_p, med_s_p, high_s_p = 0.2, 0.18, 0.14, 0.12

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
            if random() < low_s_p:
                G.add_edge(i, j)
        for j in range(m_start, h_start):
            if random() < med_s_p:
                G.add_edge(i, j)
        for j in range(h_start, h_end):
            if random() < high_s_p:
                G.add_edge(i, j)
    return G

class simulation:

    states = ["S", "I", "R", "C", "D"]

    def __init__(self, G, p=0.5, time_infected=2, solitary_response=0, solitary_capacity=0):
        self.graph = G
        self.p = 0
        self.time_infected = time_infected
        self.solitary_response = solitary_response
        self.solitary_capacity = solitary_capacity
        self.isolated = 0

        for node in self.graph.nodes.values():
            node["state"] = "S"
            node["time"] = 0

    def infect(self, node = "Random"):
        if node == "Random":
            node = choice(self.graph.nodes.keys())
        self.graph.nodes[node]["state"] = "I"

    def _step(self):
        infectable = []
        for i, node in self.graph.nodes.items():
            if node["state"] == "I":
                for nb in self.graph[i]:
                    infectable.append(nb)
                node["time"] += 1
                if node["time"] == self.time_infected:
                    node["state"] = "R"
                elif random() < self.solitary_response and self.isolated < self.solitary_capacity:
                    node["state"] = "C"
                    self.isolated += 1
            elif node["state"] == "C":
                node["time"] += 1
                if node["time"] == self.time_infected:
                    node["state"] = "R"
                    self.isolated -= 1
        for i in infectable:
            node = self.graph.nodes[i]
            if node["state"] == "S" and random() < self.p:
                node["state"] = "I"

    def draw_colored(self, colors: dict):
        color_map = [colors[node["state"]] for node in self.graph.nodes.values()]
        nx.draw(self.graph, node_color=color_map)
        plt.show()

    def _count_state(self, state):
        return sum(map(lambda x : x["state"] == state, self.graph.nodes.values()))

    def simulate(self, T:int, colors:dict, interventions:dict = {}, graph_states:bool = False):

        # interventions = {
        #     43: demo_intervention,
        #     75: lower_p
        # }

        data = {}
        for state in self.states:
            data[state] = [self._count_state(state)]

        for t in range(T):
            if t in interventions:
                interventions[t](self.graph)
            self._step()
            for state in self.states:
                data[state].append(self._count_state(state))


        if graph_states:            
            for state in self.states:
                plt.plot(data[state], color = colors[state])
            plt.show()
            self.draw_colored(colors)
        return data