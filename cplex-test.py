#!/usr/bin/env python
#coding: utf-8
import cplex
import sys

# 以下の最適化問題を解く：
# Maximize
#  obj: x1 + 2 x2 + 3 x3
# Subject To
#  c1: - x1 + x2 + x3 <= 20
#  c2: x1 - 3 x2 + x3 <= 30
# Bounds
#  0 <= x1 <= 40
# End

try:
    # Cplexオブジェクトを用意
    solver = cplex.Cplex()

    # 最大化問題
    solver.objective.set_sense(solver.objective.sense.maximize)

    # 最大化したい式と変数の定義域
    # 変数の下界はデフォルトで0.0になるので，ここでは省略している
    solver.variables.add(
        # 係数リスト
        obj   = [1.0, 2.0, 3.0],

        # 変数の上界リスト（ubはupper boundの略．下界はlbでlower boundの略．）
        ub    = [40.0, cplex.infinity, cplex.infinity],

        # 変数名リスト
        names = ["x1", "x2", "x3"]

        # Binary IPを指定
        # types = "BBB"
    )

    coefficients = [
        [["x1", "x2", "x3"], [-1.0, 1.0, 1.0]],
        [["x1", "x2", "x3"], [1.0, -3.0, 1.0]]
    ]

    # 線形制約
    solver.linear_constraints.add(
        # 線形式の係数リスト
        lin_expr = coefficients,

        # 不等号の向き(L or G?)（LはLess thanの略．GはGreater thanの略．）
        senses   = "LL",

        # 右辺の値（rhsはright-hand side）
        rhs      = [20.0, 30.0],

        # 式の名前
        names    = ["c1", "c2"]
    )

    # 問題をファイルに出力
    solver.write("cplex-test.lp")

    # 解く
    solver.solve()
except CplexError, exc:
    sys.stderr.write(exc)
    sys.exit(1)

# 結果を出力

num_constraints = solver.linear_constraints.get_num()
num_variables = solver.variables.get_num()

print
# solution.get_status() returns an integer code
print "Solution status = " , solver.solution.get_status(), ":",
# the following line prints the corresponding string
print solver.solution.status[solver.solution.get_status()]
print "Solution value  = ", solver.solution.get_objective_value()
slack = solver.solution.get_linear_slacks()
pi    = solver.solution.get_dual_values()
x     = solver.solution.get_values()
dj    = solver.solution.get_reduced_costs()
for i in range(num_constraints):
    print "Constraint %d:  Slack = %10f  Pi = %10f" % (i, slack[i], pi[i])
for j in range(num_variables):
    print "Variable %d:  Value = %10f Reduced cost = %10f" % (j, x[j], dj[j])
