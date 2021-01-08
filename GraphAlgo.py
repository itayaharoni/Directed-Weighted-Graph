import json
import matplotlib.pyplot as plt
from typing import List
from DiGraph import DiGraph as dg
from GraphAlgoInterface import GraphAlgoInterface as ga
from GraphInterface import GraphInterface as gi
from NodeData import NodeData as nd
import numpy as np

class PriorityQueue(nd):
    """This class is an implementation of a PriorityQueue for the NodeData class."""

    def __init__(self):
        """"A simple constructor for the class"""
        self._queue = []

    def insert(self, item: nd):
        """This method receives a NodeData and inserts it to the PriorityQueue.
        @:param item - NodeData"""
        self._queue.append(item)

    def is_empty(self) -> bool:
        """This method returns True iff the PriorityQueue is empty.
        @:return True - iff (if and only if) the PriorityQueue is empty"""
        return len(self._queue) == 0

    def delete(self) -> nd:
        """This method delete the NodeData with the smallest weight value in the PriorityQueue,
        and returns the NodeData.
        @:return NodeData - with the smallest weight value"""
        try:
            min_index = 0
            for i in range(len(self._queue)):
                if self._queue[i].get_weight() < self._queue[min_index].get_weight():
                    min_index = i
            item = self._queue[min_index]
            del self._queue[min_index]
            return item
        except IndexError as e:
            print(e)
            exit()


