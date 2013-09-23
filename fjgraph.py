#coding: utf-8

import networkx
import random
import itertools
from collections import Counter


class VertexCoverDistCalculator(object):

    def _ok_check_values(self, check_values):
        for value in check_values:
            if value < 1:
                return False
        return True

    def vertex_cover_dist(self, G):
        n = G.number_of_nodes()
        constraint_graph = ConstraintGraph(G)
        ret_dist = Counter()

        for variable_values in itertools.product([0, 1], repeat=n):
            weight = sum(variable_values)
            check_values = constraint_graph.calc_check_values(variable_values)
            if self._ok_check_values(check_values):
                ret_dist[weight] += 1

        return ret_dist

    def slack_vertex_cover_dist(self, G):
        n = G.number_of_nodes()
        constraint_graph = ConstraintGraph(G)
        ret_table = Counter()

        for variable_values in itertools.product([0, 0.5, 1], repeat=n):
            number_of_one_half = variable_values.count(0.5)
            number_of_one = variable_values.count(1)
            check_values = constraint_graph.calc_check_values(variable_values)
            if self._ok_check_values(check_values):
                ret_table[(number_of_one_half, number_of_one)] += 1

        return ret_table


class VertexCoverSolver(object):

    def __init__(self, results_stream=None, log_stream=None,
                 error_stream=None, warning_stream=None):
        self._results_stream = results_stream
        self._log_stream = log_stream
        self._error_stream = error_stream
        self._warning_stream = warning_stream

    def lp_solve(self, G):
        values = self._solve_with_cplex(G, easing=True)
        return VertexCoverSolver.LPSolution(G.nodes(), values)

    def ip_solve(self, G):
        values = self._solve_with_cplex(G, easing=False)
        return VertexCoverSolver.IPSolution(G.nodes(), values)

    def _create_cplex_solver(self):
        import cplex
        solver = cplex.Cplex()
        solver.set_results_stream(self._results_stream)
        solver.set_log_stream(self._log_stream)
        solver.set_warning_stream(self._warning_stream)
        solver.set_error_stream(self._error_stream)
        return solver

    def _solve_with_cplex(self, G, easing=False):
        solver = self._create_cplex_solver()

        # 最小化問題
        solver.objective.set_sense(solver.objective.sense.minimize)

        # 最小化したい式と変数の定義域
        # 変数の下界はデフォルトで0.0になるので，ここでは省略している
        if easing:
            variable_type = solver.variables.type.continuous
        else:
            variable_type = solver.variables.type.binary
        solver.variables.add(
            # 係数リスト
            obj=[1.0 for i in range(G.number_of_nodes())],
            # 変数の上界リスト
            ub=[1.0 for i in range(G.number_of_nodes())],
            # 変数名リスト
            names=[str(n) for n in G.nodes()],
            # Binary IPを指定
            types=variable_type * G.number_of_nodes()
        )

        coefficients = []
        for i, edge in enumerate(G.edges()):
            if edge[0] == edge[1]:  # self-loop
                coefficients.append([[str(edge[0])], [2.0]])
            else:
                coefficients.append([[str(edge[0]), str(edge[1])], [1.0, 1.0]])

        # 線形制約 x_i + x_j >= 1 for (x_i, x_j) in edges
        solver.linear_constraints.add(
            # 線形式の係数リスト
            lin_expr=coefficients,
            # 不等号の向き
            senses="G" * G.number_of_edges(),
            # 右辺の値
            rhs=[1.0 for i in range(G.number_of_edges())],
            # 式の名前
            names=["c{}".format(i) for i in range(G.number_of_edges())]
        )

        solver.solve()
        return solver.solution.get_values()

    class Solution(object):

        def __init__(self, nodes, values):
            self._nodes = tuple(nodes)
            self._values = tuple(values)

        def nodes(self):
            return tuple(self._nodes)

        def values(self):
            return tuple(self._values)

        def opt_value(self):
            return sum(self._values)

        def values_dict(self):
            nodes = self.nodes()
            values = self.values()
            return dict([[nodes[i], values[i]] for i in range(len(nodes))])

        def __str__(self):
            return "{}".format(self.values_dict())

    class LPSolution(Solution):
        pass

    class IPSolution(Solution):
        pass


class GraphEnsembleFactory(object):
    def create(self, type, params):
        if type == "SpecifiedDegreeDistEnsemble":
            return SpecifiedDegreeDistEnsemble(**params)
        else:
            raise FJGraphError("アンサンブルタイプが存在しない")


class GraphEnsemble(object):
    def number_of_nodes(self):
        return None

    def number_of_edges(self):
        return None

    def generate_graph(self):
        return None


class SpecifiedDegreeDistEnsemble(GraphEnsemble):
    def __init__(self, degree_dist):
        hands_count = sum([i * dist for i, dist in enumerate(degree_dist)])
        if hands_count % 2 != 0:
            raise DegreeDistError("次数の合計が2で割り切れない")
        self.degree_dist = tuple(degree_dist)

    def number_of_nodes(self):
        return sum(self.degree_dist)

    def number_of_edges(self):
        return sum([i * dist for i, dist in enumerate(self.degree_dist)]) / 2

    def generate_graph(self):
        node_size = self.number_of_nodes()

        shuffled_nodes = list(range(node_size))
        random.shuffle(shuffled_nodes)
        edge_num_table = []
        G = networkx.MultiGraph()
        for d, dist in enumerate(self.degree_dist):
            for i in range(dist):
                n = shuffled_nodes.pop()
                #print("頂点{0}を次数{1}にする".format(n,d))
                G.add_node(n)
                edge_num_table.extend([n] * d)

        random.shuffle(edge_num_table)
        while edge_num_table:
            a = edge_num_table.pop()
            b = edge_num_table.pop()
            G.add_edge(a, b, weight=1)

        return G

    def __str__(self):
        return "{}(degree_dist={}) [n={}, m={}]".format(
            self.__class__.__name__, self.degree_dist,
            self.number_of_nodes(), self.number_of_edges())


class ConstraintGraph(object):
    def __init__(self, G, check_function=lambda u, v: u + v):
        self.original_graph = G
        self.check_function = check_function

    def calc_check_values(self, variable_values):
        G = self.original_graph
        if len(variable_values) != G.number_of_nodes():
            raise ValueError("variable_valuesのサイズがおかしい")

        check_values = []
        for u, v in G.edges():
            value = self.check_function(variable_values[u], variable_values[v])
            check_values.append(value)

        return check_values


class FJGraphError(Exception):
    pass


class DegreeDistError(FJGraphError):
    pass
