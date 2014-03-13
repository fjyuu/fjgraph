#coding: utf-8

"""研究用グラフライブラリ

以下の研究のために作成した．

* ランダムグラフアンサンブルにおける最小頂点被覆に関する研究
* ランダムグラフアンサンブルにおける2分割カットに関する研究
* ランダムグラフアンサンブルにおける3分割カットに関する研究
"""

# Copyright (c) 2013 Yuki Fujii @fjyuu
# Licensed under the MIT License

from __future__ import division, print_function
import networkx
import random
import itertools
from collections import Counter


def degree_dist(G):
    "グラフGの次数分布を求める"

    return Counter(networkx.degree(G).values())


class MinCutSolver(object):
    "最小カット問題のソルバー"

    def _simplify_multigraph(self, graph):
        if not isinstance(graph, networkx.MultiGraph):
            raise FJGraphError("MultiGraphじゃない")
        simple_graph = networkx.Graph()
        simple_graph.add_nodes_from(graph.nodes())
        for u, v in graph.edges():
            if u == v: continue  # 自己ループ削除
            if simple_graph.has_edge(u, v): continue
            attrs = graph[u][v]
            sum_weight = 0
            for attr in attrs.values():
                if "weight" in attr:
                    sum_weight += attr["weight"]
            simple_graph.add_edge(u, v, weight=sum_weight)
        return simple_graph

    def global_mincut(self, G):
        "全域最小カット重みを求める"

        if isinstance(G, networkx.MultiGraph):
            G = self._simplify_multigraph(G)
        mincut = None
        nodes = G.nodes()
        s = nodes.pop()
        for t in nodes:
            tmp = networkx.min_cut(G, s, t, capacity="weight")
            if mincut == None or tmp < mincut:
                mincut = tmp
        return mincut

    def st_mincut(self, G, s, t):
        "s-t最小カットを求める"

        if isinstance(G, networkx.MultiGraph):
            G = self._simplify_multigraph(G)
        return networkx.min_cut(G, s, t, capacity="weight")


class VertexCoverDistCalculator(object):
    "頂点被覆分布計算機"

    def _ok_check_values(self, check_values):
        "check_valuesが頂点被覆ならばTrue"

        for value in check_values:
            if value < 1:
                return False
        return True

    def vertex_cover_dist(self, G):
        "GのIP-頂点被覆分布を計算する"

        n = G.number_of_nodes()
        constraint_graph = ConstraintGraph(G)
        ret_dist = Counter()

        for variable_values in itertools.product([0, 1], repeat=n):
            weight = sum(variable_values)
            check_values = constraint_graph.calc_check_values(variable_values)
            if self._ok_check_values(check_values):
                ret_dist[weight] += 1

        return ret_dist

    def lp_vertex_cover_dist(self, G):
        "GのLP-頂点被覆分布を計算する"

        n = G.number_of_nodes()
        constraint_graph = ConstraintGraph(G)
        ret_table = Counter()

        for variable_values in itertools.product([0, 0.5, 1], repeat=n):
            num_of_one_half = variable_values.count(0.5)
            num_of_one = variable_values.count(1)
            check_values = constraint_graph.calc_check_values(variable_values)
            if self._ok_check_values(check_values):
                ret_table[(num_of_one_half, num_of_one)] += 1

        return ret_table


class VertexCoverSolver(object):
    "最小頂点被覆問題を計算機"

    def __init__(self, results_stream=None, log_stream=None,
                 error_stream=None, warning_stream=None):
        self._results_stream = results_stream
        self._log_stream = log_stream
        self._error_stream = error_stream
        self._warning_stream = warning_stream

    def lp_solve(self, G):
        "Gの最小頂点問題のLP解を出す"

        values = self._solve_with_cplex(G, easing=True)
        return VertexCoverSolver.LPSolution(G.nodes(), values)

    def ip_solve(self, G):
        "Gの最小頂点問題のIP解を出す"

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
        "最小頂点被覆問題の解"

        def __init__(self, nodes, values):
            self._nodes = tuple(nodes)
            self._values = tuple(values)

        def nodes(self):
            "頂点（変数）リスト"

            return tuple(self._nodes)

        def values(self):
            "頂点（変数）へ割り当てられた値"

            return tuple(self._values)

        def opt_value(self):
            "最小頂点被覆のサイズ（最適値）"

            return sum(self._values)

        def values_dict(self):
            nodes = self.nodes()
            values = self.values()
            return dict([[nodes[i], values[i]] for i in range(len(nodes))])

        def __str__(self):
            return "{}".format(self.values_dict())

    class LPSolution(Solution):
        "最小頂点被覆問題のLP解"

        pass

    class IPSolution(Solution):
        "最小頂点被覆問題のIP解"

        pass


