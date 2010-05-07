""" Based on http://nedbatchelder.com/code/coverage """

import os
import re
import shutil

import numpy
import matplotlib
matplotlib.use('QT4Agg')
import matplotlib.pyplot as plt
import matplotlib.transforms as transf

from phystokens import source_token_lines
from templite import Templite

class HtmlReporter(object):
    """HTML reporting."""

    def __init__(self):
		#TO-DO: Handle when template not available
		self.source_tmpl = Templite(open("htmlfiles/pyfile.html").read(), globals())

    def html_file(self, pyfile, modname, linecounts, flowarray, colorLineOnSelect, plottype, imagetype='svg'):
        """Generate a HTML file for one source file.
        """

        source = open(pyfile).read()
        htmldir = 'htmlfiles'
        lines = []
        plotvalues = []
        if colorLineOnSelect:
            colorOnSelect = "changeColor(this.id)"
        else:
            colorOnSelect = ""

        for lineno, line in enumerate(source_token_lines(source)):
            lineno += 1
            line_class = []
            annotate_html = ""
            annotate_title = ""
            
            if lineno in linecounts:
				linecount = linecounts[lineno]
            else:
                linecount = 0
            plotvalues.append(linecount)
            
            # Build the HTML for the line
            html = []
            for tok_type, tok_text in line:
                if tok_type == "ws":
                    html.append(escape(tok_text))
                else:
                    tok_html = escape(tok_text) or '&nbsp;'
                    html.append(
                        "<span class='%s'>%s</span>" % (tok_type, tok_html)
                        )

            lines.append({
                'html': ''.join(html),
                'number': lineno,
                'count': linecount,
                'class': ' '.join(line_class) or "pln",
                'annotate': annotate_html,
                'annotate_title': annotate_title,
            })
            
        imagefile = modname + '.' + imagetype
        plotLineCounts(plotvalues,os.path.join(htmldir, imagefile),lineno, imagetype,plottype)
        algflow = flowarray

        # Write the HTML page for this file.
        html_filename = os.path.join(htmldir, os.path.splitext(os.path.basename(pyfile))[0] + ".html")
        html = spaceless(self.source_tmpl.render(locals()))
        fhtml = open(html_filename, 'w')
        fhtml.write(html)
        fhtml.close()
        
        return html_filename


# Helpers for templates and generating HTML

def plotLineCounts(plotvalues,imgfilename,lineno,imagetype,plottype):
	"""Generate an image containing the plot of the line counts, and save it.
	"""
	if plottype == 'line':
		#Ugly solution for cropping the plot generated by matplotlib
		il = 16.6/100
		a = .28 * lineno
		b = .57 * a
		c = .43 * a
		fig = plt.figure(figsize=(0.5,(lineno+a)*il),frameon=False)
		bbox = transf.Bbox.from_extents(0,b*il,0.5,(lineno+a)*il-c*il)
		ax = fig.add_subplot(111)
		ax.invert_yaxis()
		ax.invert_xaxis()
		ax.set_axis_off()
		ax.plot(plotvalues,range(0,len(plotvalues)), 'r')
		fig.savefig(imgfilename,orientation='portrait',format=imagetype,transparent=True,bbox_inches=bbox)
	elif plottype == 'bar' or plottype == 'filledbar':
		#Ugly solution for cropping the plot generated by matplotlib
		il = 16.6/100
		if lineno % 2 == 0:
			a = .30 * lineno
		else:
			a = .36 * lineno
		b = .57 * a
		c = .43 * a
		fig = plt.figure(figsize=(0.5,(lineno+a)*il),frameon=False)
		bbox = transf.Bbox.from_extents(0,b*il,0.5,(lineno+a)*il-c*il)
		ax = fig.add_subplot(111)
		ax.invert_yaxis()
		ax.invert_xaxis()
		ax.set_axis_off()
		#barh does not plot values 0 from the endings, so had to add 1 
		#to all values to force them to be plotted:
		filled = False
		if plottype == 'filledbar':
			filled = True
		ax.barh(range(0,len(plotvalues)),[val+1 for val in plotvalues],fill=filled) 
		fig.savefig(imgfilename,orientation='portrait',format=imagetype,transparent=True,bbox_inches=bbox)
	

def escape(t):
    """HTML-escape the text in t.
    """
    return (t
            # Convert HTML special chars into HTML entities.
            .replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace("'", "&#39;").replace('"', "&quot;")
            # Convert runs of spaces: "......" -> "&nbsp;.&nbsp;.&nbsp;."
            .replace("  ", "&nbsp; ")
            # To deal with odd-length runs, convert the final pair of spaces
            # so that "....." -> "&nbsp;.&nbsp;&nbsp;."
            .replace("  ", "&nbsp; ")
        )

def spaceless(html):
    """Squeeze out some annoying extra space from an HTML string.
    Nicely-formatted templates mean lots of extra space in the result.  Get
    rid of some.
    """
    html = re.sub(">\s+<p ", ">\n<p ", html)
    return html
