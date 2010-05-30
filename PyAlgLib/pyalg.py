#
# Authors: Radu Dragusin and Paula Petcu
# Insitute of Computer Science, Copenhagen University, Denmark
#
# LICENSED UNDER: GNU General Public License v2
#

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import QWebView

import os
import os.path
from platform import python_version, system
from webbrowser import open as openWB
import shutil

import tracer
import ui_pyalg
from pyalgwizard import *

__version__ = "0.0.1"
website = "http://code.google.com/p/pyalg"

class PyAlgMainWindow(QMainWindow, ui_pyalg.Ui_MainWindow):
	def __init__(self,parent=None):
		"""Initializes the main window of the application and connects 
		the application's events with its logic part.
		"""
		super(PyAlgMainWindow,self).__init__(parent)
		self.setupUi(self)
		
		self.algDir = 'algorithms'
		self.confFilePath = os.path.join(self.algDir,'.alg.conf')
		self.visPyDir = 'vispy'
		self.helpFile = os.path.join('helpfiles','index.html')
		
		self.setupInitView()
		
		self.connect(self.algTree, SIGNAL("itemClicked(QTreeWidgetItem*,int)"), self.askAlgorithmInput)
		
		# Data generator widgets
		self.connect(self.runTracerButton, SIGNAL("clicked()"), self.updateWebView)
		
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
		self.connect(self.webView, SIGNAL("loadFinished(bool)"), self.enableSaveAction)
		
		# Menu actions
		self.connect(self.deleteAction, SIGNAL("triggered()"), self.deleteAlgorithm)
		self.connect(self.renameAction, SIGNAL("triggered()"), self.renameAlgorithm)
		self.connect(self.argumentsAction, SIGNAL("triggered()"), self.changeArgsAlgorithm)
		self.connect(self.aboutAction, SIGNAL("triggered()"), self.showAboutWindow)
		self.connect(self.websiteAction, SIGNAL("triggered()"), self.openWebsite)
		self.connect(self.newAction, SIGNAL("triggered()"), self.showNewAlgWindow)
		self.connect(self.compAction, SIGNAL("triggered()"), self.showCompareWiz)
		self.connect(self.linePlotAction, SIGNAL("triggered()"), self.setLinePlotType)
		self.connect(self.barPlotAction, SIGNAL("triggered()"), self.setBarPlotType)
		self.connect(self.filledBarPlotAction, SIGNAL("triggered()"), self.setFilledBarPlotType)
		self.connect(self.manualArgsAction, SIGNAL("triggered()"), self.setManualInputType)
		self.connect(self.autoArgsAction, SIGNAL("triggered()"), self.setAutoInputType)
		self.connect(self.nrBenchExecAction, SIGNAL("triggered()"), self.setNrBenchmarkExecutions)
		self.connect(self.saveAction, SIGNAL("triggered()"), self.saveHtml)
		self.connect(self.helpAction, SIGNAL("triggered()"), self.showHelpDialog)
	
	### INITIAL SETUP
		
	def setupInitView(self):
		"""Setup the initial view of the program:
		* hide algorithm options windows
		* hide the new algorithm uploading windows
		* initialize the tree of available algorithms
		* add the list of available arguments to the new-alg feature  
		* disable algorithm editing menus
		* set the tracer plot type to filled bar plot (default)
		* set the args input type to auto (default)
		"""
		self.algOptionsDockWidget.hide()
		
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
		self.newAlgArgsListView1.setDragDropMode(QAbstractItemView.DragOnly)
		self.newAlgArgsListView2.setDragDropMode(QAbstractItemView.DropOnly)
		
		self.selectedAlgorithm = None
		self.renameAction.setEnabled(False)
		self.deleteAction.setEnabled(False)
		self.argumentsAction.setEnabled(False)
		
		self.saveAction.setEnabled(False)
		
		actionGroup = QActionGroup(self)
		self.linePlotAction.setActionGroup(actionGroup)
		self.barPlotAction.setActionGroup(actionGroup)
		self.filledBarPlotAction.setActionGroup(actionGroup)
		self.filledBarPlotAction.setChecked(True)
		self.tracePlotType = 'filledbar' # default value
		
		actionGroup = QActionGroup(self)
		self.manualArgsAction.setActionGroup(actionGroup)
		self.autoArgsAction.setActionGroup(actionGroup)
		self.autoArgsAction.setChecked(True)
		self.inputType = 'auto' # default value
		
		self.nrBenchExec = 1
		
	def updateAlgTree(self,sep=';'):
		"""Read the algorithms configuration file which includes the 
		information necessary for populating the algorithm tree view. 
		Update the tree view based on the information from the file.
		"""
		self.algConf = []
		try:
			file = open(self.confFilePath)
			lines = file.readlines()
			file.close()
			for line in lines:
				if line !='\n':
					self.algConf.append(line.strip('\n').split(sep))
		except IOError:
			pass

		self.algTree.clear()
		
		sections = set([self.algConf[i][0] for i in range(len(self.algConf))])
		for section in sections:
			algTypeItem = QTreeWidgetItem(None, QStringList(section))
			self.algTree.addTopLevelItem(algTypeItem)
			self.algTree.expandItem(algTypeItem)
			algTypeItem.setFlags(Qt.ItemIsEnabled)
			algTypeWidget = QTreeWidget(self.algTree.itemWidget(algTypeItem,1))
			
			for i in range(len(self.algConf)):
				if self.algConf[i][0] == section:
					children  = self.algConf[i][1]
					algTypeWidget.addTopLevelItem(QTreeWidgetItem(algTypeItem, QStringList(children)))
		self.sections = sections
		
		self.algOptionsDockWidget.hide()
		self.renameAction.setEnabled(False)
		self.deleteAction.setEnabled(False)
		self.argumentsAction.setEnabled(False)
		
	### SHOWING ARGUMENTS INPUT FOR SELECTED ALGORITHM
	
	def askAlgorithmInput(self,item,column):
		"""Show the available input arguments for the selected algorithm.
		"""
		itemParent = item.parent()
		if itemParent is not None:
			if self.selectedAlgorithm is not item:
				self.webView.setUrl(QUrl('about:blank'))
				algName = str(item.text(column))
				self.algOptionsDockWidget.show()
				
				algIndex = [confIndex for confIndex in range(len(self.algConf))\
				  if algName in [self.algConf[confIndex][1]]][0]
				
				self.argumentsTabWidget.clear()
				self.addArgumentTabs(eval(self.algConf[algIndex][4]))
				
				self.filename = self.algConf[algIndex][2]
				self.funcname = self.algConf[algIndex][3]
				self.selectedAlgorithm = item
		else:
			self.webView.setUrl(QUrl('about:blank'))
			self.selectedAlgorithm = item
			self.algOptionsDockWidget.hide()
			
	def addArgumentTabs(self, arguments):
		"""Add tab for each input argument corresponding to the selected
		algorithm. For each such tab, add contents (manual/automatic input,
		with corresponding widgets).
		"""
		self.argsType = arguments
		self.argsDict = {}
		for i,arg in enumerate(arguments):
			tab = QWidget()
			tab.setObjectName("argumentsTab"+str(i))
			verticalLayout = QVBoxLayout(tab)
			
			manualInputRadioButton = QRadioButton(tab)
			manualInputRadioButton.setText("Input (manual)")
			manualInputRadioButton.setObjectName("manualInputRadioButton"+str(i))
			verticalLayout.addWidget(manualInputRadioButton)
			
			manualInputLineEdit = QLineEdit(tab)
			manualInputLineEdit.setObjectName("manualInputLineEdit"+str(i))
			verticalLayout.addWidget(manualInputLineEdit)
			
			autoInputRadioButton = QRadioButton(tab)
			autoInputRadioButton.setText("Generate (automatic)")
			autoInputRadioButton.setObjectName("autoInputRadioButton"+str(i))
			verticalLayout.addWidget(autoInputRadioButton)
			
			if self.inputType == 'manual': manualInputRadioButton.setChecked(True)
			elif self.inputType == 'auto': autoInputRadioButton.setChecked(True)
						
			#TO-DO: set max and min values in spin boxes?
			self.argsDict[i] = []
			if arg != 'Int' and arg in self.availableGenerators:
				genLine = self.availableGeneratorsArguments[self.availableGenerators.index(arg)]
				for j,el in enumerate(genLine):
					elName = el.strip()
					spinBox = QSpinBox(tab)
					spinBox.setObjectName("spinBox"+str(i)+str(j))
					spinBox.setMaximum(9999)
					if '=' in elName:
						elName, elDefaultValue = elName.split('=')
						elName, elDefaultValue = elName.strip(), elDefaultValue.strip()
						spinBox.setValue(int(elDefaultValue))
					spinBoxLabel = QLabel(tab)
					spinBoxLabel.setText(elName+':')
					verticalLayout.addWidget(spinBoxLabel)
					verticalLayout.addWidget(spinBox)
					self.argsDict[i].append("spinBox"+str(i)+str(j))
			elif arg == 'Int':
				manualInputRadioButton.setChecked(True)
				autoInputRadioButton.setEnabled(False)
			
			self.argumentsTabWidget.addTab(tab,'(arg '+str(i+1)+') '+arg)
	
	### UPDATING THE WEB VIEW BASED ON THE SELECTED ALGORITHM
			
	def updateWebView(self):
		"""Update the content of the web page displaying the algorithm's 
		code and analysis. Called when the 'run trace' button is pressed.
		Get input (manual or automaticaly generated) from each tab,
		verrify its correctness, send the arguments to the tracer,
		and show the generated html.
		Future TO-DO: evaluate the corectness of the arguments before/instead of 
		calling the tracer and catching errors.
		"""
		#
		nrOfArgTabs = self.argumentsTabWidget.count()
		arguments = []
		# Read input from each tab and verify if it's valid:
		for i in range(nrOfArgTabs):
			tab = self.argumentsTabWidget.widget(i)
			if tab.findChild(QRadioButton, "manualInputRadioButton"+str(i)).isChecked():
				txt = str(tab.findChild(QLineEdit, "manualInputLineEdit"+str(i)).text())
				if txt != '':
					arguments.append(txt)
			elif tab.findChild(QRadioButton, "autoInputRadioButton"+str(i)).isChecked():
				genArguments = [tab.findChild(QSpinBox, arg).value() for arg in self.argsDict[i]]
				arg = self.argsType[i]
				genIns = self.availableGeneratorsModules[self.availableGenerators.index(arg)]()
				eval('apply(genIns.generateRandom'+arg+',genArguments)')
				arguments.append(str(genIns))
			else:
				return
		if len(arguments) != nrOfArgTabs:
			QMessageBox(QMessageBox.Warning, "Warning", "Not enough arguments").exec_()
			return
		# Create the string of arguments:
		args = ''.join([arg+',' for arg in arguments])[:-1]
		# Call the tracer on the arguments:
		try:
			html_filename = tracer.tracer(self.filename, self.funcname, args, plottype=self.tracePlotType)
			self.webView.setUrl(QUrl(html_filename))
		except StandardError as detail:
			box = QMessageBox(QMessageBox.Warning, "Warning", 
			  "Could not run code on the given arguments. Review the code and the arguments it takes. \
			  See <i>Show Details</i> for hints on the problem.")
			box.setDetailedText(str(detail))
			box.exec_()

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
			types = list(self.sections)
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
		file = open(path)
		lines = file.readlines()
		file.close()
		for line in lines:
			if line.strip().startswith('def '):
				functions.append(line.strip().split(None,1)[1].split(':')[0])
		return functions
		
	def getListOfFuncArgs(self):
		"""Return the list of available function arguments types (and thus generators)
		- needed for populating the list view of the new algorithm functionality
		- needed for generating random data
		Future TO-DO: verify if only one class
		"""
		availableGenerators = ['Int']
		availableGeneratorsArguments = ['']
		availableGeneratorsModules = [None]
		for filename in os.listdir(os.path.abspath(self.visPyDir)):
			if filename.endswith('.py'):
				file = open(os.path.join(self.visPyDir,filename),'r')
				lines = file.readlines()
				file.close()
				randomGeneratorLine = 'def generateRandom'+filename.split('.')[0].capitalize()
				codeRandomGeneratorLine = [line for line in lines if randomGeneratorLine in line]
				if codeRandomGeneratorLine != []:
					module = filename.split('.')[0]
					availableGenerators.append(module.capitalize())
					generatorArgumentsLine = codeRandomGeneratorLine[0].split('(')[1].split(')')[0].split(',')[1:]
					availableGeneratorsArguments.append(generatorArgumentsLine)
					generatorClass = module.capitalize()
					_temp = __import__(os.path.basename(self.visPyDir)+'.'+module, globals(), locals(), [generatorClass], -1)
					visClass = eval('_temp.'+generatorClass)
					availableGeneratorsModules.append(visClass)
		self.availableGenerators = availableGenerators
		self.availableGeneratorsArguments = availableGeneratorsArguments
		self.availableGeneratorsModules = availableGeneratorsModules
		return availableGenerators	#return ['List','Graph','Tree','Int']
		
	def selectNewAlgArgument(self, index):
		"""Store the selected argument type from the available list of 
		arguments and enable the 'add argument' button.
		"""
		self.newAlgAddArgButton.setEnabled(True)
		self.selectedArg = index.data().toString()
		
	def addNewAlgArgument(self):
		"""Add the currently selected argument type to the list of
		arguments for the new algorithm.
		Future TO-DO: after adding, the selection should be set to the new arg type
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
		self.selectedModifArgIndexModel = index
		
	def moveUpNewAlgArgument(self):
		"""Move one position up the selected argument type.
		Future TO-DO: after moving, the selection should remain on the moved arg type
		"""
		currList = self.newAlgArgsModel.stringList()
		if self.selectedModifArgIndex > 0:
			currList.swap(self.selectedModifArgIndex-1,self.selectedModifArgIndex)
			self.newAlgArgsListView2.model().setStringList(currList)
			self.newAlgArgOpGroupBox.setEnabled(False)
			self.selectedModifArgIndex = -1
	
	def moveDownNewAlgArgument(self):
		"""Move one position down the selected argument type.
		Future TO-DO: after moving, the selection should remain on the moved arg type
		"""
		currList = self.newAlgArgsModel.stringList()
		if -1 < self.selectedModifArgIndex < len(currList)-1:
			currList.swap(self.selectedModifArgIndex+1,self.selectedModifArgIndex)
			self.newAlgArgsListView2.model().setStringList(currList)
			self.newAlgArgOpGroupBox.setEnabled(False)
			self.selectedModifArgIndex = -1	
			
	def deleteNewAlgArgument(self):
		"""Delete the selected argument type.
		"""
		currList = self.newAlgArgsModel.stringList()
		if self.selectedModifArgIndex != -1:
			currList.takeAt(self.selectedModifArgIndex)
			self.newAlgArgsListView2.model().setStringList(currList)
			self.newAlgArgOpGroupBox.setEnabled(False)
			self.selectedModifArgIndex = -1	
		
	def addNewAlg(self):
		"""Add the new algorithm to the library of available algorithms 
		(if all required input is correct).
		Future TO-DO: If a filename already exists, append a counter at the end
		of the file instead of appending zeros.
		"""
		fileName = str(self.pathLineEdit.text())
		funcName = str(self.newAlgFuncComboBox.currentText()).split('(')[0]
		algName = str(self.newAlgNameLineEdit.text().trimmed())
		sectionName = str(self.newAlgTypeComboBox.currentText())
		arguments = [str(arg) for arg in self.newAlgArgsModel.stringList()]

		if algName != "" and len([i for i in range(len(self.algConf)) if algName in [self.algConf[i][1]]])==0:
			newPath = os.path.join(os.path.join(os.getcwd(),self.algDir),os.path.basename(fileName))
			while os.path.exists(newPath):
				newPath = newPath[:-3] + '0' + newPath[-3:]
			shutil.copyfile(fileName, newPath)
			self.algConf.append([sectionName,algName,os.path.basename(newPath),funcName,str(arguments)])
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
		QMessageBox.information(self, "About PyAlg",
			"""<b>PyAlg</b> v %s
			<p>An algorithms learning platform in Python.
			<p><a href="%s">PyAlg Web Site</a>
			<p>Copyright &copy; 2010. 
			Radu Dragusin, Paula Petcu.
			<p>Code License: 
			<a href="http://www.gnu.org/licenses/old-licenses/gpl-2.0.html">GNU General Public License v2</a>
			<p>Python %s -Qt %s -PyQt %s on %s"""
			% (__version__,website,python_version(),QT_VERSION_STR,PYQT_VERSION_STR,system()))
	
	def showHelpDialog(self):
		helpDialog = QDialog(self)
		verticalLayout = QVBoxLayout(helpDialog)
		helpWebView = QWebView(helpDialog)
		helpWebView.setUrl(QUrl(self.helpFile))
		verticalLayout.addWidget(helpWebView)
		helpDialog.exec_()
		pass
	
	def showNewAlgWindow(self):
		"""Open a pop-up window for adding a new algorithm to the existing library.
		"""
		self.newAlgDockWidget.show()

	def disableAlgEditing(self):
		"""Disable the algorithm editing buttons from the menu when no 
		algorithm is selected, and vice-versa.
		"""
		if self.algTree.currentItem().parent() is not None:
			self.renameAction.setEnabled(True)
			self.deleteAction.setEnabled(True)
			self.argumentsAction.setEnabled(True)
		else:
			self.renameAction.setEnabled(True)
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
					el = [i for i in range(len(self.algConf)) if currAlgName in [self.algConf[i][1]]][0]
					try:
						os.remove(os.path.join(os.path.join(os.getcwd(),self.algDir),self.algConf[el][2]))
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
		Can also rename sections (algorithm types).
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
				currAlgTypeName = str(self.algTree.currentItem().text(0))
				(newAlgTypeName,reply) = QInputDialog.getText(self,"Rename","New name:",
				  QLineEdit.Normal,currAlgTypeName)
				newAlgTypeName = newAlgTypeName.trimmed()
				if reply and newAlgTypeName != currAlgTypeName:
					if len([i for i in range(len(self.algConf)) if newAlgTypeName in [self.algConf[i][0]]])==0:
						for i in range(len(self.algConf)):
							if currAlgTypeName in [self.algConf[i][0]]:
								self.algConf[i][0] = newAlgTypeName
						self.saveAlgConf()
		else:
			QMessageBox(QMessageBox.Warning, "Warning", "No algorithm selected.").exec_()	
			
	def changeArgsAlgorithm(self):
		"""Edit the arguments list of the selected algorithm, if any.
		"""
		currItem = self.algTree.currentItem()
		if currItem:
			if currItem.childCount() == 0:
				currAlgName = str(self.algTree.currentItem().text(0))
				el = [i for i in range(len(self.algConf)) if currAlgName in [self.algConf[i][1]]][0]
				currAlgArgs = self.algConf[el][-1]
				(newAlgArgs,reply) = QInputDialog.getText(self,"Edit Arguments",
				  "New arguments list:",QLineEdit.Normal,currAlgArgs)
				if reply and newAlgArgs != currAlgArgs and self.isWellFormedArgumentList(newAlgArgs):
					self.algConf[el][-1] = newAlgArgs
					self.saveAlgConf()
				elif reply and newAlgArgs != currAlgArgs:
					QMessageBox(QMessageBox.Warning, "Warning", "List of arguments is not well formed.").exec_()
			else:
				QMessageBox(QMessageBox.Warning, "Warning", "Cannot add arguments to algorithm type.").exec_()
		else:
			QMessageBox(QMessageBox.Warning, "Warning", "No algorithm selected.").exec_()					
			
	def isWellFormedArgumentList(self,argsList):
		"""Verify if the list of arguments is well-formed (is a list of strings 
		representing existing data generators). Returns True or False. 
		"""
		try:
			alist = eval(str(argsList))
			if len([1 for el in alist if el in self.availableGenerators]) == len(alist):
				return True
			return False
		except:
			return False
				
	def setLinePlotType(self):
		self.tracePlotType = 'line'
	
	def setBarPlotType(self):
		self.tracePlotType = 'bar'
	
	def setFilledBarPlotType(self):
		self.tracePlotType = 'filledbar'
		
	def setManualInputType(self):
		self.inputType = 'manual'
		
	def setAutoInputType(self):
		self.inputType = 'auto'
		
	def setNrBenchmarkExecutions(self):
		"""Ask the user for and set the number of execution each algorithm selected in
		the benchmark wizard should execute. Number must be positive.
		"""
		(newNrBenchExec,reply) = QInputDialog.getInt(self,"Benchmark Wizard: Nr of executions",
		  "Number of times each algorithm in the\nbenchmark wizard will be executed:",self.nrBenchExec)
		if reply and self.nrBenchExec != newNrBenchExec:
			if newNrBenchExec > 0:
				self.nrBenchExec = newNrBenchExec
			else:
				QMessageBox(QMessageBox.Warning, "Warning", "Number must be positive").exec_()
				self.setNrBenchmarkExecutions()
	
	def enableSaveAction(self,ok):
		"""Enable/disable the save action from the menu based on the state of the webView 
		"""
		if self.webView.url() != QUrl('about:blank'):
			self.saveAction.setEnabled(True)
		else:
			self.saveAction.setEnabled(False)
	
	def saveHtml(self):
		"""Save the current html from the web view, together with the svg, css and js files.
		"""
		if self.webView.url() != QUrl('about:blank'):
			browsingStartPoint = os.getenv('USERPROFILE') or os.getenv('HOME')
			dirname = QFileDialog.getExistingDirectory(self, "Select Directory To Save In", 
			  browsingStartPoint, QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
			dirname = str(dirname)
			if dirname != "":
				file = os.path.normpath(str(self.webView.url().path()))
				try:
					shutil.copyfile(file, os.path.join(dirname, os.path.basename(file)))
					img = file.replace('.html','.svg')
					shutil.copyfile(img, os.path.join(dirname, os.path.basename(img)))
				except StandardError as detail:
					box = QMessageBox(QMessageBox.Warning, "Error", "Could not save file.")
					box.setDetailedText(str(detail))
					box.exec_()
					return
				for filename in os.listdir(os.path.dirname(file)):
					if filename.endswith('.js') or filename.endswith('.css'):
						shutil.copyfile(os.path.join(os.path.dirname(file),filename), 
						  os.path.join(dirname, filename))
				box = QMessageBox(QMessageBox.Information, "Success", "Successfully saved the output.").exec_()
	
	def showCompareWiz(self):
		"""Open and focus on the Compare Algorithms Wizard.
		"""
		wizard = PyAlgWizard(self)
		wizard.exec_()
		
	def openWebsite(self):
		"""Opens the project's wiki in a new browser window (uses
		default internet browser).
		"""
		openWB(website)
			
	def closeEvent(self, event):
		"""Called either when the Quit button or the X is pressed.
		"""
		event.accept()

				
if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	form = PyAlgMainWindow()
	form.show()
	app.exec_()
