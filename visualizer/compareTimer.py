import os.path
from timeit import Timer

def compare(filenames, funcnames, listSizes, algnames, imgfilename, nrexec=10):
	timeResults = getTimes(filenames,funcnames,listSizes,algnames,nrexec)
	createGraph(timeResults,filenames,algnames,listSizes,imgfilename)

def getTimes(filenames, funcnames, listSizes,algnames,nrexec):
	times = []
	for size in range(listSizes[0],listSizes[1]):
		list = genList(size)	
		for i in range(len(filenames)):
			filename,funcname = filenames[i],funcnames[i]
			tim = getTime(filename,funcname,str(list),nrexec)
			times.append((algnames[i],size,tim))
	return times

def getTime(filename, funcname, arguments, nrexec, algdir='algorithms'):
	modname = os.path.splitext(os.path.basename(filename))[0]
	t = Timer(''+funcname+'('+arguments+')','from '+algdir+'.'+modname+' import '+funcname)
	return t.timeit(nrexec)

def createGraph(timeResults,filenames,algnames,listSizes,imgfilename):
	import matplotlib.pyplot as plt
	fig = plt.figure()
	ax = fig.add_subplot(111)
	a = range(listSizes[0],listSizes[1])
	for i in range(len(filenames)):
		values = [timeResults[j][2] for j in range(len(timeResults)) if timeResults[j][0] == algnames[i]]
		ax.plot(a,values)
	leg = [algnames[i] for i in range(len(algnames))]
	ax.legend(tuple(leg),'upper center', shadow=True)
	ax.set_xlabel('List Size --->')
	ax.set_ylabel('Time --->')
	fig.savefig(imgfilename)

def genList(size, lower_bound=0, upper_bound=10000): 
	"""Generate lists for testing the sorting algorithms.
	"""
	import random
	return random.sample(xrange(lower_bound,upper_bound), size)

if __name__ == "__main__":
	filenames = ['insertion.py','quicksort.py']
	funcnames = ['InsertionSort','QuickSort']
	listSizes = (10,12)
	algnames = ['Insertion Sort', 'My Quick Sort']
	imgfilename = 'algorithms/algTime.svg'
	compare(filenames, funcnames, listSizes, algnames, imgfilename)