class GraphEnsembleFactory(object):
    "グラフアンサンブルのファクトリークラス"

    def create(self, type, params):
        "グラフアンサンブルtypeのインスタンスをパラメータparamsで生成する"

        if type == "SpecifiedDegreeDistEnsemble":
            return SpecifiedDegreeDistEnsemble(**params)
        elif type == "MultiGraphEnsemble":
            return MultiGraphEnsemble(**params)
        elif type == "ErdosRenyiGraphEnsemble":
            return ErdosRenyiGraphEnsemble(**params)
        elif type == "NMGraphEnsemble":
            return NMGraphEnsemble(**params)
        else:
            raise FJGraphError(u"アンサンブルタイプが存在しない")


class GraphEnsemble(object):
    "グラフアンサンブルの基底クラス"

    def num_of_nodes(self):
        "頂点数を返す"

        return None

    def num_of_edges(self):
        "辺数を返す"

        return None

    def generate_graph(self):
        "グラフアンサンブルのインスタンスをひとつランダムに生成する"

        return None


class NMGraphEnsemble(GraphEnsemble):
    "頂点数nと辺数mを指定するランダムグラフアンサンブル"

    def __init__(self, num_of_nodes, num_of_edges):
        self._num_of_nodes = num_of_nodes
        self._num_of_edges = num_of_edges

    def num_of_nodes(self):
        return self._num_of_nodes

    def num_of_edges(self):
        return self._num_of_edges

    def generate_graph(self):
        n = self._num_of_nodes
        m = self._num_of_edges
        G = networkx.gnm_random_graph(n, m)
        for u, v in G.edges():
            G[u][v]["weight"] = 1
        return G

    def __str__(self):
        return "{}(num_of_nodes={}, num_of_edges={})".format(
            self.__class__.__name__, self._num_of_nodes, self._num_of_edges
        )


class ErdosRenyiGraphEnsemble(GraphEnsemble):
    "頂点数nと辺の生成確率pを指定するランダムグラフアンサンブル"

    def __init__(self, num_of_nodes, edge_prob):
        self._num_of_nodes = num_of_nodes
        self._edge_prob = edge_prob

    def num_of_nodes(self):
        return self._num_of_nodes

    def num_of_edges(self):
        raise FJGraphError(u"辺数は一定でない")

    def generate_graph(self):
        n = self._num_of_nodes
        p = self._edge_prob
        G = networkx.erdos_renyi_graph(n, p)
        for u, v in G.edges():
            G[u][v]["weight"] = 1
        return G

    def __str__(self):
        return "{}(num_of_nodes={}, edge_prob={})".format(
            self.__class__.__name__, self._num_of_nodes, self._edge_prob
        )


class MultiGraphEnsemble(GraphEnsemble):
    "自己ループと多重辺を許した(n,m)-ランダムグラフアンサンブル"

    def __init__(self, num_of_nodes, num_of_edges):
        self._num_of_nodes = num_of_nodes
        self._num_of_edges = num_of_edges

    def num_of_nodes(self):
        return self._num_of_nodes

    def num_of_edges(self):
        return self._num_of_edges

    def generate_graph(self):
        n = self._num_of_nodes
        m = self._num_of_edges

        G = networkx.MultiGraph()
        G.add_nodes_from(range(n))
        for edge in range(m):
            s = random.randint(0, n - 1)
            t = random.randint(0, n - 1)
            G.add_edge(s, t, weght=1)

        return G

    def __str__(self):
        return "{}(num_of_nodes={}, num_of_edges={})".format(
            self.__class__.__name__, self._num_of_nodes, self._num_of_edges
        )


class SpecifiedDegreeDistEnsemble(GraphEnsemble):
    """次数分布を指定したランダムグラフアンサンブル

    ここで，次数分布とは，整数のリストdegree_distである．
    degree_dist[i]は，次数iの頂点の個数を表す．
    """

    def __init__(self, degree_dist):
        hands_count = sum([i * dist for i, dist in enumerate(degree_dist)])
        if hands_count % 2 != 0:
            raise DegreeDistError(u"次数の合計が2で割り切れない")
        self.degree_dist = tuple(degree_dist)

    def num_of_nodes(self):
        return sum(self.degree_dist)

    def num_of_edges(self):
        sum_degree = sum([i * dist for i, dist in enumerate(self.degree_dist)])
        return int(sum_degree / 2)

    def generate_graph(self):
        node_size = self.num_of_nodes()

        shuffled_nodes = list(range(node_size))
        random.shuffle(shuffled_nodes)
        edge_num_table = []
        G = networkx.MultiGraph()
        for d, dist in enumerate(self.degree_dist):
            for i in range(dist):
                n = shuffled_nodes.pop()
                # 頂点nを次数dにする
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
            self.num_of_nodes(), self.num_of_edges())


