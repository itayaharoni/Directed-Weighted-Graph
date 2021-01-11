import json
from GraphInterface import GraphInterface as gi
from NodeData import NodeData as nd


class DiGraph(gi):
    """This class represents an implementation of a directed weighted graph."""

    def __init__(self):
        """A constructor for the class."""
        self._nodes = {}
        self._edges_in = {}
        self._edges_out = {}
        self._mc = 0
        self._edge_size = 0

    def v_size(self) -> int:
        """
        A method that returns the number of vertices in this graph
        @:return: The number of vertices in this graph
        """
        return len(self._nodes)

    def e_size(self) -> int:
        """
        A method that returns the number of edges in this graph
        @:return The number of edges in this graph
        """
        return self._edge_size

    def get_all_v(self) -> dict:
        """This method returns a dictionary of all the nodes in the Graph, each node is
        represented using a pair (node_id, node_data)
         @return A dictionary representing the nodes in the graph
        """
        return self._nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        """This method returns a dictionary of all the nodes connected to (into) node_id ,
        each node is represented using a pair (other_node_id, weight)
        @:return a dictionary of all the edges connected into node_id
         """
        if self._nodes.get(id1) is None:
            temp = {}
            return temp
        return self._edges_in[id1]

    def all_out_edges_of_node(self, id1: int) -> dict:
        """This method returns a dictionary of all the nodes connected from (out of) node_id ,
        each node is represented using a pair (other_node_id, weight)
        @:return a dictionary of all the edges connected out of node_id
         """
        if self._nodes.get(id1) is None:
            temp = {}
            return temp
        return self._edges_out[id1]

    def get_mc(self) -> int:
        """
        This method returns the current version of this graph,
        on every change in the graph state - the MC should be increased
        @:return The current version of this graph.
        """
        return self._mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        This method adds an edge to the graph.
        @:param id1 - The start node of the edge
        @:param id2 - The end node of the edge
        @:param weight - The weight of the edge
        @:return True if the edge was added successfully, False o.w.
        """
        if id1 == id2:
            return False
        if weight > 0:
            if self._nodes.get(id1) is None or self._nodes.get(id2) is None:
                return False
            if self._edges_out.get(id1).get(id2) is not None:
                return False
            else:
                self._edges_out[id1][id2] = weight
                self._edges_in[id2][id1] = weight
                self._mc += 1
                self._edge_size += 1
                return True
        else:
            return False

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
        This method adds a node to the graph.
        @:param node_id - The node ID
        @:param pos - The position of the node
        @:return True if the node was added successfully, False o.w.
        """
        if self._nodes.get(node_id) is None:
            self._nodes[node_id] = nd(node_id, location=pos)
            self._edges_out[node_id] = {}
            self._edges_in[node_id] = {}
            self._mc += 1
            return True
        return False

    def remove_node(self, node_id: int) -> bool:
        """
        This method removes a node from the graph.
        Removing all the edges the node_id is part of as well.
        @:param node_id - The node ID
        @:return True if the node was removed successfully, False o.w.
        """
        if self._nodes.get(node_id) is not None:
            if self._edges_out.get(node_id) is not None:
                keys_out = list(self._edges_out[node_id].keys())
                for k in keys_out:
                    self.remove_edge(node_id, k)
                self._edges_out.pop(node_id)
            if self._edges_in.get(node_id) is not None:
                keys_in = list(self._edges_in[node_id].keys())
                for k in keys_in:
                    self.remove_edge(k, node_id)
                self._edges_in.pop(node_id)
                self._nodes.pop(node_id)
                self._mc += 1
            return True
        else:
            return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        This method removes an edge from the graph.
        @:param node_id1 - The start node of the edge
        @:param node_id2 - The end node of the edge
        @:return True if the edge was removed successfully, False o.w.
        """
        if self._nodes.get(node_id1) is None or self._nodes.get(node_id2) is None:
            return False
        if self._edges_out[node_id1].get(node_id2) is None:
            return False
        else:
            self._edges_out[node_id1].pop(node_id2)
            self._edges_in[node_id2].pop(node_id1)
            self._mc += 1
            self._edge_size -= 1
            return True

    def __str__(self) -> str:
        """ This method returns a string representing this graph.
        @:return a str representing this graph"""
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def __repr__(self) -> str:
        """ This method returns a string representing this graph.
        @:return a str representing this graph"""
        return "DiGraph: " + self.__str__()

    def __eq__(self, other) -> bool:
        """This method returns True iff the other graph equals this graph.
        @:param other - another instance of DiGraph
        @:return True iff (if and only if) this graph equals other graph"""
        if not isinstance(other, self.__class__):
            return False
        other_nodes = other.get_all_v()
        other_edge_size = other.e_size()
        if other_edge_size != self._edge_size:
            return False
        if len(other_nodes) != len(self._nodes):
            return False
        for k, v in self._nodes.items():
            if other_nodes.get(k) is None:
                return False
            elif other_nodes[k] != self._nodes[k]:
                return False
            else:
                for dest, weight in self._edges_out[k].items():
                    if other.all_out_edges_of_node(k).get(dest) is None:
                        return False
                    elif other.all_out_edges_of_node(k)[dest] != weight:
                        return False
        return True