class GraphAlgo(ga):
    """This abstract class represents an implementation of a some complicated algorithms performed on a
    directed weighted graph, such as:
    1) short_path
    2) connected_components
    3)graph_plot"""

    def __init__(self,graph:dg=None):
        """A constructor for the class, receives a DiGraph and initializes this graph.
        @:param graph - DiGraph"""
        self._graph = graph

    def get_graph(self) -> gi:
        """This method returns the underlying graph of this class.
        @:return graph - DiGarph, the graph of this class"""
        return self._graph

    def load_from_json(self, file_name: str) -> bool:
        """This method receives a str representing a path to a JSON file and loads the  JSON object
        to this graph
        @:param file_name - a str representing a path to a JSON file
        @:return True iff the graph was loaded successfully"""
        new_graph = dg()
        try:
            with open(file_name, "r") as f:
                new_dict = json.load(f)
                for i in new_dict["Nodes"]:
                    key = -1
                    pos = None
                    for k, v in i.items():
                        if k == "pos":
                            pos = v
                        elif k=="id":
                            key = v
                    if pos is not None:
                        tup_from_string = tuple(pos.split(","))
                        new_tuple=(float(tup_from_string[0]),float(tup_from_string[1]),float(tup_from_string[2]))
                        new_graph.add_node(key,new_tuple)
                        pos=None
                    else:
                        new_graph.add_node(key,None)
                for i in new_dict["Edges"]:
                    src = -1
                    weight = -1
                    dest = -1
                    for k, v in i.items():
                        if k == "src":
                            src = v
                        elif k == "dest":
                            dest = v
                        else:
                            weight = v
                    new_graph.add_edge(src, dest, weight)
            self._graph = new_graph
            return True
        except Exception as e:
            print(e)
            return False

    def save_to_json(self, file_name: str) -> bool:
        """This method receives a str representing a path to save a file and saves the underlying
        graph of this graph as a JSON object.
        @:param file_name - str representing a path
        @:return True iff the graph was saved successfully"""
        if self._graph is None:
            return False
        Nodes=[]
        Edges=[]
        for node in self._graph.get_all_v().values():
            if node.get_location() is not None:
                Nodes.append({"pos":""+str(node.get_location()[0])+","+str(node.get_location()[1])+","+str(node.get_location()[2]),"id":node.get_key()})
            else:
                Nodes.append({"id":node.get_key()})
            for dest,edges in self._graph.all_out_edges_of_node(node.get_key()).items():
                Edges.append({"src":node.get_key(),"w":edges,"dest":dest})
        graph_to_json={"Edges":Edges,"Nodes":Nodes}
        try:
            with open(file_name,"w") as f:
                json.dump(graph_to_json,default=lambda o:o.__dict__,indent=4,fp=f)
                return True
        except Exception as e:
            return False


    def shortest_path(self, id1: int, id2: int)-> (float, list):
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @:param id1 - The start node id
        @:param id2 - The end node id
        @:return The distance of the path, a list of the nodes ids that the path goes through
        """
        if self._graph is None:
            return float('inf'), []
        all_nodes=self._graph.get_all_v()
        if all_nodes.get(id1) is None or all_nodes.get(id1) is None:
            return float('inf'), []
        if id1 == id2:
            return 0,[]
        for k,v in all_nodes.items():
            v.set_weight(float('inf'));
        first_node=all_nodes[id1]
        first_node.set_weight(0)
        queue=PriorityQueue()
        queue.insert(first_node)
        while not queue.is_empty():
            first_node=queue.delete()
            for dest,weight in self._graph.all_out_edges_of_node(first_node.get_key()).items():
                if all_nodes[dest].get_weight()> first_node.get_weight()+weight:
                    all_nodes[dest].set_weight(first_node.get_weight()+weight)
                    queue.insert(all_nodes[dest])
        dest_node=all_nodes[id2]
        dist = dest_node.get_weight()
        if dist == float('inf'):
            return float('inf'), []
        path= [dest_node.get_key()]
        while dest_node.get_weight() != 0:
            edges_into_node=self._graph.all_in_edges_of_node(dest_node.get_key())
            for k,v in edges_into_node.items():
                if dest_node.get_weight() == all_nodes[k].get_weight()+v:
                    dest_node=all_nodes[k]
                    path.insert(0,dest_node.get_key())
                    break
        return dist,path

    def connected_component(self, id1: int)-> list:
        """
        Finds the Strongly Connected Component(SCC) that node id1 is a part of in this graph.
        @:param id1 - The node id
        @:return The list of nodes in the SCC
        """
        if self._graph is None:
            return []
        all_nodes=self._graph.get_all_v()
        for node in all_nodes.values():
            node.set_tag(-1)
            node.set_weight(-1)
        component_out=[all_nodes[id1]]
        while len(component_out) != 0:
            first_node=component_out.pop(0)
            for dest,weight in self._graph.all_out_edges_of_node(first_node.get_key()).items():
                if all_nodes[dest].get_tag() == -1:
                    all_nodes[dest].set_tag(0)
                    component_out.append(all_nodes[dest])
        component_in=[all_nodes[id1]]
        while len(component_in) != 0:
            first_node=component_in.pop(0)
            for dest,weight in self._graph.all_in_edges_of_node(first_node.get_key()).items():
                if all_nodes[dest].get_weight() == -1:
                    all_nodes[dest].set_weight(0)
                    component_in.append(all_nodes[dest])
        component_list=[all_nodes[id1].get_key()]
        for j in all_nodes.values():
            if j.get_tag() == 0 and j.get_weight()==0 and j.get_key() != id1:
                component_list.append(j.get_key())
        return component_list

    def connected_components(self)-> list:
        """
        Finds all the Strongly Connected Component(SCC) in this graph.
        @return: The list all SCC
        """
        if self._graph is None:
            return []
        all_nodes=self._graph.get_all_v()
        all_componentes=[]
        keys_list= list(all_nodes.keys())
        index=0
        while len(keys_list) != 0:
            rand_key = keys_list.pop(0)
            all_componentes.append(self.connected_component(rand_key))
            for j in all_componentes[index]:
                for k in keys_list:
                    if k == j:
                        keys_list.remove(k)
            index+=1
        return all_componentes

    def graph_width(self,v_dict:dict):
        """"This method returns a list containing the smallest x value of a node in the graph
        and the highest x value of a node in this graph.
        @:return list - containing the highest and lowest x value of the nodes in this graph"""
        min_val=float('inf')
        max_val=-1
        for k,v in v_dict.items():
            if v.get_location() is not None:
                v2=v.get_location()[0]
                if v2 < min_val:
                    min_val=v2
                elif v2 > max_val:
                    max_val=v2
        width=[min_val,max_val]
        return width

    def graph_height(self,v_dict:dict):
        """"This method returns a list containing the smallest y value of a node in the graph
        and the highest y value of a node in this graph.
        @:return list - containing the highest and lowest y value of the nodes in this graph"""
        min_val=float('inf')
        max_val=-1
        for k,v in v_dict.items():
            if v.get_location() is not None:
                v2=v.get_location()[1]
                if v2 < min_val:
                    min_val=v2
                elif v2 > max_val:
                    max_val=v2
        height=[min_val,max_val]
        return height

    def plot_graph(self):
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        """
        fig,ax=plt.subplots()
        all_nodes=self._graph.get_all_v()
        x_axis=[]
        y_axis=[]
        keys=[]
        edges_by_src={}
        width_range=self.graph_width(all_nodes)
        if width_range[0] == float('inf'):
            width_range=[0,100]
        height_range=self.graph_height(all_nodes)
        if height_range[0] == float('inf'):
            height_range=[0,100]
        width=width_range[1]-width_range[0]
        height=height_range[1]-height_range[0]
        for node in all_nodes.values():
            if node.get_location() is None:
                node.set_location((width_range[0]+width*np.random.uniform(low=0.01,high=0.1,size=1),height_range[0]+height*np.random.uniform(low=0.01,high=0.1,size=1),0))
        for key,node in all_nodes.items():
            x_val=node.get_location()[0]/width
            y_val=node.get_location()[1]/height
            x_axis.append(x_val)
            y_axis.append(y_val)
            keys.append(key)
            ax.scatter(x_val,y_val,color='blue',zorder=2)
           # ax.annotate(key,(x_val,y_val))
            ax.text(x_val+1*0.0001/width,y_val+0.15*0.0001/height,s=str(key),zorder=3)
            for dest,weight in self._graph.all_out_edges_of_node(key).items():
                x_val_dest=all_nodes[dest].get_location()[0]/width
                y_val_dest=all_nodes[dest].get_location()[1]/height
                edges_by_src[key]= [[x_val,y_val],[x_val_dest,y_val_dest]]
                ax.plot([x_val,x_val_dest],[y_val,y_val_dest],color='red',zorder=1)
        plt.axis('off')
        plt.show()


