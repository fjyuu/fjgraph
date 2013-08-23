#!/usr/bin/env python
#coding: utf-8

from __future__ import division, print_function, unicode_literals
import fjgraph
import fjutil
import fjexperiment
import random


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


def ave_vertex_cover_dist_experiment():
    # 引数処理
    (opts, json_file) = parse_arguments()

    # 実験パラメータ
    print("= experiment params =")
    random.seed(opts.seed)
    ensemble_def = fjutil.load_json_file(json_file)
    ensemble = fjgraph.GraphEnsembleFactory().create(**ensemble_def)
    loop_count = opts.trials
    print("ensemble: {}".format(ensemble))
    print("seed: {}".format(opts.seed))
    print("num_of_trials: {}".format(loop_count))
    print()

    # 実験
    ave_dist = fjexperiment.ave_vertex_cover_dist(ensemble, loop_count)
    ave_table = fjexperiment.ave_slack_vertex_cover_dist(ensemble, loop_count)

    print("= main result =")
    print("ave_vertex_cover_dist:")
    fjutil.print_counter(ave_dist, format="{:>5}: {}")
    print("ave_slack_vertex_cover_dist:")
    fjutil.print_counter(ave_table, format="{:>10}: {}")


if __name__ == '__main__':
    ave_vertex_cover_dist_experiment()
