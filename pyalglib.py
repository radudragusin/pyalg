'''Algorithms Library in Python.

Originally designed for the 'Algorithms and Data Structures' course held
at the Copenhagen University - Department of Computer Science.
Based on the algorithms presented in the 'Introduction to Algorithms'
book by Cormen et al. 
Uses the algorithms library implemented by Massimo Di Pierro
(https://launchpad.net/algorithms-animator).

TO-DO:
- CountingSort is inconsistent in the sense that it return a sorted list,
while the other algs modify the list
- A random generator with different distributions
	Add examples (like: get sorting list + shuffle)
- If a list is not given as argument for genBST, generate a random BST
- Watch out that some methods in algs return the modified trees, and some
jost modify it.
- Catch error raised by BSTDelete (Index out of bounds)
- Add more __cmp__ options for Nodes in BST
- Generate graph: add argument for directed non symetric, 
					add more letters,
					add separate probability for loops
	
'''

import random
import sys

import csc321algorithms as algs

#
# SORTING ALGORITHMS
#

def insertionSort(A):
	'''Do Insertion Sort and return the sorted list. Take a list as the argument.'''
	algs.InsertionSort(A)
	print A
	return A
	
def mergeSort(A):
	'''Do Merge Sort and return the sorted list. Take a list as the argument.'''
	algs.MergeSort(A)
	print A
	return A
	
def heapSort(A):
	'''Do Heap Sort and return the sorted list. Take a list as the argument.'''
	algs.HeapSort(A)
	print A
	return A
	
def quickSort(A):
	'''Do Quick Sort and return the sorted list. Take a list as the argument.'''
	algs.QuickSort(A)
	print A
	return A

def randQuickSort(A):
	'''Do Randomized Quick Sort and return the sorted list. Take a list as the argument.'''
	algs.RandomizedQuickSort(A)
	print A
	return A
	
def countingSort(A):
	'''Do Counting Sort and return the sorted list. Take a list as the argument.'''
	A = algs.CountingSort(A)
	print A
	return A

def countingSortSmall(A):
	'''Do Counting Sort Small and return the sorted list. Take a list as the argument.'''
	algs.CountingSortSmall(A)
	print A
	return A

def genList(size=10, lower_bound=0, upper_bound=sys.maxint-1, distribution='normal'): 
	'''Generate lists for testing the sorting algorithms.
	
	Keyword arguments:
	size - the size of the list to generate (default 10)
	lower_bound - the lower bound of the range from which the elements of the list are generated (default 0)
	upper_bound - the upper bound of the range from which the elements of the list are generated (default sys.maxint-1)
	distribution - the type of distribution to use when sampling the elements of the list (default 'normal')
	'''
	if distribution == 'normal':
		return random.sample(xrange(lower_bound,upper_bound), size)
	else:
		return []
		
#insertionSort(genList())
#mergeSort(genList())
#heapSort(genList())
#quickSort(genList())
#randQuickSort(genList())
#countingSortSmall(genList(upper_bound=100))
#countingSort(genList(upper_bound=100))

#
#BINARY SEARCH TREES ALGORITHMS
#

class Node:
	'''Node data type'''
	def __init__(self, value='', parent=None, tag=''):
		self.value = value
		self.parent = parent        
		self.tag = tag

	def __cmp__(self, other):
		if self.value<other: return -1
		if self.value>other: return +1
		return 0
	def __repr__(self):
		return repr(self.value)
	pass
	
def NodesList(list):
	'''Transform a regular list in a list of elements of type Node.'''
	for i in range(len(list)):
		item = list[i]
		list[i] = Node(item)
	return list

def BSTInorderWalk(tree):
	'''Traverse the BST tree given as argument.'''
	list = algs.BSTInorderWalk(tree)
	print list
	return list
	
def BSTSearch(tree, k):
	'''Search a Binary Search Tree for the node with value k in the BST given as argument.'''
	item = algs.BSTSearch(tree, k)
	if item != None:
		print "Element", item, "found in the tree."
		return item
	else:
		print "Element", k, "not found in the tree."
	
