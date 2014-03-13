#!/usr/bin/env python
#coding: utf-8

"平均頂点被覆分布を実験的に求めるプログラム"

# Copyright (c) 2013 Yuki Fujii
# Licensed under the MIT License

from __future__ import division, print_function
import fjgraph
import fjutil
import fjexperiment
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
    parser.add_option("-O", "--output",
                      dest="output",
                      type="string",
                      default=None,
                      help="set the output file prefix",
                      metavar="FILE")
    (opts, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("required a json file which define the ensemble")
    if not os.access(args[0], os.R_OK):
        parser.error("cannot read {}".format(args[0]))
    return (opts, args[0])


def flatten_ave_lp_vertex_cover_dist(dist):
    flatten_dist = Counter()
    for s, t in dist:
        flatten_dist[s/2 + t] += dist[s, t]
    return flatten_dist


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
    ave_ip_dist = fjexperiment.ave_vertex_cover_dist(ensemble, loop_count)
    ave_lp_table = fjexperiment.ave_lp_vertex_cover_dist(ensemble, loop_count)
    ave_lp_dist = flatten_ave_lp_vertex_cover_dist(ave_lp_table)

    # 結果出力
    print("= main result =")
    print("ave_ip_vertex_cover_dist:")
    fjutil.print_dist(ave_ip_dist, format="{:>5}: {}")
    print("ave_lp_vertex_cover_dist:")
    fjutil.print_dist(ave_lp_table, format="{:>10}: {}")
    print("ave_lp_vertex_cover_dist(flatten):")
    fjutil.print_dist(ave_lp_dist, format="{:>7.1f}: {}")

    # ファイル出力
    if opts.output:
        n = ensemble.num_of_nodes()
        ip_file = open(opts.output + "-ip.dat", "w")
        fillup_ip_dist = fjutil.fillup_dist(ave_ip_dist,
                                            start=0, stop=n, step=1)
        fjutil.output_dist(fillup_ip_dist, ip_file)
        lp_file = open(opts.output + "-lp.dat", "w")
        fillup_lp_dist = fjutil.fillup_dist(ave_lp_dist,
                                            start=0, stop=n, step=0.5)
        fjutil.output_dist(fillup_lp_dist, lp_file)


if __name__ == '__main__':
    ave_vertex_cover_dist_experiment()
