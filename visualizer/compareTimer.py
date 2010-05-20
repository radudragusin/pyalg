import os.path
from timeit import Timer

class CompareTimer():
	def __init__(self,filenames, funcnames, listSizes, algnames, imgfilename, nrexec):
		self.filenames, self.funcnames, self.listSizes, self.algnames, self.imgfilename, self.nrexec = filenames, funcnames, listSizes, algnames, imgfilename, nrexec

	def getTimes(self,arguments):
		"""For each algorithm and arguments, call getTime
		"""
		times = []
		for i in range(len(self.filenames)):
			filename,funcname = self.filenames[i],self.funcnames[i]
			tim = self.getTime(filename,funcname,str(arguments))
			times.append((self.algnames[i],tim))
		return times

	def getTime(self,filename, funcname, arguments, algdir='algorithms'):
		"""Return the running time of funcname with the given arguments
		"""
		modname = os.path.splitext(os.path.basename(filename))[0]
		t = Timer(''+funcname+'('+arguments+')','from '+algdir+'.'+modname+' import '+funcname)
		return t.timeit(self.nrexec)

	def createGraph(self,timeResults):
		"""Visually represent the results of the getTimes as a plot, and save it as an image
		"""
		import matplotlib.pyplot as plt
		plt.ioff()
		fig = plt.figure()
		ax = fig.add_subplot(111)
		a = range(self.listSizes[0],self.listSizes[1])
		for i in range(len(self.filenames)):
			values = [timeResults[j][1] for j in range(len(timeResults)) if timeResults[j][0] == self.algnames[i]]
			ax.plot(a,values)
		leg = [self.algnames[i] for i in range(len(self.algnames))]
		ax.legend(tuple(leg),'upper center', shadow=True)
		ax.set_xlabel('Range')
		ax.set_ylabel('Time')
		fig.savefig(self.imgfilename)
