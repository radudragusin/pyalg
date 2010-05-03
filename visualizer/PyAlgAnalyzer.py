from PyQt4.QtCore import *
from PyQt4.QtGui import *

import os
import os.path
import platform
import shutil

import tracer
import ui_pyalg
from PyAlgWizard import *

__version__ = "0.0.1"

class PyAlgAnalyzer(QMainWindow, ui_pyalg.Ui_MainWindow):
	def __init__(self,parent=None):
		"""Initializes the main window of the application and connects 
		the application's events with its logic part.
		"""
		super(PyAlgAnalyzer,self).__init__(parent)
		self.setupUi(self)
		
		self.setupInitView()
		
		self.connect(self.algTree, SIGNAL("itemClicked(QTreeWidgetItem*,int)"), self.askAlgorithmInput)
		
		# List generator widgets
		self.connect(self.listInputRadioButton, SIGNAL("clicked()"), self.showListEditor)
		self.connect(self.listGenRadioButton, SIGNAL("clicked()"), self.showListGeneratorSettings)
		self.connect(self.listSortButton, SIGNAL("clicked()"), self.updateWebView)
		
		# Adding new algorithm widgets
		self.connect(self.pathBrowseButton, SIGNAL("clicked()"), self.updateNewAlgPath)
		self.connect(self.pathLineEdit, SIGNAL("textChanged(QString)"), self.showNewAlgProperties)
		self.connect(self.newAlgCancelButton, SIGNAL("clicked()"), self.newAlgDockWidget.hide)
		self.connect(self.newAlgArgsListView1, SIGNAL("clicked(QModelIndex)"), self.selectNewAlgArgument)
		self.connect(self.newAlgAddArgButton, SIGNAL("clicked()"), self.addNewAlgArgument)
		self.connect(self.newAlgArgsListView2, SIGNAL("clicked(QModelIndex)"), self.selectModifNewAlgArgument)
		self.connect(self.newAlgArgUpButton, SIGNAL("clicked()"), self.moveUpNewAlgArgument)
		self.connect(self.newAlgArgDownButton, SIGNAL("clicked()"), self.moveDownNewAlgArgument)
		self.connect(self.newAlgArgDelButton, SIGNAL("clicked()"), self.deleteNewAlgArgument)
		self.connect(self.newAlgAddButton, SIGNAL("clicked()"), self.addNewAlg)
		
		self.connect(self.algTree, SIGNAL("itemSelectionChanged()"), self.disableAlgEditing)
		
		# Menu actions
		self.connect(self.deleteAction, SIGNAL("triggered()"), self.deleteAlgorithm)
		self.connect(self.renameAction, SIGNAL("triggered()"), self.renameAlgorithm)
		self.connect(self.argumentsAction, SIGNAL("triggered()"), self.changeArgsAlgorithm)
		self.connect(self.aboutAction, SIGNAL("triggered()"), self.showAboutWindow)
		self.connect(self.newAction, SIGNAL("triggered()"), self.showNewAlgWindow)
		self.connect(self.compAction, SIGNAL("triggered()"), self.showCompareWiz)
		
	
	### INITIAL SETUP
		
	def setupInitView(self):
		"""Setup the initial view of the program:
		* hide algorithm options windows
		* hide the new algorithm uploading windows
		* initialize the tree of available algorithms
		* add the list of available arguments to the new-alg feature  
		* disable algorithm editing menus
		"""
		self.algOptionsDockWidget.hide()
		self.listSettingsGroupBox.hide()
		self.listInputLineEdit.hide()
		self.listSortButton.setEnabled(False)
		
		self.confFilePath = 'algorithms/alg.conf'
		
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
		
		self.renameAction.setEnabled(False)
		self.deleteAction.setEnabled(False)
		self.argumentsAction.setEnabled(False)
		
	def updateAlgTree(self,sep=';'):
		"""Read the algorithms configuration file which includes the 
		information necessary for populating the algorithm tree view. 
		Update the tree view based on the information from the file.
		"""
		self.algConf = []
		try:
			lines = open(self.confFilePath).readlines()
			for line in lines:
				if line !='\n':
					self.algConf.append(line.strip('\n').split(sep))
		except IOError:
			pass

		self.algTree.clear()
		
		parents = set([self.algConf[i][0] for i in range(len(self.algConf))])
		for parent in parents:
			algTypeItem = QTreeWidgetItem(None, QStringList(parent))
			self.algTree.addTopLevelItem(algTypeItem)
			self.algTree.expandItem(algTypeItem)
			algTypeItem.setFlags(Qt.ItemIsEnabled)
			algTypeWidget = QTreeWidget(self.algTree.itemWidget(algTypeItem,1))
			
			for i in range(len(self.algConf)):
				if self.algConf[i][0] == parent:
					children  = self.algConf[i][1]
					algTypeWidget.addTopLevelItem(QTreeWidgetItem(algTypeItem, QStringList(children)))
		self.parents = parents
		
	# TO-DO: add data generators for more types of arguments (currently 
	#implemented: list)
		
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
		"""
		if distribution == 'normal':
			import random
			return random.sample(xrange(lower_bound,upper_bound), size)
		else:
			return []
		
	### SHOWING OPTIONS FOR SELECTED ALGORITHM
	
	def askAlgorithmInput(self,item,column):
		"""Show the available input arguments for the selected algorithm.
		TO-DO: remove hard-coded sorting algorithms and add other types
		of algorithms as soon as the new data generators are implemented.
		"""
		self.webView.setUrl(QUrl('about:blank'))
		itemParent = item.parent()
		if itemParent is not None:
			parentName = itemParent.text(column)
			if parentName == 'Sorting Algorithms':
				algName = str(item.text(column))
				self.algOptionsDockWidget.show()
				
				el = [confIndex for confIndex in range(len(self.algConf))\
				  if algName in self.algConf[confIndex][1]]
				if len(el) != 0:
					el = el[0]
					self.filename = self.algConf[el][2]
					self.funcname = self.algConf[el][3]
		else:
			self.algOptionsDockWidget.hide()
			
	### UPDATING THE WEB VIEW BASED ON THE SELECTED ALGORITHM
			
	def updateWebView(self):
		"""Update the content of the web page displaying the algorithm's 
		code and analysis. 
		TO-DO: evaluate the corectness of the arguments for datatypes 
		other than lists, as soon as the data generators are added.
		"""
		if self.listInputRadioButton.isChecked() == True:
			arguments = str(self.listInputLineEdit.text())
		elif self.listGenRadioButton.isChecked() == True:
			arguments = str(self.genList(self.listSizeBox.value(),
			  self.listLBoundBox.value(),self.listUBoundBox.value()))
		try:
			list = eval(arguments)
			if type(list) == type([]) and len(list) > 0:
				try:
					html_filename = tracer.tracer(self.filename, self.funcname, arguments)
					self.webView.setUrl(QUrl(html_filename))
				except StandardError as detail:
					box = QMessageBox(QMessageBox.Warning, "Warning", 
					  "Invalid Code. Please review the code and upload it again.")
					box.setDetailedText(str(detail))
					box.exec_()
			else:
				QMessageBox(QMessageBox.Warning, "Warning", 
				  "Input must be a non-empty list. Try something similar to: [3,1,4,9,5]").exec_()
		except(NameError, SyntaxError):
			QMessageBox(QMessageBox.Warning, "Warning", 
			  "Input not a list. Try something similar to: [3,1,4,9,5]").exec_()

	
	### NEW ALGORITHM DOCK WIDGET FUNCTIONALITIES
	
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
		This is done when the line edit for the path of the file is changed.
		"""
		path = os.path.normpath(str(path))
		if os.path.isfile(path) and path.endswith('.py'):
			self.newAlgPropGroupBox.setEnabled(True)
			functions = self.getNewAlgFunctions(path)
			self.newAlgFuncComboBox.clear()
			self.newAlgFuncComboBox.addItems(QStringList(functions))
			types = list(self.parents)
			if '' not in types:
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
		"""Return the list of available function arguments types - needed for 
		populating the list view of the new algorithm functionality.
		TO-DO: connect this with actual data generators
		"""
		return ['List','Graph','Tree','Int']
		
	def selectNewAlgArgument(self, index):
		"""Store the selected argument type from the available list of 
		arguments and enable the 'add argument' button.
		"""
		self.newAlgAddArgButton.setEnabled(True)
		self.selectedArg = index.data().toString()
		
	def addNewAlgArgument(self):
		"""Add the currently selected argument type to the list of
		arguments for the new algorithm.
		TO-DO: after adding, the selection is set to the new arg type
		"""
		currList = self.newAlgArgsModel.stringList()
		currList.append(self.selectedArg)
		self.newAlgArgsModel = QStringListModel(QStringList(currList))
		self.newAlgArgsListView2.setModel(self.newAlgArgsModel)
		
	def selectModifNewAlgArgument(self, index):
		"""Store the selected argument type for the new algorithm and
		enable the buttons for editing the order of arguments.
		"""
		self.newAlgArgOpGroupBox.setEnabled(True)
		self.selectedModifArgIndex = index.row()
		
	def moveUpNewAlgArgument(self):
		"""Move one position up the selected argument type.
		TO-DO: after moving, the selection remains on the moved arg type
		"""
		currList = self.newAlgArgsModel.stringList()
		if self.selectedModifArgIndex > 0:
			currArg = currList.takeAt(self.selectedModifArgIndex)
			currList.insert(self.selectedModifArgIndex-1,currArg)
			self.newAlgArgsModel = QStringListModel(QStringList(currList))
			self.newAlgArgsListView2.setModel(self.newAlgArgsModel)
			self.newAlgArgOpGroupBox.setEnabled(False)
			self.selectedModifArgIndex = -1
	
	def moveDownNewAlgArgument(self):
		"""Move one position down the selected argument type.
		TO-DO: after moving, the selection remains on the moved arg type
		"""
		currList = self.newAlgArgsModel.stringList()
		if -1 < self.selectedModifArgIndex < len(currList)-1:
			currArg = currList.takeAt(self.selectedModifArgIndex)
			currList.insert(self.selectedModifArgIndex+1,currArg)
			self.newAlgArgsModel = QStringListModel(QStringList(currList))
			self.newAlgArgsListView2.setModel(self.newAlgArgsModel)
			self.newAlgArgOpGroupBox.setEnabled(False)
			self.selectedModifArgIndex = -1	
			
	def deleteNewAlgArgument(self):
		"""Delete the selected argument type.
		"""
		currList = self.newAlgArgsModel.stringList()
		if self.selectedModifArgIndex != -1:
			currList.takeAt(self.selectedModifArgIndex)
			self.newAlgArgsModel = QStringListModel(QStringList(currList))
			self.newAlgArgsListView2.setModel(self.newAlgArgsModel)
			self.newAlgArgOpGroupBox.setEnabled(False)
			self.selectedModifArgIndex = -1	
		
	def addNewAlg(self):
		"""Add the new algorithm to the library of available algorithms 
		(if all required input is correct).
		TO-DO: If a filename already exists, append a counter at the end
		of the file instead of appending zeros.
		"""
		fileName = str(self.pathLineEdit.text())
		funcName = str(self.newAlgFuncComboBox.currentText()).split('(')[0]
		algName = str(self.newAlgNameLineEdit.text().trimmed())
		parentName = str(self.newAlgTypeComboBox.currentText())
		arguments = [str(arg) for arg in self.newAlgArgsModel.stringList()]

		if algName != "" and len([i for i in range(len(self.algConf)) if algName in [self.algConf[i][1]]])==0:
			newPath = os.path.join(os.path.join(os.getcwd(),'algorithms'),os.path.basename(fileName))
			while os.path.exists(newPath):
				newPath = newPath[:-3] + '0' + newPath[-3:]
			shutil.copyfile(fileName, newPath)
			self.algConf.append([parentName,algName,os.path.basename(newPath),funcName,str(arguments)])
			self.saveAlgConf()
			QMessageBox(QMessageBox.Information , "Success", "OK. Algorithm added.").exec_()
			self.newAlgDockWidget.hide()
		else:
			QMessageBox(QMessageBox.Warning, "Warning", "Algorithm name empty or already used.").exec_()
	
	def saveAlgConf(self):
		"""Write to the algorithms configuration file the current structure, 
		and update the algorithms tree from the interface.
		"""
		with open(self.confFilePath,'w') as file:
			for i in range(len(self.algConf)):
				file.write(self.algConf[i][0]+';'+self.algConf[i][1]+';'+self.algConf[i][2]+\
				  ';'+self.algConf[i][3]+';'+self.algConf[i][4]+'\n')
		self.updateAlgTree()
	
	### MENU FUNCTIONALITIES
	
	def showAboutWindow(self):
		"""Open a message box containing appplication information.
		"""
		QMessageBox.information(self, "About PyAlgLib",
			"""<b>PyAlgLib</b> v %s
			<p>An algorithms learning platform in Python.
			<p><a href="http://code.google.com/p/pyalg">PyAlgLib Web Site</a>
			<p>Copyright &copy; 2010. 
			Radu Dragusin, Paula Petcu.
			<p>Code License: 
			<a href="http://www.gnu.org/licenses/old-licenses/gpl-2.0.html">GNU General Public License v2</a>
			<p>Python %s -Qt %s -PyQt %s on %s"""
			% (__version__,platform.python_version(),QT_VERSION_STR,PYQT_VERSION_STR,platform.system()))
	
	def showNewAlgWindow(self):
		"""Open a pop-up window for adding a new algorithm to the existing library.
		"""
		self.newAlgDockWidget.show()

	def disableAlgEditing(self):
		"""TO-DO: Currently does not work - it should disable the algorithm editing 
		buttons from the menu when no algorithm is selected, and vice-versa."""
		currItem = self.algTree.currentItem()
		if currItem:
			self.renameAction.setEnabled(True)
			self.deleteAction.setEnabled(True)
			self.argumentsAction.setEnabled(True)
		else:
			self.renameAction.setEnabled(False)
			self.deleteAction.setEnabled(False)
			self.argumentsAction.setEnabled(False)

	def deleteAlgorithm(self):
		"""Delete from the library the selected algorithm, if any.
		"""
		currItem = self.algTree.currentItem()
		if currItem:
			if currItem.childCount() == 0:
				currAlgName = str(self.algTree.currentItem().text(0))
				reply = QMessageBox.question(self, "Last chance to change your mind", 
				"Are you sure you want to permanently delete "+currAlgName+\
				" (including the corresponding Python file) from the library?",
				QMessageBox.Yes|QMessageBox.Default, QMessageBox.No|QMessageBox.Escape)
				if reply == QMessageBox.Yes:
					el = [i for i in range(len(self.algConf)) if currAlgName in self.algConf[i][1]][0]
					try:
						os.remove(os.path.join(os.path.join(os.getcwd(),'algorithms'),self.algConf[el][2]))
						self.algConf.pop(el)
						self.saveAlgConf()
					except StandardError as detail:
						box = QMessageBox(QMessageBox.Warning, "Warning", 
						  "Error deleting algorithm.")
						box.setDetailedText(str(detail))
						box.exec_()
			else:
				QMessageBox(QMessageBox.Warning, "Warning", 
				  "Cannot delete algorithm type containing one or more algorithms.").exec_()
		else:
			QMessageBox(QMessageBox.Warning, "Warning", "No algorithm selected.").exec_()
			
	def renameAlgorithm(self):
		"""Rename the selected algorithm from the library, if any selected.
		"""
		currItem = self.algTree.currentItem()
		if currItem:
			if currItem.childCount() == 0:
				currAlgName = str(self.algTree.currentItem().text(0))
				(newAlgName,reply) = QInputDialog.getText(self,"Rename","New name:",
				  QLineEdit.Normal,currAlgName)
				newAlgName = newAlgName.trimmed()
				if reply and newAlgName != currAlgName:
					if len([i for i in range(len(self.algConf)) if newAlgName in [self.algConf[i][1]]])==0:
						el = [i for i in range(len(self.algConf)) if currAlgName in [self.algConf[i][1]]][0]
						self.algConf[el][1] = newAlgName
						self.saveAlgConf()
					else:
						QMessageBox(QMessageBox.Warning, "Warning", "Name already used.").exec_()
			else:
				QMessageBox(QMessageBox.Warning, "Warning", 
				  "Cannot rename algorithm type containing one or more algorithms.").exec_()
		else:
			QMessageBox(QMessageBox.Warning, "Warning", "No algorithm selected.").exec_()	
			
	def changeArgsAlgorithm(self):
		"""Edit the arguments list of the selected algorithm, if any.
		TO-DO: verify if the list of arguments is well-formed
		"""
		currItem = self.algTree.currentItem()
		if currItem:
			if currItem.childCount() == 0:
				currAlgName = str(self.algTree.currentItem().text(0))
				el = [i for i in range(len(self.algConf)) if currAlgName in [self.algConf[i][1]]][0]
				currAlgArgs = self.algConf[el][-1]
				(newAlgArgs,reply) = QInputDialog.getText(self,"Edit Arguments",
				  "New arguments list:",QLineEdit.Normal,currAlgArgs)
				if reply and newAlgArgs != currAlgArgs:
					self.algConf[el][-1] = newAlgArgs
					self.saveAlgConf()
			else:
				QMessageBox(QMessageBox.Warning, "Warning", "Cannot add arguments to algorithm type.").exec_()
		else:
			QMessageBox(QMessageBox.Warning, "Warning", "No algorithm selected.").exec_()					
			
	def showCompareWiz(self):
		"""Open and focus on the Compare Algorithms Wizard.
		"""
		wizard = PyAlgWizard(self)
		wizard.exec_()
			
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
