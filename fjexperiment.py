#!/usr/bin/env python
#coding: utf-8

from __future__ import division, print_function
import fjgraph
import fjutil
from collections import Counter


def count_one_half(values):
    counter = Counter(values)
    return counter[1/2]


def ip_lp_ensemble(ensemble, number_of_trials):
    sum_number_of_one_half = 0
    sum_lp_opt_value = 0.0
    sum_ip_opt_value = 0.0
    sum_opt_ratio = 0.0
    solver = fjgraph.VertexCoverSolver()

    print("= ip_lp_ensemble =")
    print("""input:
 * ensemble: {}
 * number_of_trials: {}""".format(ensemble, number_of_trials))
    print("""output:
 * ave_number_of_one_half
 * ave_number_of_one_half_ratio
 * ave_opt_ration
 * ave_lp_opt_value
 * ave_ip_opt_value""")

    progress_bar = fjutil.ProgressBar("Calculation", 80)
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
    print()

    # 結果返却
    ave_number_of_one_half = sum_number_of_one_half / number_of_trials
    ave_opt_ration = sum_opt_ratio / number_of_trials
    ave_ratio_of_one_half = \
        ave_number_of_one_half / ensemble.number_of_nodes()
    ave_lp_opt_value = sum_lp_opt_value / number_of_trials
    ave_ip_opt_value = sum_ip_opt_value / number_of_trials
    return { "ave_number_of_one_half": ave_number_of_one_half,
             "ave_number_of_one_half_ratio": ave_ratio_of_one_half,
             "ave_opt_ration": ave_opt_ration,
             "ave_lp_opt_value": ave_lp_opt_value,
             "ave_ip_opt_value": ave_ip_opt_value}
