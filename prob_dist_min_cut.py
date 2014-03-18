#!/usr/bin/env python
#coding: utf-8

"全域最小カット重み及びs-t最小カット重みがdelta以上になる確率を実験的に求めるプログラム"

# Copyright (c) 2013 Yuki Fujii @fjyuu
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
    parser.add_option("--non-cumulative",
                      dest="non_cumulative",
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


def prob_dist_min_cut_experiment():
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
    global_prob_dist = fjexperiment.prob_dist_global_min_cut(ensemble, num_of_trials)
    c_global_prob_dist = fjutil.cumulative_prob_dist(global_prob_dist, step=1)
    st_prob_dist = fjexperiment.prob_dist_st_min_cut(ensemble, num_of_trials)
    c_st_prob_dist = fjutil.cumulative_prob_dist(st_prob_dist, step=1)

    print("= main result =")

    if opts.non_cumulative:
        print(u"全域最小カット重みの確率分布:")
        fjutil.print_dist(global_prob_dist, format="{:>5}: {}")
        print(u"s-t最小カット重みの確率分布:")
        fjutil.print_dist(st_prob_dist, format="{:>5}: {}")
    else:
        print(u"全域最小カット重みがdelta以上の確率分布:")
        fjutil.print_dist(c_global_prob_dist, format="{:>5}: {}")
        print(u"s-t最小カット重みがdelta以上の確率分布:")
        fjutil.print_dist(c_st_prob_dist, format="{:>5}: {}")

    # ファイル出力
    if opts.output:
        global_file = open(opts.output + "-global.dat", "w")
        st_file = open(opts.output + "-st.dat", "w")
        if opts.non_cumulative:
            fjutil.output_dist(global_prob_dist, global_file)
            fjutil.output_dist(st_prob_dist, st_file)
        else:
            fjutil.output_dist(c_global_prob_dist, global_file)
            fjutil.output_dist(c_st_prob_dist, st_file)


if __name__ == "__main__":
    prob_dist_min_cut_experiment()
