from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os
import platform

import ui_pyalg
import tracer

__version__ = "0.0.1"

class PyAlgAnalyzer(QMainWindow, ui_pyalg.Ui_MainWindow):
	def __init__(self,parent=None):
		"""Initializes the main window of the application and connects the application's 
		events with its logic part.
		"""
		super(PyAlgAnalyzer,self).__init__(parent)
		self.setupUi(self)
		
		self.setupInitView()
		
		self.connect(self.algTree, SIGNAL("itemClicked(QTreeWidgetItem*,int)"), self.showOptions4Algorithm)
		
		self.connect(self.listInputRadioButton, SIGNAL("clicked()"), self.showListEditor)
		self.connect(self.listGenRadioButton, SIGNAL("clicked()"), self.showListGeneratorSettings)
		self.connect(self.listSortButton, SIGNAL("clicked()"), self.updateWebView)
		
		self.connect(self.pathBrowseButton, SIGNAL("clicked()"), self.updateNewAlgPath)
		self.connect(self.pathLineEdit, SIGNAL("textChanged(QString)"), self.showNewAlgProperties)
		self.connect(self.newAlgCancelButton, SIGNAL("clicked()"), self.newAlgDockWidget.hide)
		self.connect(self.newAlgArgsListView1, SIGNAL("clicked(QModelIndex)"), self.selectNewAlgArgument)
		self.connect(self.newAlgAddArgButton, SIGNAL("clicked()"), self.addNewAlgArgument)
		self.connect(self.newAlgArgsListView2, SIGNAL("clicked(QModelIndex)"), self.selectModifNewAlgArgument)
		self.connect(self.newAlgArgUpButton, SIGNAL("clicked()"), self.moveUpNewAlgArgument)
		self.connect(self.newAlgArgDownButton, SIGNAL("clicked()"), self.moveDownNewAlgArgument)
		self.connect(self.newAlgArgDelButton, SIGNAL("clicked()"), self.deleteNewAlgArgument)
		
		self.connect(self.aboutAction, SIGNAL("triggered()"), self.showAboutWindow)
		self.connect(self.newAction, SIGNAL("triggered()"), self.showNewAlgWindow)
		
	
	### INITIAL SETUP
		
	def setupInitView(self):
		"""Setup the initial view of the program:
		* hide algorithm options windows
		* hide the new algorithm uploading windows
		* initialize the tree of available algorithms
		* add the list of available function arguments to the new-alg functionality  
		"""
		self.algOptionsDockWidget.hide()
		self.listSettingsGroupBox.hide()
		self.listInputLineEdit.hide()
		self.listSortButton.setEnabled(False)
		
		self.updateAlgTree()
		
		self.newAlgDockWidget.hide()
		self.newAlgPropGroupBox.setEnabled(False)
		
		self.newAlgArgsListView1.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.newAlgArgsListView1.setModel(QStringListModel(QStringList(self.getListOfFuncArgs())))
		self.newAlgArgsListView2.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.newAlgArgsModel = QStringListModel(QStringList([]))
		self.newAlgArgsListView2.setModel(self.newAlgArgsModel)
		self.newAlgAddArgButton.setEnabled(False)
		self.newAlgArgOpGroupBox.setEnabled(False)
		
	def updateAlgTree(self,confFilePath='algorithms/alg.conf',sep=';'):
		"""Read the algorithms configuration file which includes the 
		information necessary for populating the algorithm tree view. 
		Update the tree view based on the information from the file.
		"""
		lines = open(confFilePath).readlines()
		self.algConf = []
		for line in lines:
			self.algConf.append(line.strip('\n').split(sep))
		
		self.algTree.clear()
		
		parents = set([self.algConf[i][0] for i in range(len(self.algConf))])
		for parent in parents:
			wid = QTreeWidgetItem(None, QStringList(parent))
			self.algTree.addTopLevelItem(wid)
			self.algTree.expandItem(wid)
			u = QTreeWidget(self.algTree.itemWidget(wid,1))
			
			for i in range(len(self.algConf)):
				if self.algConf[i][0] == parent:
					children  = self.algConf[i][1]
					u.addTopLevelItem(QTreeWidgetItem(wid, QStringList(children)))
		self.parents = parents
		
	### FUNCTIONALITIES FOR THE LIST ALGORITHMS
				
	def showListGeneratorSettings(self):
		"""Show the settings for generating a list to sort.
		"""
		self.listInputLineEdit.hide()
		self.listSettingsGroupBox.show()
		self.listSortButton.setEnabled(True)
	
	def showListEditor(self):
		"""Show the line edit for writing a user-defined list to sort.
		"""
		self.listSettingsGroupBox.hide()
		self.listInputLineEdit.show()
		self.listSortButton.setEnabled(True)
		
	def genList(self, size, lower_bound, upper_bound, distribution='normal'): 
		"""Generate lists for testing the sorting algorithms.
		Keyword arguments:
		size - the size of the list to generate (default 10)
		lower_bound - the lower bound of the range from which the elements of the list are generated (default 0)
		upper_bound - the upper bound of the range from which the elements of the list are generated (default sys.maxint-1)
		distribution - the type of distribution to use when sampling the elements of the list (default 'normal')
		"""
		if distribution == 'normal':
			import random
			return random.sample(xrange(lower_bound,upper_bound), size)
		else:
			return []
		
	### SHOWING OPTIONS FOR SELECTED ALGORITHM
	
	def showOptions4Algorithm(self,item,column):
		"""Show the available options for the selected algorithm.
		"""
		self.webView.setUrl(QUrl('about:blank'))
		itemParent = item.parent()
		if itemParent is not None:
			parentName = itemParent.text(column)
			if parentName == 'Sorting Algorithms':
				algName = item.text(column)
				self.algOptionsDockWidget.show()
				
				el =[i for i in range(len(self.algConf)) if algName in self.algConf[i]]
				if len(el) != 0:
					el = el[0]
					self.filename = self.algConf[el][2]
					self.funcname = self.algConf[el][3]
		else:
			self.algOptionsDockWidget.hide()
			
	### UPDATING THE WEB VIEW BASED ON THE SELECTED ALGORITHM
			
	def updateWebView(self):
		"""Update the content of the web page displaying the algorithm's code and analysis. 
		"""
		if self.listInputRadioButton.isChecked() == True:
			arguments = str(self.listInputLineEdit.text())
		elif self.listGenRadioButton.isChecked() == True:
			arguments = str(self.genList(self.listSizeBox.value(),self.listLBoundBox.value(),self.listUBoundBox.value()))
		try:
			list = eval(arguments)
			if type(list) == type([]) and len(list) > 0:
				try:
					html_filename = tracer.tracer(self.filename, self.funcname, arguments)
					self.webView.setUrl(QUrl(html_filename))
				except StandardError as detail:
					box = QMessageBox(QMessageBox.Warning, "Warning", "Invalid Code. Please review the code and upload it again.")
					box.setDetailedText(str(detail))
					box.exec_()
			else:
				box = QMessageBox(QMessageBox.Warning, "Warning", "Input must be a non-empty list. Try something similar to: [3,1,4,9,5]")
				box.exec_()
		except(NameError, SyntaxError):
			box = QMessageBox(QMessageBox.Warning, "Warning", "Input not a list. Try something similar to: [3,1,4,9,5]")
			box.exec_()

	
	### NEW ALGORITHM DOCK WIDGET FUNCTIONALITIES
	
	def showNewAlgWindow(self):
		"""Open a pop-up window for adding a new algorithm to the existing library.
		"""
		self.newAlgDockWidget.show()
	
	def updateNewAlgPath(self):
		"""Opens a file browsing window for selection of a Python file, and 
		updates the corresponding line edit for the path.
		"""
		browsingStartPoint = os.getenv('USERPROFILE') or os.getenv('HOME')
		filename = QFileDialog.getOpenFileName(self, "Select Python File", browsingStartPoint)
		if filename != "":
			self.pathLineEdit.setText(filename)
	
	def showNewAlgProperties(self,path):
		"""Populate the available properties for the selected file.
		"""
		path = os.path.normpath(str(path))
		if os.path.isfile(path) and path.endswith('.py'):
			self.newAlgPropGroupBox.setEnabled(True)
			functions = self.getNewAlgFunctions(path)
			self.newAlgFuncComboBox.clear()
			self.newAlgFuncComboBox.addItems(QStringList(functions))
			types = list(self.parents)
			types.insert(0,'')
			self.newAlgTypeComboBox.clear()
			self.newAlgTypeComboBox.addItems(QStringList(types))
		else:
			self.newAlgPropGroupBox.setEnabled(False)
	
	def getNewAlgFunctions(self,path):
		"""Returns all Python function definitions from the code given 
		in the path argument.
		"""
		functions = []
		lines = open(path).readlines()
		for line in lines:
			if line.strip().startswith('def '):
				functions.append(line.strip().split()[1].split(':')[0])
		return functions
		
	def getListOfFuncArgs(self):
		"""Return the list of available function arguments - needed for 
		populating the list view of the new algorithm functionality."""
		return ['List','Graph','Tree','Int']
		
	def selectNewAlgArgument(self, index):
		"""Store the selected argument for the new function/algorithm and
		enable the 'add argument' button."""
		self.newAlgAddArgButton.setEnabled(True)
		self.selectedArg = index.data().toString()
		
	def addNewAlgArgument(self):
		currList = self.newAlgArgsModel.stringList()
		currList.append(self.selectedArg)
		self.newAlgArgsModel = QStringListModel(QStringList(currList))
		self.newAlgArgsListView2.setModel(self.newAlgArgsModel)
		
	def selectModifNewAlgArgument(self, index):
		self.newAlgArgOpGroupBox.setEnabled(True)
		self.selectedModifArgIndex = index.row()
		
	def moveUpNewAlgArgument(self):
		currList = self.newAlgArgsModel.stringList()
		if self.selectedModifArgIndex > 0:
			currArg = currList.takeAt(self.selectedModifArgIndex)
			currList.insert(self.selectedModifArgIndex-1,currArg)
			self.newAlgArgsModel = QStringListModel(QStringList(currList))
			self.newAlgArgsListView2.setModel(self.newAlgArgsModel)
			self.newAlgArgOpGroupBox.setEnabled(False)
			self.selectedModifArgIndex = -1
	
	def moveDownNewAlgArgument(self):
		currList = self.newAlgArgsModel.stringList()
		if -1 < self.selectedModifArgIndex < len(currList)-1:
			currArg = currList.takeAt(self.selectedModifArgIndex)
			currList.insert(self.selectedModifArgIndex+1,currArg)
			self.newAlgArgsModel = QStringListModel(QStringList(currList))
			self.newAlgArgsListView2.setModel(self.newAlgArgsModel)
			self.newAlgArgOpGroupBox.setEnabled(False)
			self.selectedModifArgIndex = -1	
			
	def deleteNewAlgArgument(self):
		currList = self.newAlgArgsModel.stringList()
		if self.selectedModifArgIndex != -1:
			currList.takeAt(self.selectedModifArgIndex)
			self.newAlgArgsModel = QStringListModel(QStringList(currList))
			self.newAlgArgsListView2.setModel(self.newAlgArgsModel)
			self.newAlgArgOpGroupBox.setEnabled(False)
			self.selectedModifArgIndex = -1	
		
	
	### MENU FUNCTIONALITIES
	
	def showAboutWindow(self):
		"""Open a message box containing appplication information.
		"""
		QMessageBox.about(self, "About PyAlgLib",
			"""<b>PyAlgLib</b> v %s
			<p>An algorithms learning platform in Python.
			<p><a href="http://code.google.com/p/pyalg">PyAlgLib Web Site</a>
			<p>Copyright &copy; 2010. 
			Radu Dragusin, Paula Petcu.
			<p>Code License: <a href="http://www.gnu.org/licenses/old-licenses/gpl-2.0.html">GNU General Public License v2</a>
			<p>Python %s -Qt %s -PyQt %s on %s"""
			% (__version__,platform.python_version(),QT_VERSION_STR,PYQT_VERSION_STR,platform.system()))
	
	def closeEvent(self, event):
		"""Called either when the Quit button or the X is pressed.
		"""
		event.accept()
 
if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	form = PyAlgAnalyzer()
	form.show()
	app.exec_()
