#!/usr/bin/env python
#coding: utf-8

from __future__ import division, print_function
import fjgraph
import fjutil
import fjexperiment
import random


def parse_arguments():
    import optparse
    import os
    parser = optparse.OptionParser("usage: %prog [options] num_of_degree")
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
    parser.add_option("-m", "--max-degree",
                      dest="max_degree",
                      type="int",
                      default=30,
                      help="set the max degree",
                      metavar="NUMBER")
    (opts, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("required a num_of_degree")
    return opts, int(args[0])


def print_table(table):
    for row in table:
        print(" ".join(["{}".format(v) for v in row]))


def report20130823_experiment():
    # 引数処理
    (opts, num_of_degree) = parse_arguments()

    # 実験パラメータ
    print("= experiment params =")
    random.seed(opts.seed)
    print("num_of_degree: {}".format(num_of_degree))
    print("max_degree: {}".format(opts.max_degree))
    print("num_of_trials: {}".format(opts.trials))
    print("seed: {}".format(opts.seed))
    print()

    ensemble_type = "SpecifiedDegreeDistEnsemble"
    degree_dist_base = [0, 10, 10, 10, 10, 10, 10, 10]
    ensemble_factory = fjgraph.GraphEnsembleFactory()
    result_one_half = []
    result_opt_ratio = []

    for plus in range(0, opts.max_degree, 10):
        degree_dist = list(degree_dist_base)
        degree_dist[num_of_degree] += plus

        ensemble = ensemble_factory.create(
            type="SpecifiedDegreeDistEnsemble",
            params={"degree_dist": degree_dist})
        r = fjexperiment.ip_lp_ensemble(ensemble, opts.trials)
        result_one_half.append([degree_dist[num_of_degree],
                                1.0 - r["ave_number_of_one_half_ratio"]])
        result_opt_ratio.append([degree_dist[num_of_degree],
                                 r["ave_opt_ration"]])

    # 結果出力
    print("= main result: 1.0 - ave_number_of_one_half_ratio =")
    print_table(result_one_half)
    print()
    print("= main result: ave_opt_ratio =")
    print_table(result_opt_ratio)


if __name__ == '__main__':
    report20130823_experiment()
