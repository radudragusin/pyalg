import trace
import os
import sys

def getPerf(filenames,funcnames,listSizes,lineSelections,algdir='algorithms'):
	
	trac = trace.Trace(count=True)
	
	functions = []
	for i in range(len(filenames)):
		filename, funcname = filenames[i], funcnames[i]
		modname = os.path.splitext(os.path.basename(filename))[0]
		functions.append("__import__('"+algdir+"."+modname+"')."+modname+'.'+funcname+'(')
	
	results = []
	for size in range(listSizes[0],listSizes[1]):
		list = genList(size)
		for i in range(len(funcnames)):
			function = functions[i]
			lineSel = lineSelections[i]
			
			# Temporarily redirecting stdout to a file
			f = open('flow2.txt','w')
			sys.stdout = f
			trac.run(function+str(list)+')')
			sys.stdout = sys.__stdout__
			f.close()
			
			counts = trac.counts
			linecounts = {}
			p = os.path.abspath(os.path.join(algdir,filenames[i]))
			for count in counts:
				if p in count:
					linecounts[count[1]] = counts[count]
			results.append((filenames[i],size,linecounts[lineSel]))
	
	return results

def createGraph(perfResults,filenames,funcnames,listSizes,lineSelections,algnames,imgfilename):
	import matplotlib.pyplot as plt
	fig = plt.figure()
	ax = fig.add_subplot(111)
	a = range(listSizes[0],listSizes[1])
	for i in range(len(filenames)):
		values = [perfResults[j][2] for j in range(len(perfResults)) if perfResults[j][0] == filenames[i]]
		ax.plot(a,values)
	leg = [algnames[i]+" - Line "+str(lineSelections[i]) for i in range(len(algnames))]
	ax.legend(tuple(leg),'upper center', shadow=True)
	ax.set_xlabel('List Size --->')
	ax.set_ylabel('Line Count --->')
	fig.savefig(imgfilename)

def genList(size, lower_bound=0, upper_bound=10000): 
	"""Generate lists for testing the sorting algorithms.
	"""
	import random
	return random.sample(xrange(lower_bound,upper_bound), size)

def compare(filenames, funcnames, listSizes, lineSelections, algnames, imgfilename):
	perfResults = getPerf(filenames, funcnames, listSizes, lineSelections)
	createGraph(perfResults,filenames,funcnames,listSizes,lineSelections,algnames,imgfilename)
	

if __name__ == "__main__":
	filenames = ['insertion.py','quicksort.py']
	funcnames = ['InsertionSort','QuickSort']
	listSizes = (10,50)
	lineSelections = [5,5]
	algnames = ['Insertion Sort', 'My Quick Sort']
	imgfilename = 'algorithms/algPerf.svg'
	compare(filenames, funcnames, listSizes, lineSelections, algnames, imgfilename)

