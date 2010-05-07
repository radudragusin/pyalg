from abstract import abstract

class GraphDatastructure():

    def nodeExists(self, node_id): abstract()

    def edgeExists(self, edge_id): abstract()
    
    def removeEdge(self, (node_id_1, node_id_2), edge_id=None): abstract()

    def removeEdges(self, edge_list): abstract()

    def getNodes(self): abstract()
    
    def getEdges(self):  abstract()
    
    def degreeList(self):  abstract()
    
    def getAdjEdges(self, node_id): abstract()

    def getAdjNodes(self, node_id): abstract()
        
    def isEdge(self, (node_id_1, node_id_2)): abstract()
    
    def getNode(self, node_id):  abstract()
    
    def __str__(self): abstract()

    # the following functions are following a strict naming scheme across
    # our datastructures
    def vizMe(self, figNum=1, markEdges=[], markNodes=[]): abstract()

    def vizMeNot(self): abstract()
        
    def random(self, n): abstract()
        
    def empty(self):  abstract()
    
    def clear(self):  abstract()

