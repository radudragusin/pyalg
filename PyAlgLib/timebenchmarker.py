#
# Authors: Radu Dragusin and Paula Petcu
# Insitute of Computer Science, Copenhagen University, Denmark
#
# LICENSED UNDER: GNU General Public License v2
#

import os.path
from timeit import Timer

class TimeBenchmarker():
	def __init__(self,filenames, funcnames, listSizes, algnames, imgfilename, nrexec):
		self.filenames, self.funcnames, self.listSizes, self.algnames, self.imgfilename, self.nrexec = \
		  filenames, funcnames, listSizes, algnames, imgfilename, nrexec

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
		
	def createHeatmaps(self,timeResults,secondRange):
		"""Visually represent the results of the getTimes as heatmaps, and save it as an image
		"""
		import matplotlib.pyplot as plt
		from mpl_toolkits.axes_grid import AxesGrid
		from numpy import reshape
		plt.ioff()
		fig = plt.figure()
		noOfImgsInGrid = len(self.algnames)
		grid = AxesGrid(fig, 111, nrows_ncols = (noOfImgsInGrid,1), axes_pad=0.3, cbar_mode='single')
		a = range(self.listSizes[0],self.listSizes[1])
		b = range(secondRange[0],secondRange[1])
		vmn,vmx = 0,max([timeResults[j][1] for j in range(len(timeResults))])
		for i in range(len(self.filenames)):
			currAlgName = self.algnames[i]
			values = [timeResults[j][1] for j in range(len(timeResults)) if timeResults[j][0] == currAlgName]
			im = grid[i].imshow(reshape(values,(-1,len(b))), vmin=vmn, vmax=vmx, extent=(secondRange[0],secondRange[1],self.listSizes[1],self.listSizes[0]))
			grid[i].set_ylabel(currAlgName+'\n First Range')
			grid[i].set_xlabel('Second Range')
		plt.colorbar(im,cax=grid.cbar_axes[0])
		grid.cbar_axes[0].colorbar(im)
		grid.cbar_axes[0].axis['right'].toggle(ticklabels=True)
		fig.savefig(self.imgfilename)