class ConstraintGraph(object):
    "オリジナルグラフGの各辺に，頂点（チェックノード）を追加した二部グラフ"

    def __init__(self, G, check_function=lambda u, v: u + v):
        self.original_graph = G
        self.check_function = check_function

    def calc_check_values(self, variable_values):
        """チェックノード値を計算する

        variable_valuesは各頂点に割り当てる値を表すリストである．
        """

        G = self.original_graph
        if len(variable_values) != G.number_of_nodes():
            raise ValueError(u"variable_valuesのサイズがおかしい")

        check_values = []
        for u, v in G.edges():
            value = self.check_function(variable_values[u], variable_values[v])
            check_values.append(value)

        return check_values


class FJGraphError(Exception):
    pass


class DegreeDistError(FJGraphError):
    pass


class CutSetDistCalculator(object):
    "2分割カットセット重み分布計算機"

    @staticmethod
    def _check_cut_set(u, v):
        if u != v:
            return 1
        else:
            return 0

    def detailed_global_cutset_dist(self, G):
        """詳細全域カットセット重み分布A_G(u,w)を計算する

        A_G(u,w): 頂点をu個のグループとn-u個のグループに分割するとき，カットセッ
        トサイズがwになるパターン数
        """

        n = G.number_of_nodes()
        constraint_graph = ConstraintGraph(G, self._check_cut_set)
        ret_dist = Counter()

        for variable_values in itertools.product([0, 1], repeat=n):
            check_values = constraint_graph.calc_check_values(variable_values)
            u = sum(variable_values)
            w = sum(check_values)
            ret_dist[(u, w)] += 1

        return ret_dist

    def detailed_st_cutset_dist(self, G, s, t):
        """詳細s-tカットセット重み分布A_G^{s-t}(u,w)を計算する

        A_G^{s-t}(u,w): 頂点をu個のグループとn-u個のグループに分割するとき，s-tカッ
        トセットサイズがwになるパターン数
        """

        n = G.number_of_nodes()
        constraint_graph = ConstraintGraph(G, self._check_cut_set)
        ret_dist = Counter()

        for variable_values in itertools.product([0, 1], repeat=n):
            if variable_values[s] == variable_values[t]:
                continue
            check_values = constraint_graph.calc_check_values(variable_values)
            u = sum(variable_values)
            w = sum(check_values)
            ret_dist[(u, w)] += 1

        return ret_dist


class ThreeWayCutSetDistCalculator(object):
    "3分割カットセット分布計算機"

    def _partition_size(self, variable_values):
        "0,1,2の個数を数えてそれぞれ返す"

        count = Counter(variable_values)
        return count[0], count[1], count[2]

    @staticmethod
    def _check_cut_set(u, v):
        if u != v:
            return 1
        else:
            return 0

    def detailed_cutset_dist(self, G):
        """詳細カットセット分布A_G(j,k,l;w)を計算する

        A_G(j,k,l;w): 頂点をR（サイズj）, S（サイズk）, T（サイズl）の
        集合に3分割するときに，カットセットサイズがwになるパターン数
        """

        n = G.number_of_nodes()
        constraint_graph = ConstraintGraph(G, self._check_cut_set)
        ret_dist = Counter()

        for variable_values in itertools.product([0, 1, 2], repeat=n):
            check_values = constraint_graph.calc_check_values(variable_values)
            w = sum(check_values)
            j, k, l = self._partition_size(variable_values)
            ret_dist[(j, k, l, w)] += 1

        return ret_dist

    def all_cutset(self, G):
        "すべての3分割カットセットを求める"

        n = G.number_of_nodes()
        edges = G.edges()
        constraint_graph = ConstraintGraph(G, self._check_cut_set)
        cutsets = set()

        for variable_values in itertools.product([0, 1, 2], repeat=n):
            if 0 not in variable_values:
                continue
            if 1 not in variable_values:
                continue
            if 2 not in variable_values:
                continue
            check_values = constraint_graph.calc_check_values(variable_values)
            cutset = []
            for i, value in enumerate(check_values):
                if value == 1:
                    cutset.append(edges[i])
            cutsets.add(frozenset(cutset))

        return cutsets

    def cutset_dist(self, G):
        "3分割カット重み分布を求める"

        cutset_dist = Counter()
        cutsets = self.all_cutset(G)
        for cutset in cutsets:
            weight = len(cutset)
            cutset_dist[weight] += 1

        return cutset_dist
