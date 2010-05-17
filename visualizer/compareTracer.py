import os
import sys
import trace

class CompareTracer():
	def __init__(self, filenames, funcnames, listSizes, lineSelections, algnames, imgfilename,algdir='algorithms'):
		self.filenames, self.funcnames, self.listSizes, self.lineSelections, self.algnames, self.imgfilename, self.algdir = filenames, funcnames, listSizes, lineSelections, algnames, imgfilename,algdir
		self.trac = trace.Trace(count=True)
		functions = []
		for i in range(len(filenames)):
			filename, funcname = filenames[i], funcnames[i]
			modname = os.path.splitext(os.path.basename(filename))[0]
			functions.append("__import__('"+algdir+"."+modname+"')."+modname+'.'+funcname+'(')
		self.functions = functions

	def getPerf(self,list):
		"""Return the number of executions for each selected line in each algorithm.
		"""
		results = []
		for i in range(len(self.funcnames)):
			function = self.functions[i]
			lineSel = self.lineSelections[i]

			f = open('flow2.txt','w')
			sys.stdout = f
			self.trac.run(function+str(list)+')')
			sys.stdout = sys.__stdout__
			f.close()
			
			counts = self.trac.counts
			linecounts = {}
			p = os.path.abspath(os.path.join(self.algdir,self.filenames[i]))
			for count in counts:
				if p in count:
					linecounts[count[1]] = counts[count]
			results.append((self.filenames[i],len(list),linecounts[lineSel]))
		return results

	def createGraph(self,perfResults):
		"""Visually represent the results of the getPerf as a plot, and save it as an image
		"""
		import matplotlib.pyplot as plt
		plt.ioff()
		fig = plt.figure()
		ax = fig.add_subplot(111)
		a = range(self.listSizes[0],self.listSizes[1])
		for i in range(len(self.filenames)):
			values = [perfResults[j][2] for j in range(len(perfResults)) if perfResults[j][0] == self.filenames[i]]
			ax.plot(a,values)
		leg = [self.algnames[i]+" - Line "+str(self.lineSelections[i]) for i in range(len(self.algnames))]
		ax.legend(tuple(leg),'upper center', shadow=True)
		ax.set_xlabel('List Size')
		ax.set_ylabel('Line Count')
		fig.savefig(self.imgfilename)
