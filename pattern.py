#!/usr/bin/env python
#coding:utf-8

from __future__ import division
import fjgraph
import networkx
import itertools

def ok_check_values(check_values):
    for value in check_values:
        if value < 1:
            return False
    return True

def pattern_of_vertex_cover(G):
    node_size = G.number_of_nodes()
    edge_size = G.number_of_edges()
    constraint_graph = fjgraph.ConstrantGraph(G)
    ret_dist = {}

    for variable_values in itertools.product([0, 1], repeat = node_size):
        weight = sum(variable_values)
        check_values = constraint_graph.calc_check_values(variable_values)
        if ok_check_values(check_values): # all 1
            # print("ok: {0} weight={1}".format(variable_values, weight))
            if weight in ret_dist:
                ret_dist[weight] += 1
            else:
                ret_dist[weight] = 1

    return ret_dist

def ave_pattern_of_vertex_cover(degree_dist, loop_count):
    sum_dist = {}

    for i in range(loop_count):
        G = fjgraph.specified_degree_graph(degree_dist)
        ret_dist = pattern_of_vertex_cover(G)
        # print("{0}: {1}".format(i + 1, ret_dist))
        for key, value in ret_dist.items():
            if key in sum_dist:
                sum_dist[key] += value
            else:
                sum_dist[key] = value

    ave_dist = dict((key, value / loop_count) for key, value in sum_dist.items())
    return ave_dist


if __name__ == '__main__':
    degree_dist = [0, 1, 2, 3, 4]
    loop_count = 1000

    ave_dist = ave_pattern_of_vertex_cover(degree_dist, loop_count)
    print("ave_pattern_of_vertex_cover: {0}".format(ave_dist))
