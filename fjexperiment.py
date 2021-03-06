#coding: utf-8

"""典型的な実験

頻繁に行う実験を集めた．
"""

# Copyright (c) 2013 Yuki Fujii @fjyuu
# Licensed under the MIT License

from __future__ import division, print_function
import fjgraph
import fjutil
from collections import Counter


def ave_3way_detailed_cutset_dist(ensemble, num_of_trials):
    "平均3分割詳細カットセット分布を実験的に求める"

    sum_dist = Counter()
    calc = fjgraph.ThreeWayCutSetDistCalculator()

    print("""= ave_3way_detailed_cutset_dist =
input:
 * ensemble: {}
 * num_of_trials: {}
output:
 * ave_3way_detailed_cutset_dist""".format(ensemble, num_of_trials))

    progress_bar = fjutil.ProgressBar("Calculation", 80)
    progress_bar.begin()
    for i in range(num_of_trials):
        G = ensemble.generate_graph()
        ret_dist = calc.detailed_cutset_dist(G)
        sum_dist += ret_dist
        progress_bar.write(i / num_of_trials)
    progress_bar.end()

    ave_dist = Counter(dict((key, value / num_of_trials)
                            for key, value in sum_dist.items()))
    return ave_dist


def ave_vertex_cover_dist(ensemble, num_of_trials):
    "平均IP-頂点被覆分布を実験的に求める"

    sum_dist = Counter()
    dist_calc = fjgraph.VertexCoverDistCalculator()

    print("""= ave_vertex_cover_dist =
input:
 * ensemble: {}
 * num_of_trials: {}
output:
 * ave_vertex_cover_dist""".format(ensemble, num_of_trials))

    progress_bar = fjutil.ProgressBar("Calculation", 80)
    progress_bar.begin()
    for i in range(num_of_trials):
        G = ensemble.generate_graph()
        ret_dist = dist_calc.vertex_cover_dist(G)
        sum_dist += ret_dist
        progress_bar.write(i / num_of_trials)
    progress_bar.end()

    ave_dist = Counter(dict((key, value / num_of_trials)
                            for key, value in sum_dist.items()))
    return ave_dist


def ave_lp_vertex_cover_dist(ensemble, num_of_trials):
    "平均LP-頂点被覆分布を実験的に求める"

    sum_table = Counter()
    dist_calc = fjgraph.VertexCoverDistCalculator()

    print("""= ave_lp_vertex_cover_dist =
input:
 * ensemble: {}
 * num_of_trials: {}
output:
 * ave_lp_vertex_cover_dist""".format(ensemble, num_of_trials))

    progress_bar = fjutil.ProgressBar("Calculation", 80)
    progress_bar.begin()
    for i in range(num_of_trials):
        G = ensemble.generate_graph()
        ret_table = dist_calc.lp_vertex_cover_dist(G)
        sum_table += ret_table
        progress_bar.write(i / num_of_trials)
    progress_bar.end()

    ave_table = Counter(dict((key, value / num_of_trials)
                             for key, value in sum_table.items()))
    return ave_table



def count_one_half(values):
    "valuesの中に1/2はいくつあるか求める"

    counter = Counter(values)
    return counter[1/2]


def ip_lp_ensemble(ensemble, num_of_trials):
    "アンサンブルにおける最小頂点被覆問題のIP解とLP解を比較する"

    sum_num_of_one_half = 0
    sum_lp_opt_value = 0.0
    sum_ip_opt_value = 0.0
    sum_opt_ratio = 0.0
    count_lp_equal_ip = 0
    sum_difference_opt = 0.0
    solver = fjgraph.VertexCoverSolver()

    print("= ip_lp_ensemble =")
    print("""input:
 * ensemble: {}
 * num_of_trials: {}""".format(ensemble, num_of_trials))
    print("""output:
 * ave_num_of_one_half
 * ave_num_of_one_half_ratio
 * ave_opt_ration
 * ave_lp_opt_value
 * ave_ip_opt_value
 * lp_equal_ip_prob
 * ave_difference_opt""")

    progress_bar = fjutil.ProgressBar("Calculation", 80)
    progress_bar.begin()
    for i in range(num_of_trials):
        G = ensemble.generate_graph()

        lp_solution = solver.lp_solve(G)
        num_of_one_half = count_one_half(lp_solution.values())
        lp_opt_value = lp_solution.opt_value()

        ip_solution = solver.ip_solve(G)
        ip_opt_value = ip_solution.opt_value()

        sum_num_of_one_half += num_of_one_half
        sum_opt_ratio += lp_opt_value / ip_opt_value
        sum_lp_opt_value += lp_opt_value
        sum_ip_opt_value += ip_opt_value
        sum_difference_opt += ip_opt_value - lp_opt_value
        if lp_opt_value == ip_opt_value:
            count_lp_equal_ip += 1
        progress_bar.write(i / num_of_trials)
    progress_bar.end()
    print()

    # 結果返却
    ave_num_of_one_half = sum_num_of_one_half / num_of_trials
    ave_opt_ration = sum_opt_ratio / num_of_trials
    ave_ratio_of_one_half = \
        ave_num_of_one_half / ensemble.num_of_nodes()
    ave_lp_opt_value = sum_lp_opt_value / num_of_trials
    ave_ip_opt_value = sum_ip_opt_value / num_of_trials
    lp_equal_ip_prob = count_lp_equal_ip / num_of_trials
    ave_difference_opt = sum_difference_opt / num_of_trials
    return {"ave_num_of_one_half": ave_num_of_one_half,
            "ave_num_of_one_half_ratio": ave_ratio_of_one_half,
            "ave_opt_ration": ave_opt_ration,
            "ave_lp_opt_value": ave_lp_opt_value,
            "ave_ip_opt_value": ave_ip_opt_value,
            "lp_equal_ip_prob": lp_equal_ip_prob,
            "ave_difference_opt": ave_difference_opt}


