import sys
import random

class Graph(object):
    """
    A class used to create the De Bruijn graph

    Attributes
    ----------
    dict : dictionary
        a dictionary containing all the unique edges and the information of
        vertices
    vert_num : integer
        an integer storing the number of vertices
    edge_num : integer
        an integer storing the number of unique edges

    Methods
    -------
    add_vert(info)
        creates a new instance of the Vertex class
        adds the information of a new vertex to the dictionary as new_vert
        increases the count of vertices by one
    get_vertex(vert)
        checks if the vertex being requested has been put in the dictionary
        if it is in the dictionary, it's information is returned
    add_edge(prev, next)
        checks to see if the edge attempting to be added already exists, if it
        does then update_connection() is called
        if it hasn't been added, then it increases the count of unique edges by
        1 then calls add_connection()
    get_vertices()
        returns all the keys of the dictionary
    """

    def __init__(self):
        self.dict = {}
        self.vert_num = 0
        self.edge_num = 0

    def add_vert(self,info):
        """
        Creates a new instance of the Vertex class then adds the information of
        a new vertex to the dictionary as new_vert and increases the count of
        vertices by one

        Parameters
        ---------
        info : str
            the information that will be stored with the new vertex

        Returns
        -------
        new_vert : Vertex object
            the new vertex object with the stored information
        """
        self.vert_num = self.vert_num + 1
        new_vert = Vertex(info)
        self.dict[info] = new_vert

        return new_vert

    def get_vertex(self, vert):
        """
        Using a Vertex object, returns the information stored in the dict
        dictionary with that Vertex object

        Parameters
        ---------
        vert : Vertex object
            the vertex object that the information being returned belongs to

        Returns
        -------
        self.dict[vert] : str
            the information stored in dict for that Vertex object
        """

        if vert in self.dict:
            return self.dict[vert]
        else:
            return None

    def add_edge(self, prev, next):
        """
        Using the previous vertex and next vertex, either creates or updates a
        connection between two vertices

        Parameters
        ---------
        prev : Vertex object
            The vertex on one side of the edge
        next : Vertex object
            The vertex on the other side of the edge
        """

        if self.dict[prev].get_connection(self.dict[next]):
            self.dict[prev].update_connection(self.dict[next])
        else:
            self.edge_num = self.edge_num + 1
            self.dict[prev].add_connection(self.dict[next])

    def get_vertices(self):
        """
        returns all the keys of the dictionary

        Returns
        ---------
        self.dict.keys() : list
            All keys in the dict dictionary
        """

        return self.dict.keys()


class Vertex:
    """
    A class used to create the vertices in the De Bruijn graph

    Attributes
    ----------
    data : str
        the information stored with the vertex object
    connections : dictionary
        a dictionary containing all the connections

    Methods
    -------
    add_connection(end)
        add a new connection from self to end with a weight of one
    get_connection(end)
        returns True if there is an existing connection from self to end
    update_connection(end)
        increases the weight of the edge from self to end by one
    """

    def __init__(self,storedData):
        """
        Parameters
        ---------
        storedData : str
            the information stored with the vertex object
        """

        self.data = storedData
        self.connections = {}

    def add_connection(self, end):
        """
        Adds a new connection from self to end with a weight of one

        Parameters
        ---------
        end : Vertex object
            The vertex on the other side of the edge
        """

        self.connections[end] = 1

    def get_connection(self, end):
        """
        Returns True if there is an existing connection from self to end

        Parameters
        ---------
        end : Vertex object
            The vertex on the other side of the edge
        """

        return (end in self.connections.keys())

    def update_connection(self, end):
        """
        Increases the weight of the edge from self to end by one

        Parameters
        ---------
        end : Vertex object
            The vertex on the other side of the edge
        """

        self.connections[end] = self.connections[end] + 1

def dotGraph(dbgraph):
    """
    Using a Graph object, create a .dot file and transcribe the De Bruijn graph
    into proper DOT language syntax such that a dot graph can be created to
    visualize the data

    Parameters
    ---------
    dbgraph : Graph object
        De Bruijn graph
    """

    DOTfile = open("DOT.dot","w+")
    DOTfile.write("digraph mygraph{\n")

    for vertex in dbgraph.get_vertices():
        for edge in (dbgraph.dict[vertex].connections).keys():

            DOTfile.write("\t\"")
            DOTfile.write(str(dbgraph.dict[vertex].data))
            DOTfile.write("\"->\"")
            DOTfile.write(str(edge.data))
            DOTfile.write("\"\n")

    DOTfile.write("}")

def main():
    readsFileName = sys.argv[1]
    k = int(sys.argv[2])
    readsFile = open(readsFileName,"r")
    kmers = []
    dbgraph = Graph()

    #create list of kmers
    for line in readsFile:
        for i in range((len(line)-k)):
            kmers.append(line[i:i+k])

    #create all vertices
    for i in range(len(kmers)):
        if kmers[i][0:k-1] not in dbgraph.get_vertices():
            dbgraph.add_vert(kmers[i][0:k-1])
        if kmers[i][1:k] not in dbgraph.get_vertices():
            dbgraph.add_vert(kmers[i][1:k])

    #add all edges
    for i in range(len(kmers)):
        #add edge kmers[i][0:k-1] to kmers[j][1:k]
        dbgraph.add_edge(kmers[i][0:k-1],kmers[i][1:k])

    #prints number of vertices in the graph
    print(dbgraph.vert_num)
    #prints number of unique edges in the graph
    print(dbgraph.edge_num)

    if dbgraph.vert_num <= 30:
        dotGraph(dbgraph)
    else:
        print("Can't create dotgraph, too many vertices")

if __name__ == "__main__":
    main()
