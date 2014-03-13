# coding: utf-8

import unittest
import fjgraph
import networkx


class ConstraintGraphTest(unittest.TestCase):

    def setUp(self):
        self.G = networkx.MultiGraph()
        self.G.add_edge(0, 1, capacity=1)
        self.G.add_edge(0, 1, capacity=1)
        self.G.add_edge(1, 4, capacity=1)
        self.G.add_edge(1, 4, capacity=1)
        self.G.add_edge(4, 3, capacity=1)
        self.G.add_edge(3, 2, capacity=1)
        self.G.add_edge(2, 0, capacity=1)
        self.G.add_edge(1, 3, capacity=1)
        self.G.add_edge(1, 2, capacity=1)
        self.G.add_edge(1, 1, capacity=1)

    def test_calc_check_values(self):
        constraint_graph = fjgraph.ConstraintGraph(self.G)
        n = self.G.number_of_nodes()
        m = self.G.number_of_edges()
        cvalues = constraint_graph.calc_check_values([0] * n)
        self.assertEqual(cvalues, [0] * m)


class VertexCoverSolverTest(unittest.TestCase):

    def setUp(self):
        self.solver = fjgraph.VertexCoverSolver()

    def test_chain_graph(self):
        G = networkx.Graph()
        G.add_edge(0, 1)
        G.add_edge(1, 2)

        lp_solution = self.solver.lp_solve(G)
        self.assertEqual(lp_solution.opt_value(), 1.0)
        self.assertEqual(lp_solution.values_dict(),
                         {0: 0.0, 1: 1.0, 2: 0.0})

        ip_solution = self.solver.ip_solve(G)
        self.assertEqual(ip_solution.opt_value(), 1.0)
        self.assertEqual(lp_solution.values_dict(),
                         {0: 0.0, 1: 1.0, 2: 0.0})

    def test_perfect_graph(self):
        G = networkx.complete_graph(4)

        lp_solution = self.solver.lp_solve(G)
        self.assertEqual(lp_solution.opt_value(), 2.0)
        self.assertEqual(lp_solution.values_dict(),
                         {0: 0.5, 1: 0.5, 2: 0.5, 3: 0.5})

        ip_solution = self.solver.ip_solve(G)
        self.assertEqual(ip_solution.opt_value(), 3.0)
        self.assertEqual(ip_solution.values_dict(),
                         {0: 1.0, 1: 1.0, 2: 1.0, 3: 0.0})

    def test_self_loop(self):
        G = networkx.MultiGraph()
        G.add_edge(0, 0)

        lp_solution = self.solver.lp_solve(G)
        self.assertEqual(lp_solution.opt_value(), 0.5)
        self.assertEqual(lp_solution.values_dict(),
                         {0: 0.5})

        ip_solution = self.solver.ip_solve(G)
        self.assertEqual(ip_solution.opt_value(), 1.0)
        self.assertEqual(ip_solution.values_dict(),
                         {0: 1.0})


class ThreeWayCutSetDistCalculatorTest(unittest.TestCase):
    "ThreeWayCutSetDistCalculatorクラスのテスト"

    @classmethod
    def setUpClass(self):
        self.calc = fjgraph.ThreeWayCutSetDistCalculator()

    def test_detailed_cutset_dist(self):
        "詳細カットセット分布を計算する"

        calc = self.calc

        G = networkx.MultiGraph()
        G.add_edge(0, 1)
        G.add_edge(1, 2)
        G.add_edge(2, 0)

        ret = calc.detailed_cutset_dist(G)
        self.assertEqual(ret[(1, 1, 1, 3)], 6)

        # (j, k, l, w) num_of_patterns
        # ----------------------------
        # (0, 0, 3, 0) 1
        # (0, 1, 2, 2) 3
        # (0, 2, 1, 2) 3
        # (0, 3, 0, 0) 1
        # (1, 0, 2, 2) 3
        # (1, 1, 1, 3) 6
        # (1, 2, 0, 2) 3
        # (2, 0, 1, 2) 3
        # (2, 1, 0, 2) 3
        # (3, 0, 0, 0) 1

    def test_all_cutset(self):
        "すべての3分割カットセットを求める"

        calc = self.calc

        G = networkx.MultiGraph()
        G.add_edge(0, 1)
        G.add_edge(1, 2)
        G.add_edge(2, 0)

        ret = calc.all_cutset(G)

        # 3分割カットセットは1パターンのみ
        self.assertEqual(len(ret), 1)
        edges = frozenset(G.edges())
        self.assertTrue(edges in ret)

    def test_cutset_dist(self):
        "3分割カットセット重み分布を求める"

        calc = self.calc

        G = networkx.MultiGraph()
        G.add_edge(0, 1)
        G.add_edge(1, 2)
        G.add_edge(2, 0)

        ret = calc.cutset_dist(G)
        self.assertEqual(ret[0], 0)
        self.assertEqual(ret[1], 0)
        self.assertEqual(ret[2], 0)
        self.assertEqual(ret[3], 1)


class ErdosRenyiGraphEnsembleTest(unittest.TestCase):

    def test_generate_graph(self):
        n = 10
        p = 0.8
        ensemble = fjgraph.ErdosRenyiGraphEnsemble(
            num_of_nodes=n,
            edge_prob=p
        )
        self.assertEqual(ensemble.num_of_nodes(), n)
        G = ensemble.generate_graph()
        self.assertTrue(isinstance(G, networkx.Graph))
        self.assertTrue(not isinstance(G, networkx.MultiGraph))


class NMGraphEnsembleTest(unittest.TestCase):

    def test_generate_graph(self):
        n = 10
        m = 10
        ensemble = fjgraph.NMGraphEnsemble(
            num_of_nodes=n,
            num_of_edges=m
        )
        self.assertEqual(ensemble.num_of_nodes(), n)
        self.assertEqual(ensemble.num_of_edges(), m)
        G = ensemble.generate_graph()
        self.assertTrue(isinstance(G, networkx.Graph))
        self.assertTrue(not isinstance(G, networkx.MultiGraph))
        self.assertEqual(G.number_of_nodes(), n)
        self.assertEqual(G.number_of_edges(), m)
