# Directed Weighted Grapg Implementation
This repository exihibits an implementation of a directed weighted graph and some complicated algorithms implemnted on the said graph, the repo is in python.
There are a total of 3 main classes: 
1) NodeData - an implementation of a vertex in a directed weighted graph.
2) DiGraph - an implementation of a directed weighted graph, using the NodeData class as it's vertices of the graph.
3) GraphAlgo - a class that implements complicated algorithms on a directed weighted graph (DiGraph object), such as: short path, finds connectivity components and more.

Two Interfaces:
1) GraphInterface - an interface for a directed weighted graph and simple methods applicable on it.
2) GraphAlgoInterface - an interface for complicated algorithms applicable on a directed weighted graph.

Two tests classes:
1) TestDiGraph - a simple test class for the methods of the class DiGraph.
2)TestGraphAlgo - a test for all of the methods of the algorithms class GraphAlgo.
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Table of contents

1) NodeData  

2) DiGraph

3) GraphAlgo
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
### NodeData class - implements a vertex in directed weighted graph (used in the DiGraph class)
This class represents a single vertex in a weighted directed graph and the set of methods applicable on it. Each vertex has a unique integer key 
that differentiate it from other vertices. Also, each vertex contains a string to meta-data, 3D point object that represents it's location, a tag
object which is used in more advanced algorithms and weight.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


### DiGraph class - inherited from the GraphInterface
This class represents a directed weighted graph, this class uses the NodeData class to construct a graph. The methods applicable on the graph
are quite simple, such as: adding vertices, connecting two vertices by an edge, removing edge or a vertex and retrieving the graph vertices or a specific vertex 
group of edges, and few more simple methods which are discussed in length in the wike page.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### GraphAlgo - inherited from the GraphAlgoInterface
This class contains a few more complicated algorithms applicable on a directed weighted graph (the DiGraph class), here are some methods:
- shortPath/shortPathDist - receives a source vertex and a destination vertex, iterates through the graph and retrieves the shortest path/distance between
the said vertices.
- connected_component-  returns the a list of all the SCC (strong connectivity component) of a the received node ID. 
- connected_components - returns a list of lists, each list represents a SCC in the graph, in case the graph is strongly connected it returns a list of 1 list - The graph.
- plot_graph - Draws the graph using the matplot library.

Here's is a small taste of what you can do with this repo:
![‏‏plot](https://user-images.githubusercontent.com/74153075/104137440-51156d00-53a5-11eb-8832-c466e50b8d2b.PNG)

In case you are intersted in more detailed information about the project, and the implementation of the mentioned above method you can enter our wiki page.
You can always contact us for more information or updates through our github profile, we hope this page was helpful to you!
