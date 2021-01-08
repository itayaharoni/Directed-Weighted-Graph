import json
from json.encoder import JSONEncoder


class NodeData:
    """This class represents an implementation of a vertex in a directed weighted graph."""

    def __init__(self, key: int = 0, weight: float = -1, location: tuple = None, info: str = "", tag: int = -1):
        """A constructor for the class.
        @:param key - int unique to each vertex
        @:param weight - float the weight of the vertex
        @:param location - a tuple represents a 3D Point
        @:param info - a str meta-data of the vertex
        @:param tag - an int variable used for algorithms"""
        self._key = key
        self._weight = weight
        self._location = location
        self._info = info
        self._tag = tag

    def set_key(self, key: int):
        """"This method changes the key of the node
        @:param key int unique to the node """
        self._key = key

    def set_weight(self, weight: float):
        """"This method changes the weight of the node
        @:param weight - float """
        self._weight = weight

    def set_location(self, location: tuple):
        """"This method changes the location of the node
        @:param location - tuple representing the pos of a node as a 3D Point """
        self._location = location

    def set_info(self, info: str):
        """"This method changes the info of the node
        @:param info - str which represents the meta-data of the node """
        self._info = info

    def set_tag(self, tag: int):
        """"This method changes the tag of the node
        @:param tag - int variable used in complicated algorithms """
        self._tag = tag

    def get_weight(self) -> float:
        """"This method returns the weight of the node
        @:return weight - float """
        return self._weight

    def get_location(self) -> tuple:
        """"This method returns the location of the node
        @:return location - tuple """
        return self._location

    def get_info(self) -> str:
        """"This method returns the info of the node
        @:return info - str """
        return self._info

    def get_tag(self) -> int:
        """"This method returns the tag of the node
        @:return tag - int """
        return self._tag

    def get_key(self) -> int:
        """"This method returns the key of the node
        @:return key - int """
        return self._key

    def __str__(self) -> str:
        """"This method returns a string representing this node
        @:return str - representing this node """
        return json.dumps(self, indent=4, cls=self.NodeDataEncoder)

    def __repr__(self)->str:
        """"This method returns a string representing this node
        @:return str - representing this node """
        return "NodeData: " + self.__str__()

    def __eq__(self, other)->bool:
        """This method returns True iff the other node equals this node.
        @:return True iff (if and only if) this node equals other node"""
        key_flag = other.get_key() == self._key
        weight_flag = other.get_weight() == self._weight
        info_flag= other.get_info() == self._info
        location_flag= other.get_location() == self._location
        tag_flag=other.get_tag() == self._tag
        return key_flag and weight_flag and info_flag and location_flag

    class NodeDataEncoder(JSONEncoder):
        """ This class is a class of simple json Encoder to the NodeData class"""
        def default(self, o) -> dict:
            """This method returns the dictionary of an object.
            @:return the dicionary of the object o"""
            return o.__dict__

