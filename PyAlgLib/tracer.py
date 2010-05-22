#
# Authors: Radu Dragusin and Paula Petcu
# Insitute of Computer Science, Copenhagen University, Denmark
#
# LICENSED UNDER: GNU General Public License v2
#

import sys
import os
import trace

import html

def tracer(filename, funcname, arguments, algdir='algorithms', plottype='line'):
	""" Trace the execution of a Python program using the trace library, 
	and pass the results to the HTML generator.
	"""
	modname = os.path.splitext(os.path.basename(filename))[0]
	function = "__import__('"+algdir+"."+modname+"')."+modname+'.'+funcname+'('+arguments+')'
	
	trac = trace.Trace(count=True, trace=True)
			
	# Temporarily redirecting stdout to a file
	f = open('flow.txt','w')
	sys.stdout = f
	trac.run(function)
	sys.stdout = sys.__stdout__
	f.close()
	
	# Count number of execution per line
	counts = trac.counts
	linecounts = {}
	p = os.path.abspath(os.path.join(algdir,filename))
	for count in counts:
		if p in count:
			linecounts[count[1]] = counts[count]

	flowarray = getAlgorithmFlow(filename,'flow.txt')

	ht = html.HtmlReporter()
	return ht.html_file(os.path.join(algdir,filename),modname,linecounts,flowarray,plottype)

def getAlgorithmFlow(filename,flow_filename):
	"""Return an array containing the code trace as line numbers
	"""
	file = open(flow_filename)
	lines = file.readlines()
	file.close()

	flow = []

	for line in lines:
		if filename in line:
			flow.append(int(line.split('(')[1].split(')')[0]))
			
	return flow
