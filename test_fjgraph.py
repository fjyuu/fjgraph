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
