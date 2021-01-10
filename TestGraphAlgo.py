from unittest import TestCase

from DiGraph import DiGraph
from GraphAlgo import GraphAlgo


class Test(TestCase):

    def setUp(self) -> None:
        self.graph = DiGraph()
        self.graph_algo = GraphAlgo(self.graph)
        self.graph.add_node(1, (1, 1, 1))
        self.graph.add_node(2, (2, 2, 2))
        self.graph.add_node(3, (3, 3, 3))
        self.graph.add_node(4, (4, 4, 4))
        self.graph.add_node(5, (5, 5, 5))
        for i in range(4):
            self.graph.add_edge(i + 1, i + 2, i + 1)

    def test_get_graph(self):
        self.assertEqual(self.graph_algo.get_graph(), self.graph)
        test_graph = DiGraph()
        test_graph_algo = GraphAlgo(test_graph)
        self.assertEqual(test_graph, test_graph_algo.get_graph())

    def test_save_and_load_from_json(self):
        self.graph_algo.save_to_json("load_test_file.json")
        original_graph = self.graph_algo.get_graph()
        self.graph_algo = GraphAlgo()
        self.assertTrue(self.graph_algo.load_from_json("load_test_file.json"))
        self.assertEqual(self.graph_algo.get_graph(), original_graph)

    def test_shortest_path(self):
        test_tuple_1 = (10, [1, 2, 3, 4, 5])
        self.assertEqual(test_tuple_1, self.graph_algo.shortest_path(1, 5))
        test_tuple_2 = (float('inf'), [])
        self.assertEqual(test_tuple_2, self.graph_algo.shortest_path(5, 1))
        self.graph.add_edge(5, 1, 20)
        test_tuple_3 = (20, [5, 1])
        self.assertEqual(test_tuple_3, self.graph_algo.shortest_path(5, 1))

    def test_connected_component(self):
        self.assertEqual([1], self.graph_algo.connected_component(1))
        self.assertEqual([2], self.graph_algo.connected_component(2))
        self.graph_algo.get_graph().add_edge(2, 1, 2)
        self.assertEqual([1, 2], self.graph_algo.connected_component(1))
        self.assertEqual([2, 1], self.graph_algo.connected_component(2))
        self.graph_algo.get_graph().add_edge(5, 1, 1)
        self.assertEqual([1, 2, 3, 4, 5], self.graph_algo.connected_component(1))

    def test_connected_components(self):
        self.assertEqual([[1], [2], [3], [4], [5]], self.graph_algo.connected_components())
        self.graph_algo.get_graph().add_edge(5, 1, 1)
        self.assertEqual([[1, 2, 3, 4, 5]], self.graph_algo.connected_components())
        self.graph_algo.get_graph().remove_edge(1, 2)
        self.graph_algo.get_graph().add_edge(5, 2, 2)
        self.assertEqual([[1], [2, 3, 4, 5]], self.graph_algo.connected_components())

    def test_graph_width(self):
        self.assertEqual([1, 5], self.graph_algo.graph_height(self.graph.get_all_v()))

    def test_graph_height(self):
        self.assertEqual([1, 5], self.graph_algo.graph_height(self.graph.get_all_v()))

    def test_plot_graph(self):
        self.graph_algo.plot_graph()
