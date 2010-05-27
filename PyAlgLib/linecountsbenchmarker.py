#
# Authors: Radu Dragusin and Paula Petcu
# Insitute of Computer Science, Copenhagen University, Denmark
#
# LICENSED UNDER: GNU General Public License v2
#

import os
import sys
import trace

class LineCountsBenchmarker():
	def __init__(self, filenames, funcnames, listSizes, lineSelections, algnames, imgfilename,algdir='algorithms'):
		self.filenames, self.funcnames, self.listSizes, self.lineSelections, self.algnames, self.imgfilename, self.algdir =\
		  filenames, funcnames, listSizes, lineSelections, algnames, imgfilename,algdir
		self.trac = trace.Trace(count=True)
		functions = []
		for i in range(len(filenames)):
			filename, funcname = filenames[i], funcnames[i]
			modname = os.path.splitext(os.path.basename(filename))[0]
			functions.append("__import__('"+algdir+"."+modname+"')."+modname+'.'+funcname+'(')
		self.functions = functions

	def getPerf(self,arguments):
		"""Return the number of executions for each selected line in each algorithm.
		"""
		results = []
		for i in range(len(self.funcnames)):
			function = self.functions[i]
			lineSels = self.lineSelections[i]

			f = open('flow2.txt','w')
			sys.stdout = f
			self.trac.run(function+str(arguments)+')')
			sys.stdout = sys.__stdout__
			f.close()
			
			counts = self.trac.counts
			linecounts = {}
			p = os.path.abspath(os.path.join(self.algdir,self.filenames[i]))
			for count in counts:
				if p in count:
					linecounts[count[1]] = counts[count]
			for lineSel in lineSels:
				try:
					results.append((self.algnames[i],lineSel,linecounts[lineSel]))
				except KeyError:
					results.append((self.algnames[i],lineSel,0))
		return results

	def createGraph(self,perfResults):
		"""Visually represent the results of the getPerf as a plot, and save it as an image
		"""
		import matplotlib.pyplot as plt
		plt.ioff()
		fig = plt.figure()
		ax = fig.add_subplot(111)
		a = range(self.listSizes[0],self.listSizes[1])
		leg = []
		for i in range(len(self.algnames)):
			currAlgName = self.algnames[i]
			for currLineSel in self.lineSelections[i]:
				values = [perfResults[j][2] for j in range(len(perfResults)) if currAlgName == perfResults[j][0] and currLineSel == perfResults[j][1]]
				ax.plot(a,values)
				leg.append(currAlgName+' - Line '+str(currLineSel))
		ax.legend(tuple(leg),'upper center', shadow=True)
		ax.set_xlabel('Range')
		ax.set_ylabel('Line Count')
		fig.savefig(self.imgfilename)
		
	def createHeatmaps(self,perfResults,secondRange):
		"""Visually represent the results of the getPerf as a plot, and save it as an image
		"""
		import matplotlib.pyplot as plt
		from mpl_toolkits.axes_grid import AxesGrid
		from numpy import reshape
		plt.ioff()
		fig = plt.figure()
		noOfImgsInGrid = 0
		for i in range(len(self.algnames)):
			noOfImgsInGrid += len(self.lineSelections[i])
		grid = AxesGrid(fig, 111, nrows_ncols = (noOfImgsInGrid,1), axes_pad=0.3, cbar_mode='single')
		a = range(self.listSizes[0],self.listSizes[1])
		b = range(secondRange[0],secondRange[1])
		vmn,vmx = 0,max([perfResults[j][2] for j in range(len(perfResults))])
		currentGridNumber = 0
		for i in range(len(self.algnames)):
			currAlgName = self.algnames[i]
			for currLineSel in self.lineSelections[i]:
				values = [perfResults[j][2] for j in range(len(perfResults)) if currAlgName == perfResults[j][0] and currLineSel == perfResults[j][1]]
				im = grid[currentGridNumber].imshow(reshape(values,(-1,len(b))), vmin=vmn, vmax=vmx, extent=(secondRange[0],secondRange[1],self.listSizes[1],self.listSizes[0]))
				grid[currentGridNumber].set_ylabel(currAlgName+' - Line '+str(currLineSel)+'\n First Range')
				grid[currentGridNumber].set_xlabel('Second Range')
				currentGridNumber += 1
		plt.colorbar(im,cax=grid.cbar_axes[0])
		grid.cbar_axes[0].colorbar(im)
		grid.cbar_axes[0].axis['right'].toggle(ticklabels=True)
		fig.savefig(self.imgfilename)
		
