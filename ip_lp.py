#!/usr/bin/env python
#coding: utf-8

"ランダムグラフアンサンブルにおける最小頂点被覆問題のIP解とLP解を比較するプログラム"

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
    (opts, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("required a json file which define the ensemble")
    if not os.access(args[0], os.R_OK):
        parser.error("cannot read {}".format(args[0]))
    return (opts, args[0])


def lp_ip_ensemble_experiment():
    # 引数処理
    (opts, json_file) = parse_arguments()

    # 実験パラメータの設定と確認
    print("= experiment params =")
    random.seed(opts.seed)
    ensemble_def = fjutil.load_json_file(json_file)
    ensemble = fjgraph.GraphEnsembleFactory().create(**ensemble_def)
    print("ensemble: {}".format(ensemble))
    print("num_of_trials: {}".format(opts.trials))
    print("seed: {}".format(opts.seed))
    print()

    # 結果出力
    r = fjexperiment.ip_lp_ensemble(ensemble, opts.trials)
    print("= main result =")
    print("ave_num_of_one_half: {:.4} ({:.2%})".format(
            r["ave_num_of_one_half"], r["ave_num_of_one_half_ratio"]))
    print("ave_opt_ration: {:.4}".format(r["ave_opt_ration"]))
    print("ave_lp_opt_value: {:.4}".format(r["ave_lp_opt_value"]))
    print("ave_ip_opt_value: {:.4}".format(r["ave_ip_opt_value"]))
    print("lp_equal_ip_prob: {:.4}".format(r["lp_equal_ip_prob"]))


if __name__ == '__main__':
    lp_ip_ensemble_experiment()