def BSTIterativeSearch(tree, k):
	'''Iterative Search a Binary Search Tree for the node with value k in the BST given as argument.'''
	item = algs.BSTIterativeSearch(tree, k)
	if item != None:
		print "Element", item, "found in the tree."
		return item
	else:
		print "Element", k, "not found in the tree."
		return

def BSTInsert(tree, k):
	'''Insert a node with value k in the BST given as argument and return the modified BST.'''
	tree = algs.BSTInsert(tree, Node(k))
	print tree
	return tree
	
def BSTDelete(tree,k):
	'''Delete the k'th element from the BST given as argument and return the modified BST.'''
	algs.BSTDeleteIndex(tree,k)
	print tree
	return tree

def genBST(list):
	'''Generate a Binary Search Tree from the list given as an argument.'''
	bstree = []
	for i in list:
		bstree = algs.BSTInsert(bstree,Node(i))
	print bstree
	return bstree

#bstree = genBST(genList(size=8,upper_bound=100))
#BSTInorderWalk(bstree)
#BSTSearch(bstree,9)
#BSTIterativeSearch(bstree,5)
#BSTInsert(bstree,9)
#BSTSearch(bstree,9)
#BSTDelete(bstree,2)


#
# AVL TREES ALGORITHMS
#

def AVLSearch(tree, k):
	'''Search an AVL tree for the node with value k in the BST given as argument.'''
	item = algs.BSTSearch(tree, k)
	if item != None:
		print "Element", item, "found in the tree."
		return item
	else:
		print "Element", k, "not found in the tree."
		
def AVLInsert(tree, k):
	'''Insert a node with value k in the AVL tree given as argument and return the modified AVL tree.'''
	tree = algs.BSTInsert(tree, Node(k))
	algs.AVLRebalanceTree(tree)
	print tree
	return tree

def AVLDelete(tree, k):
	'''Delete the k'th element from the AVL tree given as argument and return the modified AVL tree.'''
	algs.BSTDeleteIndex(tree,k)
	algs.AVLRebalanceTree(tree)
	print tree
	return tree

def genAVL(list):
	'''Generate an AVL tree from the list given as an argument.'''
	tree = algs.List2AVLTree(NodesList(list))
	print tree
	return tree
	
#avltree = genAVL(genList(size=8,upper_bound=100))
#AVLInsert(avltree,6)
#AVLSearch(avltree,3)
#AVLDelete(avltree,3)
#AVLSearch(avltree,3)


#
# GRAPHS
#

def Graph(graph):
	'''Graph data type
	Example input: [['a', 'b', 'c', 'd'], [[0,0,5], [0,1,3], [0,2,7], [3,1,9]]] 
	'''
	vertices=graph[0]
	links=graph[1]
	for i in range(len(vertices)):
		vertices[i]=Node(vertices[i],'')
	for i in range(len(links)):
		link=links[i]
		try:
			if link.source<0 or link.source>=len(vertices):
				raise 'Incorrect link'
			elif link.destination<0 or link.destination>=len(vertices):
				raise 'Incorrect link'
			links[i].color=None
		except:            
			if link[0]<0 or link[0]>=len(vertices):
				raise 'Incorrect link'
			elif link[1]<0 or link[1]>=len(vertices):
				raise 'Incorrect link'
			try:
				links[i]=algs.Link(source=link[0], destination=link[1], length=eval(repr(link[2])))
			except:
				links[i]=algs.Link(source=link[0], destination=link[1])
	return [vertices,links]

def graphBreadthFirstSearch(graph, start=0):
	'''Traverse the graph with Breadth First Search. Return the indeces visited.'''
	nodes = algs.BreadthFirstSearch(graph, start)
	print nodes
	return nodes

def graphDepthFirstSearch(graph, start=0):
	'''Traverse the graph with Depth First Search. Return the indeces visited.'''
	nodes = algs.DepthFirstSearch(graph, start)
	print nodes
	return nodes

def graphTopologicalSortBFS(graph,start=0):
	'''Traverse the graph with Breadth First Search. Return the nodes visited.'''
	list = algs.TopologicalSort(graph,start,algs.BreadthFirstSearch)
	print list
	return list
	
