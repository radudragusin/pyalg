##
## list.py
##

import matplotlib.pyplot as plt
import networkx as nx
import random as r



class list(list):
    ''' Simply inherit the original list class and extend with new 
    functionality, such as vizMe, randomgenerator, etc.
'''      
    def __init__ (self, content=[]):
        for i in content:
            self.append(i)
        plt.ion()
        self.G = nx.Graph()

    def vizMe(self, figNum=1, positioning=None):

        def calcPos(list):
            pos = {}
            for i in range(0,len(list)):
                pos.update({list[i]:(i,0)})
            return pos

        plt.figure(figNum, facecolor='white')
        plt.clf()
        plt.axis('off')
        self.G.clear()
        if not positioning:
            positioning = calcPos
        for i in self:
            self.G.add_node(i)
        pos = positioning(self.G.nodes())
        
        nx.draw_networkx(self.G, pos)

        

    def vizMeNot(self):
        plt.close()
        
    def random(self, length):
        self.empty()
        for i in range(0,length):
            self.append(r.randint(0,length))

    def genRandomList(self, int_length=10):
        self.empty()
        for i in range(0,int_length):
            self.append(r.randint(0,int_length))
            
    def empty(self):
        self.clear()
    
    def clear(self): 
        while not self == []:
            self.pop()
            
            
            
