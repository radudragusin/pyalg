##
## Authors: Kim Lundsteen Juncher and Brian Soborg Mathiasen
## Insitute of Computer Science, Copenhagen University, Denmark
##
## Date: 22-05-2010
##
## datastructure.py
##
## LICENSED UNDER: GNU General Public License v2
##


from abstract import abstract

class GraphDatastructure():

    def addVertex(self, vertex_id): abstract()
    
    def addEdge(self, (vertex_id_1, vertex_id_2), weight=0): abstract()

    def vertexExists(self, node_id): abstract()

    def edgeExists(self, edge_id): abstract()
    
    def removeEdge(self, (node_id_1, node_id_2), edge_id=None): abstract()

    def removeEdges(self, edge_list): abstract()

    def getVertices(self): abstract()
    
    def getEdges(self):  abstract()
    
#    def degreeList(self):  abstract()
    
    def getAdjEdges(self, node_id): abstract()

    def getAdjVertices(self, node_id): abstract()
        
    def getVertex(self, node_id):  abstract()
    
    # the following functions are following a strict naming scheme across
    # our datastructures
    def visualise(self, figNum=1, markEdges=[], markNodes=[], savefig=None,
        savefig_format='png', vertexLabels=None): abstract()

    def clearVisualisation(self): abstract()
        
    def generateRandomGraph(self, n): abstract()
        
    def clear(self):  abstract()

