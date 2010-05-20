##
## list.py
##

import matplotlib.pyplot as plt
import networkx as nx
import random as r



class List(list):
    ''' Simply inherit the original list class and extend with new 
    functionality, such as visualise, generateRandomList, etc.
'''      
    def __init__ (self, content=None):
        if not content:
            content = []
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

        nx.draw_networkx(self._G, pos, labels=labels,node_color='#557A66')

#        nx.draw_networkx(self._G, pos, labels=labels,\
#         node_color='#9ed95e')
        #nx.draw_networkx(self._G, pos2, nodelist=[3])
#        nx.draw_networkx_nodes(self._G, pos, node_color='#557A66', node_shape='s')#, edge_color='#272E2E')
#        nx.draw_networkx_labels(self._G, pos, labels=labels)
        

    def clearVisualisation(self):
        plt.close()
        
    def generateRandomList(self, length=0, minvalue=0, maxvalue=20):
        if length == 0:
            length = r.randint(5,20)
            
        self.clear()
        for i in range(0,length):
            self.append(r.randint(minvalue,maxvalue))
        
#        self.append("wuhuuu!");
    
    def clear(self): 
        self = list()            
            
            
