from unittest import TestCase

from DiGraph import DiGraph


class TestDiGraph(TestCase):

    def setUp(self) -> None:
        self.graph = DiGraph()
        self.graph.add_node(1, (1, 1, 1))
        self.graph.add_node(2, (2, 2, 2))
        self.graph.add_node(3, (3, 3, 3))
        self.graph.add_node(4, (4, 4, 4))
        self.graph.add_node(5, (5, 5, 5))
        for i in range(4):
            self.graph.add_edge(i+1,i+2,i+1)


    def test_v_size(self):
        self.assertEqual(5,self.graph.v_size())
        self.graph.add_node(6)
        self.assertEqual(6,self.graph.v_size())
        self.graph.remove_node(1)
        self.assertEqual(5,self.graph.v_size())

    def test_e_size(self):
        self.assertEqual(4,self.graph.e_size())
        self.graph.add_edge(5,1,2)
        self.assertEqual(5,self.graph.e_size())
        self.graph.remove_edge(1,2)
        self.assertEqual(4,self.graph.e_size())

    def test_get_all_v(self):
        self.assertEqual(self.graph._nodes,self.graph.get_all_v())
        self.graph.add_node(7,(7,7,7))
        self.assertEqual(self.graph._nodes,self.graph.get_all_v())
        self.graph.remove_node(5)
        self.assertEqual(self.graph._nodes,self.graph.get_all_v())

    def test_all_in_edges_of_node(self):
        self.assertIsNotNone(self.graph.all_in_edges_of_node(2).get(1))
        self.assertEqual(1,self.graph.all_in_edges_of_node(2)[1])
        self.assertIsNotNone(self.graph.all_in_edges_of_node(3).get(2))
        self.assertEqual(2,self.graph.all_in_edges_of_node(3)[2])
        self.assertIsNotNone(self.graph.all_in_edges_of_node(4).get(3))
        self.assertEqual(3,self.graph.all_in_edges_of_node(4)[3])
        self.assertIsNotNone(self.graph.all_in_edges_of_node(5).get(4))
        self.assertEqual(4,self.graph.all_in_edges_of_node(5)[4])

    def test_all_out_edges_of_node(self):
        self.assertIsNotNone(self.graph.all_out_edges_of_node(1).get(2))
        self.assertEqual(1,self.graph.all_out_edges_of_node(1)[2])
        self.assertIsNotNone(self.graph.all_out_edges_of_node(2).get(3))
        self.assertEqual(2,self.graph.all_out_edges_of_node(2)[3])
        self.assertIsNotNone(self.graph.all_out_edges_of_node(3).get(4))
        self.assertEqual(3,self.graph.all_out_edges_of_node(3)[4])
        self.assertIsNotNone(self.graph.all_out_edges_of_node(4).get(5))
        self.assertEqual(4,self.graph.all_out_edges_of_node(4)[5])

    def test_get_mc(self):
        self.assertEqual(9,self.graph.get_mc())
        self.graph.add_node(6)
        self.assertEqual(10,self.graph.get_mc())
        self.graph.add_node(6)
        self.assertEqual(10,self.graph.get_mc())
        self.graph.remove_edge(1,2)
        self.assertEqual(11,self.graph.get_mc())
        self.graph.remove_edge(1,2)
        self.assertEqual(11,self.graph.get_mc())
        self.graph.remove_node(1)
        self.assertEqual(12,self.graph.get_mc())
        self.graph.remove_node(1)
        self.assertEqual(12,self.graph.get_mc())
        self.graph.add_edge(4,3,-1)
        self.assertEqual(12,self.graph.get_mc())
        self.graph.add_edge(2,3,4)
        self.assertEqual(12,self.graph.get_mc())

    def test_add_edge(self):
        self.graph.add_edge(5,1,2)
        self.assertIsNotNone(self.graph.all_out_edges_of_node(5)[1])
        self.assertIsNotNone(self.graph.all_in_edges_of_node(1)[5])
        self.assertEqual(2,self.graph.all_in_edges_of_node(1)[5])
        self.assertEqual(2,self.graph.all_out_edges_of_node(5)[1])
        self.graph.add_edge(2,4,-3)
        self.assertIsNone(self.graph.all_out_edges_of_node(2).get(4))
        self.assertIsNone(self.graph.all_in_edges_of_node(4).get(2))
        self.graph.add_edge(5,1,3)
        self.assertEqual(2,self.graph.all_in_edges_of_node(1)[5])
        self.assertEqual(2,self.graph.all_out_edges_of_node(5)[1])
        self.assertFalse(self.graph.add_edge(10,100,90))

    def test_add_node(self):
        self.assertIsNone(self.graph.get_all_v().get(6))
        self.graph.add_node(6)
        self.assertIsNotNone(self.graph.get_all_v().get(6))
        self.assertIsNone(self.graph.get_all_v()[6].get_location())
        self.assertIsNone(self.graph.get_all_v().get(7))
        self.graph.add_node(7,(7,7,7))
        self.assertIsNotNone(self.graph.get_all_v().get(7))
        self.assertEqual((7,7,7),self.graph.get_all_v()[7].get_location())
        self.assertFalse(self.graph.add_node(7))

    def test_remove_node(self):
        self.assertIsNotNone(self.graph.get_all_v()[1])
        self.assertIsNotNone(self.graph.all_out_edges_of_node(1).get(2))
        self.assertIsNotNone(self.graph.all_in_edges_of_node(2).get(1))
        self.graph.remove_node(1)
        self.assertIsNone(self.graph.get_all_v().get(1))
        self.assertIsNone(self.graph.all_in_edges_of_node(2).get(1))

    def test_remove_edge(self):
        self.assertIsNotNone(self.graph.all_out_edges_of_node(1).get(2))
        self.assertIsNotNone(self.graph.all_in_edges_of_node(2).get(1))
        self.graph.remove_edge(1,2)
        self.assertIsNone(self.graph.all_out_edges_of_node(1).get(2))
        self.assertIsNone(self.graph.all_in_edges_of_node(2).get(1))
        self.assertIsNotNone(self.graph.all_out_edges_of_node(2).get(3))
        self.assertIsNotNone(self.graph.all_in_edges_of_node(3).get(2))
        self.graph.remove_edge(2,3)
        self.assertIsNone(self.graph.all_out_edges_of_node(2).get(3))
        self.assertIsNone(self.graph.all_in_edges_of_node(3).get(2))
        self.assertIsNone(self.graph.all_out_edges_of_node(1).get(3))
        self.assertFalse(self.graph.remove_edge(1,3))