def graphTopologicalSortDFS(graph,start=0):
	'''Traverse the graph with Depth First Search. Return the nodes visited.'''
	list = algs.TopologicalSort(graph,start,algs.DepthFirstSearch)
	print list
	return list
	
def graphToUndirected(graph):
	'''Transform a directed graph into an undirected graph.'''
	algs.SymmetrizeGraph(graph)
	return graph
	
def graphDijkstra(graph, start=0):
	'''Apply Dijkstra's algorithm of finding the shortest path from a starting 
	node to all the other nodes in the graph.
	Pay attention that the distance from the starting node to itself will 
	always be zero, even if the graph given as argument states otherwise.
	'''
	res = algs.Dijkstra(graph, start)
	print res
	return graph
	
def graphBellmanFord(graph, start=0):
	'''Apply Bellman Ford's algorithm of finding the shortest path from a starting 
	node to all the other nodes in the graph.
	'''
	print algs.BellmanFord(graph,start)
	
def genGraph(nodes=5, directed=True, loops=True, len_lower_bound=0, len_upper_bound=100, edge_prob=0.5):
	'''Generate a graph. Can be directed or undirected, based on the bool argument.'''
	#Example of graph:
	#graph = Graph([['a', 'b', 'c', 'd'], [[0,0,5], [0,1,3], [0,2,7], [3,1,9], [2,1,6]]])
	#Example of graph to test Bellman Ford on:
	#graph = Graph([['a', 'b', 'c', 'd'], [[0,0,5], [0,1,3], [0,2,7], [3,1,9], [2,1,-6], [1,3,-1],[3,2,20]]])
	vertices = [chr(i) for i in xrange(ord('a'), ord('a')+nodes)]
	edges = []
	for i in range(nodes):
		for j in range(nodes):
			if not (loops == False and i == j):
				r = random.random()
				if r > edge_prob:
					edges.append([i,j,random.randint(len_lower_bound,len_upper_bound)])
	print [vertices,edges]
	graph = Graph([vertices,edges])
	if directed == False:
		graphToUndirected(graph)
	return graph
	
#graf = genGraph(nodes=10,loops=False)
#print graf
#graphBreadthFirstSearch(graf)
#graphDepthFirstSearch(graf)
#graphTopologicalSortBFS(graf)
#graphTopologicalSortDFS(graf)
#graphToUndirected(graf)
#print graf
#graphBreadthFirstSearch(graf)
#graphDepthFirstSearch(graf)
#graphTopologicalSortBFS(graf)
#graphTopologicalSortDFS(graf)
#graphDijkstra(graf)
#graphBellmanFord(graf)

#
# MINIMUM SPANNING TREES
#

def MSTKruskal(graph):
	'''Compute the minimum spanning tree for a given graph using Kruskal's algorithm'''
	A = algs.MSTKruskal(graph)
	print A
	return A
	
def MSTPrim(graph, start):
	'''Compute the minimum spanning tree for a given graph using Prim's algorithm'''
	A = algs.MSTPrim(graph, start)
	print A
	return A
	
#mygraf = genGraph(nodes=10,loops=False)
#MSTKruskal(mygraf)
#MSTPrim(mygraf,0)

#
# STACKS AND QUEUES
#

def stackPush(stack, node):
	'''Insert a node on the stack, as the first element of the list'''
	algs.Push(stack, node)
	print stack
	return stack
	
def stackPop(stack):
	'''Remove and return the first element of the list'''
	el = algs.Pop(stack)
	print el, stack
	return stack
	
def queueEnqueue(queue, node):
	'''Insert a node in the queue, as the last element of the list.'''
	algs.Enqueue(queue, node)
	print queue
	return queue
	
def queueDequeue(queue):
	'''Remove and return the first element of the list '''
	el = algs.Dequeue(queue)
	print el, queue
	return el
	
#myStack = genList(upper_bound=50)
#stackPush(myStack,2)
#stackPop(myStack)
#myQueue = genList(upper_bound=50)
#queueEnqueue(myQueue,9)
#queueDequeue(myQueue)
