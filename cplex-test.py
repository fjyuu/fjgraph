#!/usr/bin/env python
#encoding: utf8
import cplex

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
    solver = cplex.Cplex()

    # 最小化問題
    solver.objective.set_sense(solver.objective.sense.maximize)

    # 最小化したい式と変数の定義域
    # 変数の下界はデフォルトで0.0になるので，ここでは省略している
    solver.variables.add(
        obj   = [1.0, 2.0, 3.0], # 係数リスト
        ub    = [40.0, cplex.infinity, cplex.infinity], # 変数の上界リスト
        names = ["x1", "x2", "x3"] # 変数名リスト
        # types = "BBB" # Binary IP
    )

    # can query variables like the following:

    # lbs is a list of all the lower bounds
    lbs = solver.variables.get_lower_bounds()
    # ub1 is just the first lower bound
    ub1 = solver.variables.get_upper_bounds(0)
    # names is ["x1", "x3"]
    names = solver.variables.get_names([0, 2])

    coefficients = [
        [["x1", "x2", "x3"], [-1.0, 1.0, 1.0]],
        [["x1", "x2", "x3"], [1.0, -3.0, 1.0]]
    ]

    # 線形制約
    solver.linear_constraints.add(
        lin_expr = coefficients, # 線形式の係数リスト
        senses   = "LL", # 不等号の向き(L or G?)
        rhs      = [20.0, 30.0], # 右辺の値
        names    = ["c1", "c2"] # 名前
    )

    # because there are two arguments, they are taken to specify a range
    # thus, cols is the entire constraint matrix as a list of column vectors
    cols = solver.variables.get_cols("x1", "x3")

    solver.solve()
except CplexError, exc:
    print exc

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

solver.write("cplex-test.lp")
