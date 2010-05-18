##
## list.py
##

import matplotlib.pyplot as plt
import networkx as nx
import random as r



class List(list):
    ''' Simply inherit the original list class and extend with new 
    functionality, such as vizMe, randomgenerator, etc.
'''      
    def __init__ (self, content=[]):
        for i in content:
            self.append(i)
        plt.ion()
        self._G = nx.Graph()

    def visualise(self, figNum=1, positioning=None):

        def calcPos(lst):
            pos = {}
            labels = {}
            for i in range(0,len(lst)):
                pos[i] = (i,0)
                labels[i] = lst[i]
            return pos, labels

        plt.figure(figNum, facecolor='white')
        plt.clf()
        plt.axis('off')
        self._G.clear()
        if not positioning:
            positioning = calcPos
        for i in range(0,len(self)):
            self._G.add_node(i)
        pos, labels = positioning(self)
        
#        nx.draw_networkx(self.G, pos)
        nx.draw_networkx_nodes(self._G, pos, node_color='#557A66')#, edge_color='#272E2E')
        nx.draw_networkx_labels(self._G, pos, labels=labels)
        

    def clearVisualisation(self):
        plt.close()
        
    def generaterandomlist(self, numberofelements, minimumvalue, maximumvalue):
        self.empty()
        for i in range(0,numberofelements):
            self.append(r.randint(0,numberofelements))
            
            
    def empty(self):
        self.clear()
    
    def clear(self): 
        while not self == []:
            self.pop()
            
            
            
