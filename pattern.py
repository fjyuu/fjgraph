#!/usr/bin/env python
#coding:utf-8

from __future__ import division, print_function, unicode_literals
import fjgraph
import fjutil
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
        if ok_check_values(check_values):
            # print("ok: {0} weight={1}".format(variable_values, weight))
            if weight in ret_dist:
                ret_dist[weight] += 1
            else:
                ret_dist[weight] = 1

    return ret_dist

def ave_pattern_of_vertex_cover(degree_dist, loop_count):
    sum_dist = {}
    progress_bar = fjutil.ProgressBar("Calculation", 80)

    progress_bar.begin()
    for i in range(loop_count):
        G = fjgraph.specified_degree_graph(degree_dist)
        ret_dist = pattern_of_vertex_cover(G)
        progress_bar.write(i / loop_count)
        for key, value in ret_dist.items():
            if key in sum_dist:
                sum_dist[key] += value
            else:
                sum_dist[key] = value
    progress_bar.end()

    ave_dist = dict((key, value / loop_count) for key, value in sum_dist.items())
    return ave_dist

def pattern_of_LP_vertex_cover(G):
    node_size = G.number_of_nodes()
    edge_size = G.number_of_edges()
    constraint_graph = fjgraph.ConstrantGraph(G)
    ret_table = [[0 for j in range(node_size + 1)] for i in range(node_size + 1)]

    for variable_values in itertools.product([0, 0.5, 1], repeat = node_size):
        number_of_one_half = variable_values.count(0.5)
        number_of_one = variable_values.count(1)
        check_values = constraint_graph.calc_check_values(variable_values)
        if ok_check_values(check_values):
            # print("ok: {0} number_of_one_half={1} number_of_one={2}".format(variable_values, number_of_one_half, number_of_one))
            ret_table[number_of_one_half][number_of_one] += 1

    return ret_table

def ave_pattern_of_LP_vertex_cover(degree_dist, loop_count):
    node_size = sum(degree_dist)
    sum_table = [[0 for j in range(node_size + 1)] for i in range(node_size + 1)]
    progress_bar = fjutil.ProgressBar("Calculation", 80)

    progress_bar.begin()
    for i in range(loop_count):
        G = fjgraph.specified_degree_graph(degree_dist)
        ret_table = pattern_of_LP_vertex_cover(G)
        progress_bar.write(i / loop_count)
        for number_of_one_half, row in enumerate(ret_table):
            for number_of_one, number in enumerate(row):
                sum_table[number_of_one_half][number_of_one] += number
    progress_bar.end()

    ave_table = [[sum_table[i][j] / loop_count for j in range(node_size + 1)] for i in range(node_size + 1)]
    return ave_table

if __name__ == '__main__':
    degree_dist = [0, 1, 2, 3, 4]
    loop_count = 1000

    print("number of nodes: {0}".format(sum(degree_dist)))
    print("number of edges: {0}".format(
        int(sum([i * dist for i, dist in enumerate(degree_dist)]) / 2)
    ))
    print("loop count: {0}".format(loop_count))

    # IP
    ave_dist = ave_pattern_of_vertex_cover(degree_dist, loop_count)
    print("ave_pattern_of_vertex_cover: {0}".format(ave_dist))

    # LP
    ave_table = ave_pattern_of_LP_vertex_cover(degree_dist, loop_count)
    print("ave_pattern_of_LP_vertex_cover:")
    for row in ave_table:
        print(row)
