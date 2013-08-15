#!/usr/bin/env python
#coding: utf-8

import networkx
import random

class ConstraintGraph(object):
    def __init__(self, G):
        self.original_graph = G

    def calc_check_values(self, variable_values):
        G = self.original_graph
        if len(variable_values) != G.number_of_nodes():
            raise ValueError("variable_valuesのサイズがおかしい")

        check_values = []
        for u, v in G.edges():
            value = variable_values[u] + variable_values[v]
            check_values.append(value)

        return check_values

class FJGraphError(Exception):
    pass

class DegreeDistError(FJGraphError):
    pass

def specified_degree_graph(degree_dist):
    hands_count = sum([i * dist for i, dist in enumerate(degree_dist)])
    if hands_count % 2 != 0:
        raise DegreeDistError("次数の合計が2で割り切れない")

    node_size = sum(degree_dist)
    edge_size = hands_count / 2

    shuffled_nodes = list(range(node_size))
    random.shuffle(shuffled_nodes)
    edge_num_table = []
    G = networkx.MultiGraph()
    for d, dist in enumerate(degree_dist):
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
