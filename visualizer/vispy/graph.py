##
## Authors: Kim Lundsteen Juncher and Brian Soborg Mathiasen
## Insitute of Computer Science, Copenhagen University, Denmark
##
##
##
## graph.py
##
## LICENSED UNDER: GNU General Public License v2
##

import random as r
import matplotlib.pyplot as plt
import networkx as nx
import datastructure as abstract

class Graph(abstract.GraphDatastructure):
    def __init__ (self, visual=False):
        self.vertices = {}
        self.edges = {}
        self._lastaddedvertex = -1
        self._lastaddededge = -1
        self._edgeidcount = 0
#        self._vertexidcount = 0
        #needed for internal networkX representation
        self._visualisation = visual
        plt.ion()
        self._g = nx.Graph()
        self._oldgvertices = []
        self._oldgedges = []
        self._pos = {}

    def addVertex(self, vertex_id):
        self.vertices[vertex_id] = Vertex(vertex_id)

    def addEdge(self, (vertex_id_1, vertex_id_2), weight=0): 
        if not self.vertexExists(vertex_id_1): self.addVertex(self, vertex_id_1)
        if not self.vertexExists(vertex_id_2): self.addVertex(self, vertex_id_2)
        edge_id = self._edgeidcount
        self._edgeidcount += 1
        self.edges[(vertex_id_1, vertex_id_2)] = Edge(edge_id, (vertex_id_1,\
                                                         vertex_id_2), weight)

    def removeVertex(self, vertex_id):
        if vertex_id in self.vertices:
            del self.vertices[vertex_id]
            self.removeEdges(self.getAdjEdges(vertex_id))

    def vertexExists(self, vertex_id):
        return vertex_id in self.vertices

    def edgeExists(self, (vertex_id_1, vertex_id_2)):
        return (vertex_id_1, vertex_id_2) in self.edges
    
    def removeEdge(self, (vertex_id_1, vertex_id_2)):
        if self.edgeExists((vertex_id_1, vertex_id_2)):
            del self.edges[(vertex_id_1, vertex_id_2)]

    def removeEdges(self, edge_list):
        for edge in edge_list:
            self.removeEdge(edge)

    def getVertices(self):
        ''' Function to return the vertex objects, as an iterator
        '''
        return [self.getVertex(vertex) for vertex in self.vertices].__iter__()
    
    def getEdges(self): 
        return [self.getEdge(edge) for edge in self.edges].__iter__()
    
    def degreeList(self): 
        return
    
    def getAdjEdges(self, vertex_id):
        return [(edge.start_vertex, edge.end_vertex) for edge in self.edges if self.getEdge(edge).start_vertex == vertex_id or self.getEdge(edge).end_vertex == vertex_id]

    def getAdjVertices(self, vertex_id):
        # this function needs rewriting
        buf = []
        for edge in self.getAdjEdges(self, vertex_id):
            if edge.start_vertex == vertex_id:
                buf.append(edge.end_vertex)
            elif edge.end_vertex == vertex_id:
                buf.append(edge.start_vertex)
        return buf
    
    def getVertex(self, vertex_id): 
        if self.vertexExists(vertex_id):
            return self.vertices[vertex_id]
            
    def getEdge(self, (vert_id_1, vert_id_2)):
        if self.edgeExists((vert_id_1, vert_id_2)):
            return self.edges[(vert_id_1, vert_id_2)]
    
    def visualise(self, figNum=1, markEdges=[], markVertices=[], savefig=None,
        savefig_format='png', vertexLabels=None):
        plt.figure(figNum, facecolor='white')
        plt.clf()
        plt.axis('off')
        self._g.clear()
        for vertex in self.vertices:
            self._g.add_node(self.getVertex(vertex).getId())

        for edge in self.edges:
            self._g.add_edge(self.getEdge(edge).start_vertex,self.getEdge(edge).end_vertex)
            
        if (not self._oldgvertices and not self._oldgedges) or \
            (not self._oldgvertices == self._g.nodes() or \
             not self._oldgedges == self._g.edges()):
            self._pos = nx.spring_layout(self._g)

        self._oldgvertices = self._g.nodes()
        self._oldgedges = self._g.edges()

        if not markVertices and not markEdges:
            nx.draw_networkx_nodes(self._g, self._pos, node_color='#557A66')#, edge_color='#272E2E')
            nx.draw_networkx_edges(self._g, self._pos)#, edge_color='#272E2E')
            nx.draw_networkx_labels(self._g, self._pos, labels=vertexLabels)
#            nx.draw_networkx_edge_labels(self.G, self._pos, edge_labels=vertexLabels)
# drawing edge labels are only available from networkX 1.1 and beyond
        else:
            unmarkedVertices = list(set(self._g.nodes()).difference(markVertices))
            unmarkedEdges = list(set(self._g.edges()).difference(markEdges))

            nx.draw_networkx_nodes(self._g, self._pos, nodelist=unmarkedVertices, node_color='#557A66')#, vertex_size=700)
            nx.draw_networkx_nodes(self._g, self._pos, nodelist=markVertices, node_size=700, node_color='#9ed95e')
            # E82B1E <- roed sort trae
            nx.draw_networkx_edges(self._g, self._pos, edgelist=unmarkedEdges)#, edge_color='#272E2E')#, width=6)
            nx.draw_networkx_edges(self._g, self._pos, edgelist=markEdges,width=6)#, edge_color='#272E2E')

            nx.draw_networkx_labels(self._g, self._pos, labels=vertexLabels)

        if savefig:
            plt.savefig(savefig, format=savefig_format)

    def clearVisualisation(self):
        self._pos = {}
        plt.close()
        
    def generateRandomGraph(self, numberofvertices=0, numberofedges=0):
        if numberofvertices == 0:
            numberofvertices = r.randint(5,10)
        self.clear()
        vertexId = 0
        self.addVertex(vertexId)
        for i in range(1,numberofvertices):
            neighbor = r.randint(0,len(self.vertices)-1)
            vertexId += 1
            self.addVertex(i)
            self.addEdge((i, neighbor))
        if numberofedges:
            for i in range(0,numberofedges):
                added = False
                while not added:
                    neighbour1 = r.randint(0,len(self.vertices)-1)
                    neighbour2 = r.randint(0,len(self.vertices)-1)
                    if not self.edgeExists((neighbour1, neighbour2)):
                        self.addEdge((neighbour1, neighbour2))
                        added = True

    def clear(self): 
        self.vertices = {}
        self.edges = {}
        self._lastaddedvertex = -1
        self._lastaddededge = -1
        self._edgeidcount = 0
        self._g = nx.Graph()
        self._oldgvertices = []
        self._oldgedges = []
        self._pos = {}



class Vertex:
    def __init__(self, vertex_id, label=None):
        self._id = vertex_id
        self.label = label
        
    def getId(self):
        return self._id
        
    def getLabel(self):
        if not self.label:
            return self.getId()
        return self.label
    
class Edge:
    def __init__(self, edge_id, (start_vertex_id, end_vertex_id), weight):
        self._id = edge_id
        self.weight = weight
        self.start_vertex = start_vertex_id
        self.end_vertex = end_vertex_id
            
    def getId(self):
        return self._id
    def getWeight(self):
        return self.weight
    
    
