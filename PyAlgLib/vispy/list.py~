##
## Authors: Kim Lundsteen Juncher and Brian Soborg Mathiasen
## Insitute of Computer Science, Copenhagen University, Denmark
##
## Date: 22-05-2010
##
## list.py
##
## LICENSED UNDER: GNU General Public License v2
##

import matplotlib.pyplot as plt
import networkx as nx
import random as r



class List(list):
    """ inherits the built-in list container and extend with new 
    functionality, such as visualise, generateRandomList, etc."""
    def __init__ (self, content=None):
        """ constructor. Specify the content variable to add content to the
        structure at initialisation. """
        if not content:
            content = []
        for i in content:
            self.append(i)

    def __subconstruct__(self):
        """Sub constructor managing initialisations needed for visualisations.
        This method is invoked implicitly."""
        plt.ion()
        self._G = nx.Graph()

    def visualise(self, figNum=1, positioning=None):
        """ Method to invoke the visualisation of the content of the structure."""
        try:
            if self._G:
                pass
        except AttributeError:
            self.__subconstruct__()
            
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
        """ Clears and closes the active visualisations"""
        plt.close()
        
    def generateRandomList(self, length=0, minvalue=0, maxvalue=20):
        """ Generates and occupies the structure with random elements."""
        if length == 0:
            length = r.randint(5,20)
            
        self.clear()
        for i in range(0,length):
            self.append(r.randint(minvalue,maxvalue))
        
#        self.append("wuhuuu!");
    
    def clear(self): 
        """ Clears and empties the structure of elements """
        self = list()            
        self.__subconstruct__()
            
