#!/usr/bin/env python
#coding: utf-8

"最小頂点被覆サイズがdelta以上になる確率を実験的に求めるプログラム"

# Copyright (c) 2013 Yuki Fujii
# Licensed under the MIT License

from __future__ import division, print_function
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
    parser.add_option("--probdist",
                      dest="probdist",
                      action="store_true",
                      default=False,
                      help="report probability distribution (not acumulated)")
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


def prob_dist_min_vertex_cover_experiment():
    # 引数処理
    (opts, json_file) = parse_arguments()

    # 実験パラメータ
    print("= experiment params =")
    random.seed(opts.seed)
    ensemble_def = fjutil.load_json_file(json_file)
    ensemble = fjgraph.GraphEnsembleFactory().create(**ensemble_def)
    num_of_trials = opts.trials
    print("ensemble: {}".format(ensemble))
    print("seed: {}".format(opts.seed))
    print("num_of_trials: {}".format(num_of_trials))
    print()

    # 実験
    ip_prob_dist = fjexperiment.prob_dist_min_vertex_cover(ensemble, num_of_trials)
    ip_c_prob_dist = fjutil.cumulative_prob_dist(ip_prob_dist, step=1)
    lp_prob_dist = fjexperiment.prob_dist_lp_min_vertex_cover(ensemble, num_of_trials)
    lp_c_prob_dist = fjutil.cumulative_prob_dist(lp_prob_dist, step=0.5)

    print("= main result =")

    if opts.probdist:
        print(u"最小頂点被覆サイズの確率分布:")
        fjutil.print_counter(ip_prob_dist, format="{:>5}: {}")
    else:
        print(u"最小頂点被覆サイズがdelta以上の確率分布:")
        fjutil.print_counter(ip_c_prob_dist, format="{:>5}: {}")
    print()

    if opts.probdist:
        print(u"半整数を許したときの最小頂点被覆サイズの確率分布:")
        fjutil.print_counter(lp_prob_dist, format="{:>5}: {}")
    else:
        print(u"半整数を許したときの最小頂点被覆サイズがdelta以上の確率分布:")
        fjutil.print_counter(lp_c_prob_dist, format="{:>5}: {}")

    # ファイル出力
    if opts.output:
        ip_file = open(opts.output + "-ip.dat", "w")
        lp_file = open(opts.output + "-lp.dat", "w")
        if opts.probdist:
            fjutil.output_counter(ip_prob_dist, ip_file)
            fjutil.output_counter(lp_prob_dist, lp_file)
        else:
            fjutil.output_counter(ip_c_prob_dist, ip_file)
            fjutil.output_counter(lp_c_prob_dist, lp_file)


if __name__ == '__main__':
    prob_dist_min_vertex_cover_experiment()
