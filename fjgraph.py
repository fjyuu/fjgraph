#!/usr/bin/env python
#coding: utf-8

import networkx
import random

class GraphEnsembleFactory(object):
    def create(self, type, params):
        if type == "SpecifiedDegreeDistEnsemble":
            return SpecifiedDegreeDistEnsemble(**params)
        else:
            raise FJGraphError("アンサンブルタイプが存在しない")

class GraphEnsemble(object):
    def number_of_nodes(self):
        return None

    def number_of_edges(self):
        return None

    def generate_graph(self):
        return None

class SpecifiedDegreeDistEnsemble(GraphEnsemble):
    def __init__(self, degree_dist):
        hands_count = sum([i * dist for i, dist in enumerate(degree_dist)])
        if hands_count % 2 != 0:
            raise DegreeDistError("次数の合計が2で割り切れない")
        self.degree_dist = tuple(degree_dist)

    def number_of_nodes(self):
        return sum(self.degree_dist)

    def number_of_edges(self):
        return sum([i * dist for i, dist in enumerate(self.degree_dist)]) / 2

    def generate_graph(self):
        node_size = self.number_of_nodes()
        edge_size = self.number_of_edges()

        shuffled_nodes = list(range(node_size))
        random.shuffle(shuffled_nodes)
        edge_num_table = []
        G = networkx.MultiGraph()
        for d, dist in enumerate(self.degree_dist):
            for i in range(dist):
                n = shuffled_nodes.pop()
                #print("頂点{0}を次数{1}にする".format(n,d))
                G.add_node(n)
                edge_num_table.extend([n] * d)

        random.shuffle(edge_num_table)
        while edge_num_table:
            a = edge_num_table.pop()
            b = edge_num_table.pop()
            G.add_edge(a, b, weight = 1)

        return G

    def __str__(self):
        return "{}(degree_dist={})".format(
            self.__class__.__name__, self.degree_dist)

class ConstraintGraph(object):
    def __init__(self, G, check_function = lambda u, v: u + v):
        self.original_graph = G
        self.check_function = check_function

    def calc_check_values(self, variable_values):
        G = self.original_graph
        if len(variable_values) != G.number_of_nodes():
            raise ValueError("variable_valuesのサイズがおかしい")

        check_values = []
        for u, v in G.edges():
            value = self.check_function(variable_values[u], variable_values[v])
            check_values.append(value)

        return check_values

class FJGraphError(Exception):
    pass

class DegreeDistError(FJGraphError):
    pass
