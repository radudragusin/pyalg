##
## tree.py
##

import matplotlib.pyplot as plt
import networkx as nx
import random as r

class Tree():
    def __init__ (self, children=[]):
        self.children = children
        plt.ion()
        self.G=nx.Graph()
    def getChildren(self):
        return self.children
    def setChildren(self, children):
        self.children = children
    def addChild(self, child):
        self.children.append(child)
    def removeChild(self):
        self.children.pop()

    def vizMe(self, figNum=1):
        '''Visualize the tree'''
        
        def getEdges(tree,p=0,num=0):
            '''Return list of edges for drawing the tree'''
            this = num
            if(p != this):
                e = [(p,this)]
            else:
                e = []
            for t in tree.children:
                if not isinstance(t, Leaf):
                    res = getEdges(t,this,num+1)
                else:
                    #We reached a leaf
                    if(p!=num):
                        res = [[(this,num+1)],num+1]
                    else:
                        res = []
                num = res[1]
                e += res[0]
            if(p != this):
                return [e, num]
            else:
                return e
                
        def fam(tree):   
            '''Returns a list with the number of familymembers on each level below the given root.'''        
            res = []
            if not isinstance(tree, Leaf):
                if(tree.children == []):
                    return []
                else:
                    for child in tree.children:
                            res.append(fam(child))                  
                    addedRes = addList(res)
                    return [len(tree.children)] + addedRes
            else:
                #We reached leaf
                return []
                
        def getPercentage(lst):
            '''Calculates how much space a given child should recieve, to draw a nice tree'''
            tmp = []
            totals = addList(lst)
            for i in range(0,len(lst)):
                tmp.append(1.0/float(len(lst)))
                for j in range(0,len(lst[i])):
                    tmp[i] += float(lst[i][j])/(float(totals[j]))
            totL = len(totals);
            if(totL <= 0):
                for i in range(0,len(lst)):
                    tmp[i] = 1.0/float(len(lst))
                return tmp            
            else:
                for i in range(0,len(lst)):
                    tmp[i] = tmp[i]/float(totL+1)
                return tmp 
                
        def addList(lst):
            tmp = []
            for l in lst:
                for i in range(0,len(l)):
                    try:
                        tmp[i] += l[i]
                    except:
                        tmp.append(l[i])
            return tmp

        def getCount(tree):
            '''Calculates the number of nodes'''
            c = 1
            if not isinstance(tree, Leaf):
                for t in tree.children:
                    c += getCount(t)
            return c

        def pos(tree,num=0, ph=0, pw=0, space=1):
            '''Recursively calculates the position of the nodes in the tree'''
            d = {num:(pw,ph)}
            edge = pw-(space/2.0)
            deepNodeCount = []
            #Get the family of all children
            for t in tree.children:
                deepNodeCount.append(fam(t))
            #Calculate the percentage(width) each child should recieve in the tree
            perc = getPercentage(deepNodeCount)
            c = 0
            #Calculate positions for all children, and family recursively
            for t in tree.children:
                l = float(space)*perc[c]
                if not isinstance(t, Leaf):
                    res = pos(t,num+1, ph-1, edge+(l/2.0), l)
                else:
                    #We reached a leaf
                    res = [{num+1:(edge+(l/2.0),ph-1)}, num+1]
                edge += l
                c += 1
                num = res[1]
                d.update(res[0])
            return [d, num]
        
        def getPos(tree,num=0, ph=0, pw=0, space=1):
            '''Creates a position dictionary'''
            p = pos(tree, num, ph, pw, space)
            return p[0]

        ##VISUALIZE##
        plt.figure(figNum)
        plt.clf()
        plt.axis('on')
        self.G.clear()
        p = getPos(self)
        e = getEdges(self)
        for i in range(0,getCount(self)):
            self.G.add_node(i)
        self.G.add_edges_from(e)
        nx.draw_networkx(self.G, p)

    
                
class Leaf:
    def __init__(self, content):
        self.content = content        
    def getContent(self):
        return self.content
    def setContent(self,content):
        self.content = content
        
t1 = Tree([Tree([Tree([Leaf('a'),Leaf('b')]),Tree([Leaf('c'),Leaf('d')])]),Tree([Leaf('e'),Leaf('f')])])
t2 = Tree([Tree([Tree([Leaf('a'),Leaf('b')]),Tree([Leaf('c'),Leaf('d')])]),Tree([Leaf('e'),Leaf('f')]), Tree([Tree([Leaf('g'),Leaf('h')]), Tree([Tree([Leaf('i'),Leaf('j'),Leaf('k'),Leaf('l')])])])])
t3 = Tree([Tree([Tree([Leaf('a'),Leaf('b')]),Tree([Leaf('c'),Leaf('d')])]),Tree([Leaf('e'),Leaf('f')]), Tree([Tree([Leaf('g'),Leaf('h'),Tree([Tree([Leaf('i'),Leaf('j'),Leaf('k'),Leaf('l')])])]), Tree([Tree([Leaf('m'),Leaf('n'),Leaf('o'),Leaf('p')])])])])

