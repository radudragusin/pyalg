from pyalglib import *

print "SORTING ALGORITHMS\n"
l=genList(upper_bound=100)
print "Insertion sort on",l
insertionSort(l)
l=genList(upper_bound=100)
print "\nMerge sort sort on",l
mergeSort(l)
l=genList(upper_bound=100)
print "\nHeap sort on",l
heapSort(l)
l=genList(upper_bound=100)
print "\nQuick sort on",l
quickSort(l)
l=genList(upper_bound=100)
print "\nRandom quick sort on",l
randQuickSort(l)
#l=genList(upper_bound=100)
#countingSortSmall(l)
l=genList(upper_bound=100)
print "\nCounting sort on",l
countingSort(l)

print "\nBINARY SEARCH TREES ALGORITHMS\n"

bstree = genBST(genList(size=8,upper_bound=100))
print "InorderWalk:"
BSTInorderWalk(bstree)
print "\nSearch for value 9:"
BSTSearch(bstree,9)
#BSTIterativeSearch(bstree,5)
print "\nInsert value 9:"
BSTInsert(bstree,9)
print "\nSearch for value 9:"
BSTSearch(bstree,9)
print "\nDelete the node with index 2:"
BSTDelete(bstree,2)

print "\nAVL TREES ALGORITHMS\n"

avltree = genAVL(genList(size=8,upper_bound=100))
print "AVL tree:", avltree
print "\nInsert value 6:"
AVLInsert(avltree,6)
print "\nSearch for value 6:"
AVLSearch(avltree,6)
print "\nDelete the second node"
AVLDelete(avltree,2)

print "\nGRAPHS\n"

graf = genGraph(nodes=5,loops=False)
print "\nBFS:"
graphBreadthFirstSearch(graf)
print "\nDFS:"
graphDepthFirstSearch(graf)
print "\nTopological BFS:"
graphTopologicalSortBFS(graf)
print "\nTopological DFS:"
graphTopologicalSortDFS(graf)
#graphToUndirected(graf)
print "\nDijkstra:"
graphDijkstra(graf)
print "\nBellman-Ford:"
graphBellmanFord(graf)

print "\nMININUM SPANNING TREES\n"

mygraf = genGraph(nodes=5,loops=False)
print "\nKruskal:"
MSTKruskal(mygraf)
print "\nPrim:"
MSTPrim(mygraf,0)

print "\nSTACKS AND QUEUES\n"

myStack = genList(upper_bound=50)
print myStack
print "\nPush value 2:"
stackPush(myStack,2)
print "\nPop top of stack:"
stackPop(myStack)
myQueue = genList(upper_bound=50)
print "\n",myQueue
print "\nEnqueue value 9:"
queueEnqueue(myQueue,9)
print "\nDequeue first element:"
queueDequeue(myQueue)
