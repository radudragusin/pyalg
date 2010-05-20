##
## tree.py
##

import matplotlib.pyplot as plt
import networkx as nx
import random as r

class Tree(object):
    def __init__ (self, children = None, content = None):
        """Initialise the Tree object"""
        if not children:
            self.children = []
        else:
            self.children = children
        if not content:
            self.content = ''
        else:
            self.content = content
        # Initialises visualisation related options
        plt.ion()
        self.G=nx.Graph()
    
    def clear(self):
        """Clear the Tree"""
        self.setChildren([])
        self.G = nx.Graph()
        
    def getContent(self):
        """Return content"""
        return self.content
    
    def setContent(self, content):
        """Set content"""
        self.content = content
        
    def getChildren(self):
        """Return all children"""
        return self.children
        
    def setChildren(self, children):
        """Set new children to Tree"""
        self.children = children
        
    def addChild(self, child, index=None):
        """Add new child to Tree"""
        self.children.append(child)
        
    def removeChild(self, index):
        """Remove a child specified by the index"""
        if(self.children.__len__() > index and index > -1):
            del self.children[index]
        
    def generateRandomTree(self, numberofvertices = 10, numberofleafs = 5):
        """Generates a random Tree"""
        
        def maybeAddLeaf(t, content):
            """Recursively (and randomly) goes through the Tree and add a Leaf"""
            index = r.randint(0,len(t.getChildren()))
            if(index == len(t.getChildren())):
                index = r.randint(0,len(t.getChildren()))
                first = t.getChildren()[:index]
                last = t.getChildren()[index:]
                t.setChildren(first + [Leaf(content = 'L')] + last)
            else:
                if(isinstance(t.getChildren()[index], Tree)):
                    maybeAddLeaf(t.getChildren()[index], content)
                else:
                    maybeAddLeaf(t, content)
                    
        def maybeAddNode(t):
            """Recursively (and randomly) goes through the Tree and add a Node"""
            index = r.randint(0,len(t.getChildren()))
            if(index == len(t.getChildren())):
                index = r.randint(0,len(t.getChildren()))
                first = t.getChildren()[:index]
                last = t.getChildren()[index:]
                t.setChildren(first + [Tree(children = None, content = 'T')] + last)
            else:
                maybeAddNode(t.getChildren()[index])
        
        # Clear the Tree
        self.clear()
        # Add children to the tree        
        for i in range(numberofvertices-1):
            maybeAddNode(self)
        for i in range(numberofleafs):
            maybeAddLeaf(self, i)

    def visualise(self, figNum=1, markVertices=None, withLabels = False, structured=False):
        '''Visualize the tree'''
        
        def getEdges(t,p=-1,num=0):
            '''Return list of edges for drawing the tree'''
            if(isinstance(t,Tree)):
                if(p != -1):
                    edges = [(p,num)]
                else:
                    edges = []
                this = num
                for child in t.getChildren():
                    if(child != None):
                        edges += getEdges(child,this,num+1)
                        p,num = edges[-1]
                return edges
            else:
                return [(p,num)]
        
        ### START - Functions used for calculating a more intelligent positioning of the tree's nodes        
        def fam(tree):   
            '''Returns a list with the number of familymembers on each level below the given root.'''        
            res = []
            if isinstance(tree, Tree):
                if(tree.getChildren() == []):
                    return []
                else:
                    for child in tree.getChildren():
                            res.append(fam(child))                  
                    addedRes = addList(res)
                    return [len(tree.getChildren())] + addedRes
            else:
                #We reached leaf
                return res
                
        def getPercentage(tree):
            '''Calculates how much space a given child should recieve, to draw a nice tree'''
            #Get the family of all children
            lst = []
            for t in tree.getChildren():
                lst.append(fam(t))
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
            """Returns a list with the sum of the values 
            for every index in the Lists 
            given a List of Lists with integers"""
            tmp = []
            for l in lst:
                for i in range(0,len(l)):
                    if(len(tmp)>i):
                        tmp[i] += l[i]
                    else:
                        tmp.append(l[i])
            return tmp
        
        def getPosAndObjectListsStructured(tree,num=0, ph=0, pw=0, space=1):
            """Returns a position dictionary, 
            a list with the node Ids, one with the Leaf Ids,
            a dictionary with labels
            and the id of the last added node.
            The positions are calculated trying to draw a more structured tree""" 
            d = {num:(pw,ph)}
            labels = {num:tree.getContent()}
            nodeList = [num]
            leafList = []            
            spaceBuf = float(space)*0.05
            l = pw-(float(space)/2.0) + spaceBuf
            if(len(tree.getChildren()) > 0):
                nodeSpace = (float(space)*0.9)/float(len(tree.getChildren()))
            else:
                nodeSpace = (float(space)*0.9)
            for t in tree.getChildren():
                l += nodeSpace/2
                if(t != None):
                    num += 1
                    if isinstance(t, Tree):
                        nList, lList, res, resLabels, num = getPosAndObjectListsStructured(t,num, ph-1, l, nodeSpace)
                        nodeList += nList
                        leafList += lList
                    else:
                        #We reached a leaf
                        res = {num:(l,ph-1)}
                        resLabels = {num:t.getContent()}
                        leafList.append(num)
                    d.update(res)
                    labels.update(resLabels)
                l += nodeSpace/2
            return nodeList, leafList, d, labels, num
        
        def getPosAndObjectLists(tree,num=0, ph=0, pw=0, space=1):
            """Returns a position dictionary, 
            a list with the node Ids, one with the Leaf Ids,
            a dictionary with labels
            and the id of the last added node.
            The positions are calculated trying to draw a nice looking tree"""   
            d = {num:(pw,ph)}
            labels = {num:tree.getContent()}
            nodeList = [num]
            leafList = []
            edge = pw-(space/2.0)
            
            #Calculate the percentage(width) each child should recieve in the tree
            perc = getPercentage(tree)
            c = 0
            #Calculate positions for all getChildren(), and family recursively
            for t in tree.getChildren():
                l = float(space)*perc[c]
                if(t != None):
                    num += 1
                    if isinstance(t, Tree):
                        nList, lList, res, resLabels, num = getPosAndObjectLists(t,num, ph-1, edge+(l/2.0), l)
                        nodeList += nList
                        leafList += lList
                    else:
                        #We reached a leaf
                        res = {num:(edge+(l/2.0),ph-1)}
                        resLabels = {num:t.getContent()}
                        leafList.append(num)
                    c += 1
                    d.update(res)
                    labels.update(resLabels)                
                edge += l
            return nodeList, leafList, d, labels, num
        
        ### END - Functions used for calculating a more intelligent positioning of the tree's nodes
                
                    
                    
        # Start visualisation
        plt.figure(figNum)
        plt.clf()
        plt.axis('off')
        self.G.clear()
        # Calc position of nodes and edges
        if(structured):
            lstOfNodes,lstOfLeafs,totalPos, labels, lastAddedObject = getPosAndObjectListsStructured(self)        
        else:
            lstOfNodes,lstOfLeafs,totalPos, labels, lastAddedObject = getPosAndObjectLists(self)
        e = getEdges(self)
        # Add edges and nodes to nx.graph
        for i in lstOfLeafs:
            self.G.add_node(i)
        for i in lstOfNodes:
            self.G.add_node(i)
        for x,y in e:
            self.G.add_edge(x,y)
        # Draw the nodes
        if(markVertices == None):
            # Don't mark any vertices
            if(withLabels):
                nx.draw_networkx(self.G, totalPos, nodelist=lstOfLeafs,labels=labels,node_color='#557A66')
                nx.draw_networkx(self.G, totalPos, nodelist=lstOfNodes,labels=labels,node_color='#272E2E')
            else:
                nx.draw_networkx(self.G, totalPos, nodelist=lstOfLeafs,node_color='#557A66')
                nx.draw_networkx(self.G, totalPos, nodelist=lstOfNodes,node_color='#272E2E')
        else:
            # Mark specific vertices
            unmarkedNodes = list(set(lstOfNodes) - set(markVertices))
            unmarkedLeafs = list(set(lstOfLeafs) - set(markVertices))
            markedNodes = list(set(lstOfNodes) - set(unmarkedNodes))
            markedLeafs = list(set(lstOfLeafs) - set(unmarkedLeafs))
            if(withLabels):
                nx.draw_networkx(self.G, totalPos, nodelist=unmarkedLeafs,labels=labels,node_color='#557A66')
                nx.draw_networkx(self.G, totalPos, nodelist=unmarkedNodes,labels=labels,node_color='#272E2E')
                nx.draw_networkx(self.G, totalPos, nodelist=markedLeafs,labels=labels,node_size=700,node_color='#557A66')
                nx.draw_networkx(self.G, totalPos, nodelist=markedNodes,labels=labels,node_size=700,node_color='#272E2E')
            else:
                nx.draw_networkx(self.G, totalPos, nodelist=unmarkedLeafs,node_color='#557A66')
                nx.draw_networkx(self.G, totalPos, nodelist=unmarkedNodes,node_color='#272E2E')
                nx.draw_networkx(self.G, totalPos, nodelist=markedLeafs,node_size=700,node_color='#557A66')
                nx.draw_networkx(self.G, totalPos, nodelist=markedNodes,node_size=700,node_color='#272E2E')
                
class Leaf:
    def __init__(self, content = None):
        """Initialises the Leaf"""
        if not content:
            self.content = ''
        else:
            self.content = content   
             
    def getContent(self):
        """Returns the content of the Leaf"""
        return self.content
        
    def setContent(self,content):
        """Set the content of the Leaf"""
        self.content = content
