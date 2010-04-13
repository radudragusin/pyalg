from PyQt4.QtCore import *
from PyQt4.QtGui import *

import ui_pyalg
import tracer

class PyAlgAnalyzer(QMainWindow, ui_pyalg.Ui_MainWindow):
	def __init__(self,parent=None):
		"""Initializes the main window of the application and connects the application's 
		events with its logic part.
		"""
		super(PyAlgAnalyzer,self).__init__(parent)
		self.setupUi(self)
		
		self.initList2Sort()
		
		self.connect(self.treeWidget, SIGNAL("itemClicked(QTreeWidgetItem*,int)"), self.showOptions4Algorithm)
		self.connect(self.radioButton, SIGNAL("clicked()"), self.showListEditor)
		self.connect(self.radioButton_2, SIGNAL("clicked()"), self.showListGeneratorSettings)
		self.connect(self.pushButton, SIGNAL("clicked()"), self.updateWebView)
		
	def initList2Sort(self):
		self.dockWidget.hide()
		self.groupBox.hide()
		self.lineEdit.hide()
		self.pushButton.setEnabled(False)
			
	def showListGeneratorSettings(self):
		self.lineEdit.hide()
		self.groupBox.show()
		self.pushButton.setEnabled(True)
	
	def showListEditor(self):
		self.groupBox.hide()
		self.lineEdit.show()
		self.pushButton.setEnabled(True)
		
	def showOptions4Algorithm(self,item,column):
		self.webView.setUrl(QUrl('about:blank'))
		itemParent = item.parent()
		if itemParent is not None:
			nameParent = itemParent.text(column)
			if nameParent == 'Sorting Algorithms':
				alg_name = item.text(column)
				self.dockWidget.show()
				if alg_name == 'Insertion Sort':
					self.filename = 'insertion.py'
					self.funcname = 'InsertionSort'
				else: 
					if alg_name == 'Quick Sort':
						self.filename = 'quicksort.py'
						self.funcname = 'QuickSort'
		else:
			self.dockWidget.hide()
			
	def updateWebView(self):
		if self.radioButton.isChecked() == True:
			arguments = str(self.lineEdit.text())
		elif self.radioButton_2.isChecked() == True:
			arguments = str(self.genList(self.spinBox.value(),self.spinBox_2.value(),self.spinBox_3.value()))
		try:
			list = eval(arguments)
			if type(list) == type([]) and len(list) > 0:
				html_filename = tracer.tracer(self.filename, self.funcname, arguments)
				self.webView.setUrl(QUrl(html_filename))
			else:
				box = QMessageBox(QMessageBox.Warning, "Warning", "Input must be a non-empty list. Try something similar to: [3,1,4,9,5]")
				box.exec_()
		except(NameError, SyntaxError):
			box = QMessageBox(QMessageBox.Warning, "Warning", "Input not a list. Try something similar to: [3,1,4,9,5]")
			box.exec_()


	def genList(self, size, lower_bound, upper_bound, distribution='normal'): 
		'''Generate lists for testing the sorting algorithms.
		Keyword arguments:
		size - the size of the list to generate (default 10)
		lower_bound - the lower bound of the range from which the elements of the list are generated (default 0)
		upper_bound - the upper bound of the range from which the elements of the list are generated (default sys.maxint-1)
		distribution - the type of distribution to use when sampling the elements of the list (default 'normal')
		'''
		if distribution == 'normal':
			import random
			return random.sample(xrange(lower_bound,upper_bound), size)
		else:
			return []

 
if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	form = PyAlgAnalyzer()
	form.show()
	app.exec_()