def prob_dist_min_vertex_cover(ensemble, num_of_trials):
    "最小頂点被覆問題のIP-最適値の確率分布を実験的に求める"

    print("= prob_min_vertex_cover =")
    print("""input:
 * ensemble: {}
 * num_of_trials: {}""".format(ensemble, num_of_trials))
    print("""output:
 * prob_dist_min_vertex_cover""")

    return _prob_dist_min_vertex_cover(ensemble, num_of_trials, "IP")


def prob_dist_lp_min_vertex_cover(ensemble, num_of_trials):
    "最小頂点被覆問題のLP-最適値の確率分布を実験的に求める"

    print("= prob_lp_min_vertex_cover =")
    print("""input:
 * ensemble: {}
 * num_of_trials: {}""".format(ensemble, num_of_trials))
    print("""output:
 * prob_dist_lp_min_vertex_cover""")

    return _prob_dist_min_vertex_cover(ensemble, num_of_trials, "LP")


def _prob_dist_min_vertex_cover(ensemble, num_of_trials, type="IP"):
    "最小頂点被覆問題のIP-最適値もしくはLP-最適値の確率分布を実験的に求める"

    sum_dist = Counter()
    solver = fjgraph.VertexCoverSolver()
    progress_bar = fjutil.ProgressBar("Calculation", 80)

    progress_bar.begin()
    for i in range(num_of_trials):
        G = ensemble.generate_graph()
        if type == "IP":
            solution = solver.ip_solve(G)
        elif type == "LP":
            solution = solver.lp_solve(G)
        else:
            raise ExperimentError(u"typeは'IP'もしくは'LP'でなければいけません")
        opt_value = solution.opt_value()
        sum_dist[round(opt_value, 1)] += 1 # 小数点第2位以下は誤差
        progress_bar.write(i / num_of_trials)
    progress_bar.end()

    return dict(
        (key, value / num_of_trials) for key, value in sum_dist.items()
    )


def prob_dist_global_min_cut(ensemble, num_of_trials):
    "全域最小カット重みの確率分布を実験的に求める"

    print("= prob_dist_global_min_cut =")
    print("""input:
 * ensemble: {}
 * num_of_trials: {}""".format(ensemble, num_of_trials))
    print("""output:
 * prob_dist_global_min_cut""")

    return _prob_dist_min_cut(ensemble, num_of_trials, type="global")


def prob_dist_st_min_cut(ensemble, num_of_trials):
    "s-t最小カット重みの確率分布を実験的に求める"

    print("= prob_dist_st_min_cut =")
    print("""input:
 * ensemble: {}
 * num_of_trials: {}""".format(ensemble, num_of_trials))
    print("""output:
 * prob_dist_st_min_cut""")

    return _prob_dist_min_cut(ensemble, num_of_trials, type="st")


def _prob_dist_min_cut(ensemble, num_of_trials, type="global"):
    "s-t最小カット重みもしくは全域最小カット重みの確率分布を実験的に求める"

    sum_dist = Counter()
    calc = fjgraph.MinCutCalculator()
    progress_bar = fjutil.ProgressBar("Calculation", 80)

    progress_bar.begin()
    for i in range(num_of_trials):
        G = ensemble.generate_graph()
        if type == "st":
            min_cut = calc.st_mincut(G, 0, 1)
        elif type == "global":
            min_cut = calc.global_mincut(G)
        else:
            raise ExperimentError(u"typeは'st'もしくは'global'でなければいけません")
        sum_dist[min_cut] += 1
        progress_bar.write(i / num_of_trials)
    progress_bar.end()

    return dict(
        (key, value / num_of_trials) for key, value in sum_dist.items()
    )


class ExperimentError(Exception):
    pass
