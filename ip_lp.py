#!/usr/bin/env python
#coding: utf-8

from __future__ import division, print_function
import fjgraph
import fjutil
import random
from collections import Counter


def parse_arguments():
    import optparse
    import os
    parser = optparse.OptionParser("usage: %prog [options] ensemble.json")
    parser.add_option("-t", "--trials",
                      dest="trials",
                      type="int",
                      default=1000,
                      help="set the number of trials",
                      metavar="NUMBER")
    parser.add_option("-s", "--seed",
                      dest="seed",
                      type="string",
                      default=None,
                      help="set the seed for the random module",
                      metavar="STRING")
    (opts, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("required a json file which define the ensemble")
    if not os.access(args[0], os.R_OK):
        parser.error("cannot read {}".format(args[0]))
    return (opts, args[0])


def count_one_half(values):
    counter = Counter(values)
    return counter[1/2]


def ip_lp_experiment(ensemble, number_of_trials):
    sum_number_of_one_half = 0
    sum_lp_opt_value = 0.0
    sum_ip_opt_value = 0.0
    sum_opt_ratio = 0.0
    progress_bar = fjutil.ProgressBar("Calculation", 80)
    solver = fjgraph.VertexCoverSolver()

    progress_bar.begin()
    for i in range(number_of_trials):
        G = ensemble.generate_graph()

        lp_solution = solver.lp_solve(G)
        number_of_one_half = count_one_half(lp_solution.values())
        lp_opt_value = lp_solution.opt_value()

        ip_solution = solver.ip_solve(G)
        ip_opt_value = ip_solution.opt_value()

        sum_number_of_one_half += number_of_one_half
        sum_opt_ratio += lp_opt_value / ip_opt_value
        sum_lp_opt_value += lp_opt_value
        sum_ip_opt_value += ip_opt_value
        progress_bar.write(i / number_of_trials)
    progress_bar.end()

    # 結果出力
    ave_number_of_one_half = sum_number_of_one_half / number_of_trials
    ave_opt_ration = sum_opt_ratio / number_of_trials
    ave_ratio_of_one_half = \
        ave_number_of_one_half / ensemble.number_of_nodes()
    ave_lp_opt_value = sum_lp_opt_value / number_of_trials
    ave_ip_opt_value = sum_ip_opt_value / number_of_trials
    print("ave_number_of_one_half: {:.4} ({:.2%})".format(
        ave_number_of_one_half, ave_ratio_of_one_half))
    print("ave_opt_ration: {:.4}".format(ave_opt_ration))
    print("ave_lp_opt_value: {:.4}".format(ave_lp_opt_value))
    print("ave_ip_opt_value: {:.4}".format(ave_ip_opt_value))


if __name__ == '__main__':
    # 引数処理
    (opts, json_file) = parse_arguments()

    # 実験パラメータの設定と確認
    random.seed(opts.seed)
    ensemble_def = fjutil.load_json_file(json_file)
    ensemble = fjgraph.GraphEnsembleFactory().create(**ensemble_def)
    print("ensemble: {}".format(ensemble))
    print("seed: {}".format(opts.seed))
    print("number of nodes: {}".format(ensemble.number_of_nodes()))
    print("number of edges: {}".format(ensemble.number_of_edges()))
    print("number of trials: {}".format(opts.trials))

    ip_lp_experiment(ensemble, opts.trials)
