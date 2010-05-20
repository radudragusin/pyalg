from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import QWebView

import os
import os.path
import shutil
import sys

import tracer
from compareTracer import CompareTracer
from compareTimer import CompareTimer
import wiz_pyalg

class PyAlgWizard(QWizard, wiz_pyalg.Ui_Wizard):
	def __init__(self,parent=None):
		"""Initializes the wizard and connects its events with its logic part.
		"""
		super(PyAlgWizard,self).__init__(parent)
		
		self.setupUi(self)
		self.parent = parent
		self.justStarted = True
		self.rangeValuesChanged = False
		
		self.imgfilename = "htmlfiles/algPerf.svg"
		self.imgfilename2 = "htmlfiles/algTime.svg"
		
		self.connect(self, SIGNAL("currentIdChanged(int)"), self.updateWizPage)
		self.connect(self, SIGNAL("customButtonClicked(int)"), self.saveWizResults)
		self.connect(self.rangeFromSpinBox, SIGNAL("valueChanged(int)"), self.setRangeValuesChanged)
		self.connect(self.rangeToSpinBox, SIGNAL("valueChanged(int)"), self.setRangeValuesChanged)
		self.connect(self.rangeElemComboBox, SIGNAL("currentIndexChanged(int)"), self.disableRangeElemValueEditing)
		
	# NAVIGATION THROUGH THE WIZARD'S PAGES	
	
	def updateWizPage(self, id):
		"""Connect the page updating functionality with the pages, 
		based on the current page.
		Update only when parameters changed.
		"""
		self.setOption(QWizard.HaveCustomButton1,False)
		
		if id == 1 and self.justStarted:
			#Page 2 - Step 1
			self.updateWizAlgTree() 
			self.justStarted = False
			self.outputSaved = False
		elif id == 2:
			#Page 3 - Step 2
			if self.prevSelectedAlgorithms != self.selectedAlgorithms:
				self.updateWizTableViews()
				self.prevSelectedAlgorithms = self.selectedAlgorithms
				self.algsChanged = True
				self.prevLineSelections = []
		elif id == 3:
			#Page 4 - Step 3
			#TO-DO: update only when necessary
			self.updateRangeAndValues()
		elif id == 4:
			#Page 5 - Step 4 (Final Step)
			#TO-DO: check if arguments changed for all types of arguments 
			#(currently supporting only modification of range for list arg)
			self.setOption(QWizard.HaveCustomButton1)
			self.setButtonText(QWizard.CustomButton1, "Save All")
			if self.algsChanged or self.rangeValuesChanged or self.prevLineSelections != self.lineSelections:
				self.updateWizPerformance()
				self.algsChanged = False
	
	def validateCurrentPage(self):
		"""Reimplementation of the validateCurrentPage(), verifies if all arguments
		are valid before going to the next page.
		The default implementation calls QtWizardPage::validatePage() on the currentPage().
		The default implementation of QtWizardPage::validatePage() returns true.
		"""
		id = self.currentId()
		if id == 1:
			# Step1: Verify that at least one algorithm was selected and that the
			#selected algorithms are compatible.
			selectedItems = self.algTreeWiz.selectedItems()
			if len(selectedItems) >= 1:
				if len(selectedItems) == 1 or self.areCompatibleAlgorithms(selectedItems):
					self.prevSelectedAlgorithms = self.selectedAlgorithms
					self.selectedAlgorithms = [str(el.text(0)) for el in selectedItems]
					if len(selectedItems) == 1:
						algArgs = [self.algConf[algIndex][4] for algIndex in range(len(self.algConf))\
						  if self.selectedAlgorithms[0] in [self.algConf[algIndex][1]]][0]
						self.algorithmsArguments = eval(algArgs)
				else:
					QMessageBox(QMessageBox.Warning, "Warning", 
					  "The algorithms you select must have the same type of arguments, given in the same order.")\
					  .exec_()
					return False
			else:
				QMessageBox(QMessageBox.Warning, "Warning", 
				  "At least one algorithm must be selected.").exec_()
				return False
		elif id == 2:
			# Step 2: Verify that the line selections are valid
			lineSelections = []
			for i in range(len(self.lineSelectionsTableViews)):
				tableView = self.lineSelectionsTableViews[i]
				algName = self.selectedAlgorithms[i]
				lineSelections.append((algName,[index.row()+1 for index in tableView.selectedIndexes()]))
			if len([1 for s in lineSelections if s[1]!=[] ]) == len(lineSelections):
				self.lineSelections = lineSelections
			else:
				QMessageBox(QMessageBox.Warning, "Warning", 
				  "All algorithms selected for comparison must have at least one line selected.").exec_()
				return False
		elif id == 3:
			#Verify that all arguments have int values (exception makes the range argument)
			if not self.areAllArgumentValuesGiven():
				QMessageBox(QMessageBox.Warning, "Warning", 
				  "All fixed arguments must have an integer value.").exec_()
				return False
		elif id == 4:
			# Final Step: Ask user to save the results, if he did not already do so.
			if self.outputSaved == False:
				reply = QMessageBox.question(self, "Reminder","You did not save the results. "+
				"You can save the images by clicking on the <i>Save All</i> button in the last page "+
				"of the wizard.\nWould you like to return to the wizard?",
				QMessageBox.Yes, QMessageBox.No)
				if reply == QMessageBox.Yes:
					return False
		return True
	
	def areCompatibleAlgorithms(self, selectedItems):
		"""The algorithms are compatible if they support the same types of 
		arguments and are given in the same order.
		"""
		selectedAlgorithmsNames = [str(el.text(0)) for el in selectedItems]
		
		algName = selectedAlgorithmsNames[0]
		prevAlgArgs = [self.algConf[algIndex][4] for algIndex in range(len(self.algConf))\
		  if algName in [self.algConf[algIndex][1]]][0]
		
		for i in range(1,len(selectedAlgorithmsNames)):
			algName = selectedAlgorithmsNames[i]
			algArgs = [self.algConf[algIndex][4] for algIndex in range(len(self.algConf))\
			  if algName in [self.algConf[algIndex][1]]][0]
			if algArgs != prevAlgArgs:
				return False
			prevAlgArgs = algArgs
		
		self.algorithmsArguments = eval(algArgs)
		return True
		
	def areAllArgumentValuesGiven(self):
		"""Return True/False depending on whether all arguments have or do not have 
		corresponding values. The exception is the selected range argument, which 
		of course does not need a fixed value.
		"""
		rangeArgumentIndex = self.rangeElemComboBox.currentIndex()
		valuesFromTableWidget = [str(self.valuesTableWidget.item(row,1).text()).strip() \
		  for row in range(self.valuesTableWidget.rowCount())\
		  if row != rangeArgumentIndex]
		if '' not in valuesFromTableWidget:
			try:
				[int(val) for val in valuesFromTableWidget]
				return True
			except:
				pass
		return False
	
	def setRangeValuesChanged(self):
		"""Set on True the value of rangeValuesChanged if the values from
		the spin boxes are different from the previous values. Called 
		when a change was made in one of the spinboxes.
		"""
		if self.prevRangeValues != (self.rangeFromSpinBox.value(), self.rangeToSpinBox.value()):
			self.rangeValuesChanged = True
		else:
			self.rangeValuesChanged = False
	
	def disableRangeElemValueEditing(self):
		"""TO-DO: Disable editing for the argument selected as range for the 
		performance analysis.
		"""
		#if self.prevDisabledTableItemIndex != -1:
			#self.valuesTableWidget.item(self.prevDisabledTableItemIndex,1).setFlags(Qt.ItemIsTristate)
		#self.valuesTableWidget.item(self.rangeElemComboBox.currentIndex(),1).setFlags(Qt.ItemIsEnabled)
		#self.prevDisabledTableItemIndex = self.rangeElemComboBox.currentIndex()
		return
	
	# UPDATE INFORMATION IN THE PAGES
	
	def updateWizAlgTree(self):
		""" Populate/Update the algorithms tree view from the wizard.
		"""
		self.algConf = self.parent.algConf
		self.algTreeWiz.clear()
		
		parents = set([self.algConf[i][0] for i in range(len(self.algConf))])
		for parent in parents:
			algTypeItem = QTreeWidgetItem(None, QStringList(parent))
			self.algTreeWiz.addTopLevelItem(algTypeItem)
			self.algTreeWiz.expandItem(algTypeItem)
			algTypeItem.setFlags(Qt.ItemIsEnabled)
			algTypeWidget = QTreeWidget(self.algTreeWiz.itemWidget(algTypeItem,1))
			
			for i in range(len(self.algConf)):
				if self.algConf[i][0] == parent:
					children  = self.algConf[i][1]
					algTypeWidget.addTopLevelItem(QTreeWidgetItem(algTypeItem, QStringList(children)))
					
		self.selectedAlgorithms = []
		
	def updateWizTableViews(self):
		"""Dynamically create tabs (with table views) for the algorithms and allow line selections.
		"""
		self.simpleAnalysisTabWidget.clear()
		self.lineSelectionsTableViews = []
		html_files = []
		for algName in self.selectedAlgorithms:
			el = [i for i in range(len(self.algConf)) if algName in [self.algConf[i][1]]][0]
			filename = self.algConf[el][2]
			tab = QWidget()
			verticalLayout = QVBoxLayout(tab)
			resultTableView = QTableView(tab)
			file = open(os.path.join(self.parent.algDir,filename),'r')
			lines = file.readlines()
			file.close()
			lines = [line.rstrip() for line in lines]
			resultTableView.setModel(QStringListModel(QStringList(lines)))
			resultTableView.setShowGrid(False)
			resultTableView.setSelectionMode(QAbstractItemView.ExtendedSelection)
			resultTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
			resultTableView.horizontalHeader().setStretchLastSection(True)
			resultTableView.horizontalHeader().setVisible(False)
			verticalLayout.addWidget(resultTableView)
			self.simpleAnalysisTabWidget.addTab(tab,algName)
			self.lineSelectionsTableViews.append(resultTableView)
		self.html_files = html_files

	def updateRangeAndValues(self):
		"""Update the list of available arguments that can be selected
		for the performance analysis.
		"""
		self.rangeElemComboBox.clear()
		self.valuesTableWidget.clearContents()
		self.valuesTableWidget.setRowCount(0)
		self.prevDisabledTableItemIndex = -1
		self.algArgs = []
		
		argNames = self.algorithmsArguments
		possibleRangeElementsStringList = []
		for i,argName in enumerate(argNames):
			if argName != 'Int':
				genLine = self.parent.availableGeneratorsArguments[self.parent.availableGenerators.index(argName)]
				for j,el in enumerate(genLine):
					elName = el.strip()
					if '=' in elName:
						elName, elDefaultValue = elName.split('=')
						elName, elDefaultValue = elName.strip(), elDefaultValue.strip()
					name = '(Arg '+str(i+1)+': '+argName+') '+elName
					possibleRangeElementsStringList.append(name)
					self.addRowWithNameValue(name,elDefaultValue)
					self.algArgs.append([i,argName,elName])
			else:
				name = '(Arg '+str(i+1)+': '+argName+') '+'value'
				possibleRangeElementsStringList.append(name)
				self.addRowWithNameValue(name,'')
				self.algArgs.append([i,argName,'value'])
				
		self.rangeElemComboBox.addItems(QStringList(possibleRangeElementsStringList))
		return
	
	def addRowWithNameValue(self,name,value):
		"""Add a row in the valuesTableWidget (containing the fixed values for
		the algorithms) with 2 columns: name and default value.
		"""
		rows = self.valuesTableWidget.rowCount()
		self.valuesTableWidget.insertRow(rows)
		item = QTableWidgetItem(QString(name))
		item.setFlags(Qt.ItemIsEnabled)
		self.valuesTableWidget.setItem(rows,0,item)
		self.valuesTableWidget.setItem(rows,1, QTableWidgetItem(QString(value)))

	def updateWizPerformance(self):
		""" Create/Update the image corresponding to the performance 
		analysis of the selected algorithms, on their corresponding
		parameters (line selections, size ranges)
		"""
		rangeBoundaries = (self.rangeFromSpinBox.value(), self.rangeToSpinBox.value())
		algnames = [linesel[0] for linesel in self.lineSelections]
		lines = [[int(sel) for sel in linesel[1]] for linesel in self.lineSelections]
		
		rangeArgumentIndex = self.rangeElemComboBox.currentIndex()
		self.rangeArgumentType = self.algArgs[rangeArgumentIndex][1]
		self.rangeArgumentTypeIndex = self.algArgs[rangeArgumentIndex][0]
		self.valuesFromTableWidget = [str(self.valuesTableWidget.item(row,1).text()) for row in range(self.valuesTableWidget.rowCount())]
		self.generateNonRangeArguments()
		
		filenames, funcnames = [], []
		for algName in algnames:
			el = [i for i in range(len(self.algConf)) if algName in [self.algConf[i][1]]][0]
			filename, funcname = self.algConf[el][2], self.algConf[el][3]
			filenames.append(filename)
			funcnames.append(funcname)
		
		self.cmpLines = CompareTracer(filenames, funcnames, rangeBoundaries, lines, algnames, self.imgfilename)
		self.lineResults = []
		self.cmpTimer = CompareTimer(filenames, funcnames, rangeBoundaries, algnames, self.imgfilename2,self.parent.nrBenchExec)
		self.timeResults = []
		self.pictureLineLabel.setPixmap(QPixmap())
		self.pictureTimeLabel.setPixmap(QPixmap())
		self.progressBar.setVisible(True)
		self.progressBar.setRange(0,rangeBoundaries[1]-rangeBoundaries[0])
		self.progressBar.setFormat('%v out of %m done')
		for i,currentValue in enumerate(range(rangeBoundaries[0],rangeBoundaries[1])):
			if self.isHidden() == False and self.currentId() == 4:
				self.valuesFromTableWidget[rangeArgumentIndex] = currentValue
				self.cmpLinesAndTime(currentValue)
				self.progressBar.setValue(i)
				QApplication.processEvents()
			else:
				break
		
		try:
			self.progressBar.setRange(0,2)
			self.progressBar.setFormat('Generating benchmark suite')
			self.progressBar.setValue(0)
			QApplication.processEvents()
			if self.isHidden() == False and self.currentId() == 4:
				self.cmpLines.createGraph(self.lineResults)
				pic = QPixmap(self.imgfilename)
				self.pictureLineLabel.setPixmap(pic)
				
				self.progressBar.setValue(1)
				QApplication.processEvents()

			if self.isHidden() == False and self.currentId() == 4:
				self.cmpTimer.createGraph(self.timeResults)
				pic = QPixmap(self.imgfilename2)
				self.pictureTimeLabel.setPixmap(pic)
				
				self.progressBar.setValue(2)
				QApplication.processEvents()
				
				self.prevLineSelections = self.lineSelections
				self.prevRangeValues = (self.rangeFromSpinBox.value(), self.rangeToSpinBox.value())
				self.rangeValuesChanged = False
			
			self.progressBar.setVisible(False)

		except StandardError as detail:
			box = QMessageBox(QMessageBox.Warning, "Warning", "Could not draw performance graph.")
			box.setDetailedText(str(detail))
			box.exec_()
			self.back()

	def cmpLinesAndTime(self,paramValue):
		"""Generate data for the current value of the changing parameter, 
		and call the modules for performance analysis for that data. Save 
		the results.
		Used by updateWizPerformance.
		"""
		if self.rangeArgumentType!='Int':
			genArguments = [int(self.valuesFromTableWidget[i]) for i,arg in enumerate(self.algArgs) if arg[0] == self.rangeArgumentTypeIndex]
			genIns = self.parent.availableGeneratorsModules[self.parent.availableGenerators.index(self.rangeArgumentType)]()
			eval('apply(genIns.generateRandom'+self.rangeArgumentType+',genArguments)')
		else:
			genIns = paramValue
		
		print self.nonRangeArgs
		
		self.nonRangeArgs.insert(self.rangeArgumentTypeIndex,str(genIns))
		args = ''.join([arg+',' for arg in self.nonRangeArgs])[:-1]
		self.nonRangeArgs.pop(self.rangeArgumentTypeIndex)

		print args
		
		self.timeResults = self.timeResults + self.cmpTimer.getTimes(args)
		self.lineResults = self.lineResults + self.cmpLines.getPerf(args)

	def generateNonRangeArguments(self):
		#TO-DO!!!: duplicate arguments when generating non range lists: produces 3 lists instead of one
		# because there are 3 arguments for the list. Need to fix this soon as posible.
		self.nonRangeArgs = []
		for i,arg in enumerate(self.algArgs):
			if arg[0] != self.rangeArgumentTypeIndex:
				if arg[1] != 'Int':
					genArguments = [int(self.valuesFromTableWidget[i]) for i,a in enumerate(self.algArgs) if a[0] == arg[0]]
					argumentType = arg[1]
					genIns = self.parent.availableGeneratorsModules[self.parent.availableGenerators.index(argumentType)]()
					eval('apply(genIns.generateRandom'+argumentType+',genArguments)')
					self.nonRangeArgs.append(str(genIns))
				elif arg[1] == 'Int':
					self.nonRangeArgs.append(str(int(self.valuesFromTableWidget[i])))

	# SAVE THE RESULTS OBTAINED THROUGH THE WIZARD
	
	def saveWizResults(self, buttonId):
		"""Save the performance results obtained through the wizz.
		QWizard::CustomButton1	Value: 6  Save performance results
		"""
		if buttonId == 6:
			browsingStartPoint = os.getenv('USERPROFILE') or os.getenv('HOME')
			dirname = QFileDialog.getExistingDirectory(self, "Select Directory To Save In", 
			  browsingStartPoint, QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
			dirname = str(dirname)
			if dirname != "":
				try:
					shutil.copyfile(os.path.abspath(self.imgfilename), 
					  os.path.join(dirname, os.path.basename(self.imgfilename)))
					shutil.copyfile(os.path.abspath(self.imgfilename2), 
					  os.path.join(dirname, os.path.basename(self.imgfilename2)))
				except StandardError as detail:
					box = QMessageBox(QMessageBox.Warning, "Error", "Could not save files.")
					box.setDetailedText(str(detail))
					box.exec_()
					return
				box = QMessageBox(QMessageBox.Information, "Success", "Successfully saved files.").exec_()
				self.outputSaved = True
