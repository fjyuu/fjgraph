import unittest
import fjgraph
import networkx

class ConstraintGraphTest(unittest.TestCase):

    def setUp(self):
        self.G = networkx.MultiGraph()
        self.G.add_edge(0,1, capacity = 1)
        self.G.add_edge(0,1, capacity = 1)
        self.G.add_edge(1,4, capacity = 1)
        self.G.add_edge(1,4, capacity = 1)
        self.G.add_edge(4,3, capacity = 1)
        self.G.add_edge(3,2, capacity = 1)
        self.G.add_edge(2,0, capacity = 1)
        self.G.add_edge(1,3, capacity = 1)
        self.G.add_edge(1,2, capacity = 1)
        self.G.add_edge(1,1, capacity = 1)

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
        G.add_edge(0,1)
        G.add_edge(1,2)

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
        G.add_edge(0,0)

        lp_solution = self.solver.lp_solve(G)
        self.assertEqual(lp_solution.opt_value(), 0.5)
        self.assertEqual(lp_solution.values_dict(),
                         {0: 0.5})

        ip_solution = self.solver.ip_solve(G)
        self.assertEqual(ip_solution.opt_value(), 1.0)
        self.assertEqual(ip_solution.values_dict(),
                         {0: 1.0})
