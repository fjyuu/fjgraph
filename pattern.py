#!/usr/bin/env python
#coding: utf-8

from __future__ import division, print_function, unicode_literals
import fjgraph
import fjutil
import networkx
import itertools
import optparse
import os
import json
from collections import Counter

def ok_check_values(check_values):
    for value in check_values:
        if value < 1:
            return False
    return True

def pattern_of_vertex_cover(G):
    node_size = G.number_of_nodes()
    edge_size = G.number_of_edges()
    constraint_graph = fjgraph.ConstraintGraph(G)
    ret_dist = Counter()

    for variable_values in itertools.product([0, 1], repeat = node_size):
        weight = sum(variable_values)
        check_values = constraint_graph.calc_check_values(variable_values)
        if ok_check_values(check_values):
            ret_dist[weight] += 1

    return ret_dist

def ave_pattern_of_vertex_cover(ensemble, loop_count):
    sum_dist = Counter()
    progress_bar = fjutil.ProgressBar("Calculation", 80)

    progress_bar.begin()
    for i in range(loop_count):
        G = ensemble.generate_graph()
        ret_dist = pattern_of_vertex_cover(G)
        sum_dist += ret_dist
        progress_bar.write(i / loop_count)
    progress_bar.end()

    ave_dist = Counter(dict((key, value / loop_count)
                            for key, value in sum_dist.items()))
    return ave_dist

def pattern_of_LP_vertex_cover(G):
    node_size = G.number_of_nodes()
    edge_size = G.number_of_edges()
    constraint_graph = fjgraph.ConstraintGraph(G)
    ret_table = Counter()

    for variable_values in itertools.product([0, 0.5, 1], repeat = node_size):
        number_of_one_half = variable_values.count(0.5)
        number_of_one = variable_values.count(1)
        check_values = constraint_graph.calc_check_values(variable_values)
        if ok_check_values(check_values):
            ret_table[(number_of_one_half, number_of_one)] += 1

    return ret_table

def ave_pattern_of_LP_vertex_cover(ensemble, loop_count):
    sum_table = Counter()
    progress_bar = fjutil.ProgressBar("Calculation", 80)

    progress_bar.begin()
    for i in range(loop_count):
        G = ensemble.generate_graph()
        ret_table = pattern_of_LP_vertex_cover(G)
        sum_table += ret_table
        progress_bar.write(i / loop_count)
    progress_bar.end()

    ave_table = Counter(dict((key, value / loop_count)
                             for key, value in sum_table.items()))
    return ave_table

if __name__ == '__main__':
    # 引数処理
    parser = optparse.OptionParser("usage: %prog [options] ensemble.json")
    parser.add_option("-t", "--trials",
                      dest    = "trials",
                      type    = "int",
                      default = 1000,
                      help    = "set the number of trials",
                      metavar = "NUMBER")
    (opts, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("required a json file which define the ensemble")
    if not os.access(args[0], os.R_OK):
        parser.error("cannot read {}".format(args[0]))

    # アンサンブル定義JSON読み込み
    jsonf = open(args[0], "r")
    ensemble_def = json.load(jsonf)
    jsonf.close()

    # 実験パラメータ
    ensemble = fjgraph.GraphEnsembleFactory().create(**ensemble_def)
    loop_count = opts.trials
    print("ensemble: {}".format(ensemble))
    print("number of nodes: {}".format(ensemble.number_of_nodes()))
    print("number of edges: {}".format(ensemble.number_of_edges()))
    print("number of trials: {}".format(loop_count))

    # IP
    print()
    ave_dist = ave_pattern_of_vertex_cover(ensemble, loop_count)
    print("ave_pattern_of_vertex_cover:")
    fjutil.printCounter(ave_dist, format = "{:>5}: {}")

    # LP
    print()
    ave_table = ave_pattern_of_LP_vertex_cover(ensemble, loop_count)
    print("ave_pattern_of_LP_vertex_cover:")
    fjutil.printCounter(ave_table, format = "{:>10}: {}")
