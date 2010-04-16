import trace
import sys
import os

import html
import instrTracer

def tracer(filename, funcname, arguments):
		#filename = 'insertion2.py'
		#funcname = 'InsertionSort'
		##arguments = '[7,2,5,32,56,21,1]'
		#import random
		#list = random.sample(xrange(0,300), 100)
		#arguments = str(list)
		
		modname = os.path.splitext(os.path.basename(filename))[0]
		function = "__import__('"+modname+"')."+funcname+'('+arguments+')'
		
		trac = trace.Trace(count=True, trace=True)
				
		# Temporarily redirecting stdout to a file
		f = open('flow.txt','w')
		sys.stdout = f
		
		trac.run(function)
		sys.stdout = sys.__stdout__
		f.close()

		counts = trac.counts
		linecounts = {}
		p = os.path.abspath(filename)
		for count in counts:
			if p in count:
				linecounts[count[1]] = counts[count]
				
		flowarray = instrTracer.getAlgorithmFlow(filename,'flow.txt')

		ht = html.HtmlReporter()
		return ht.html_file(filename,modname,linecounts,flowarray)

if __name__ == "__main__":
	filename = 'insertion.py'
	funcname = 'InsertionSort'
	arguments = '[7,2,5,32,56,21,1]'
	html_filename = tracer(filename, funcname, arguments)
