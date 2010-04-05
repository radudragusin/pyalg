import trace
import sys
import os

import html

filename = 'insertion3.py'
funcname = 'InsertionSort'
arguments = '[7,2,5,32,56,21,1]'
modname = os.path.splitext(os.path.basename(filename))[0]
exec 'import ' + modname
function = modname+'.'+funcname+'('+arguments+')'

tracer = trace.Trace(count=True, trace=True)

# Temporarily redirecting stdout to a file
f = open('flow.txt','w')
sys.stdout = f
tracer.run(function)
sys.stdout = sys.__stdout__
f.close()

counts = tracer.counts
linecounts = {}
p = os.path.abspath(filename)
for count in counts:
	if p in count:
		linecounts[count[1]] = counts[count]

ht = html.HtmlReporter()
ht.html_file(filename,modname,linecounts)
