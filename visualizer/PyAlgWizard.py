from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import QWebView

import os
import os.path
import shutil

import tracer
from compareTracer import CompareTracer
from compareTimer import CompareTimer
import wiz_pyalg

from vispy.list import list as visList

class PyAlgWizard(QWizard, wiz_pyalg.Ui_Wizard):
	def __init__(self,parent=None):
		"""Initializes the wizard and connects its events with its logic part.
		"""
		super(PyAlgWizard,self).__init__(parent)
		
		self.setupUi(self)
		self.parent = parent
		self.justStarted = True
		self.oldArguments = None
		self.rangeChanged = False
		
		self.connect(self, SIGNAL("currentIdChanged(int)"), self.updateWizPage)
		self.connect(self, SIGNAL("customButtonClicked(int)"), self.saveWizResults)
		self.connect(self.listFromSpinBox, SIGNAL("valueChanged(int)"), self.setListSizeRangeChanged)
		self.connect(self.listToSpinBox, SIGNAL("valueChanged(int)"), self.setListSizeRangeChanged)
		
	# NAVIGATION THROUGH THE WIZARD'S PAGES	
	
	def updateWizPage(self, id):
		"""Connect the page updating functionality with the pages, 
		based on the current page.
		Update only when parameters changed.
		TO-DO: add more data generators and interface for giving the args
		"""
		self.setOption(QWizard.HaveCustomButton1,False)
		self.setOption(QWizard.HaveCustomButton2,False)
		
		if id == 1 and self.justStarted:
			#Page 2 - Step 1
			self.updateWizAlgTree() 
			self.justStarted = False
		elif id == 2:
			#Page 3 - Step 2
			#TO-DO: create generator
			self.newArguments = str(self.parent.genList(11,0,20))
			self.argumentsLabel.setText(self.newArguments)
		elif id == 3:
			#Page 4 - Step 3
			self.setOption(QWizard.HaveCustomButton1)
			self.setButtonText(QWizard.CustomButton1, "Save All")
			if self.newArguments != self.oldArguments or \
			  self.prevSelectedAlgorithms != self.selectedAlgorithms:
				self.updateWizWebViews()
				self.oldArguments = self.newArguments
				self.prevSelectedAlgorithms = self.selectedAlgorithms
				self.algsChanged = True
		elif id == 4:
			#Page 5 - Step 4
			if self.algsChanged:
				self.updateWizLineSelection()
				self.algsChanged = False
				self.prevLineSelections = []
				self.prevRangeValues = ()
		elif id == 5:
			#Page 6 - Step 5
			#TO-DO: check if arguments changed for all types of arguments 
			#(currently supporting only modification of range for list arg)
			self.setOption(QWizard.HaveCustomButton2)
			self.setButtonText(QWizard.CustomButton2, "Save All")
			if self.prevLineSelections != self.lineSelections or self.rangeChanged:
				self.updateWizPerformance()
				
	
	def validateCurrentPage(self):
		"""Reimplementation of the validateCurrentPage(), verifies if all arguments
		are valid before going to the next page.
		The default implementation calls QtWizardPage::validatePage() on the currentPage().
		The default implementation of QtWizardPage::validatePage() returns true.
		"""
		id = self.currentId()
		if id == 1:
			#Step1: Verify that at least 2 algorithms were selected 
			if len(self.algTreeWiz.selectedItems()) >= 2:
				self.prevSelectedAlgorithms = self.selectedAlgorithms
				self.selectedAlgorithms = [str(el.text(0)) for el in self.algTreeWiz.selectedItems()]
			else:
				QMessageBox(QMessageBox.Warning, "Warning", 
				  "At least two algorithms must be selected.").exec_()
				return False
		elif id == 2:
			#Step2: TO-DO: Verify that the arguments are well-formed
			pass
		elif id == 3:
			pass			
		elif id == 4:
			#Step4: Verify that at least two algorithms have line selected.
			#TO-DO: verify that line number does exist in alg
			#TO-DO: connect selection of line in Javascript with this interface
			#TO-DO: figure out if it makes sense to 'compare' just one algorithm
			lineSelections = [(str(self.lineTableWidget.item(row,0).text()), 
			  str(self.lineTableWidget.item(row,1).text()).strip()) \
			  for row in range(self.lineTableWidget.rowCount()) \
			  if self.lineTableWidget.item(row,1) != None and \
			    str(self.lineTableWidget.item(row,1).text()).strip() != ""]
			if len(lineSelections) >= 2:
				if len(lineSelections) == len([1 for line in lineSelections if line[1].isdigit()]):
					self.lineSelections = lineSelections
				else:
					QMessageBox(QMessageBox.Warning, "Warning", 
					  "The Line column should only contain line numbers.").exec_()
					return False
			else:
				QMessageBox(QMessageBox.Warning, "Warning", 
				  "At least two algorithms must be selected for comparison.").exec_()
				return False
				
		return True
	
	def setListSizeRangeChanged(self):
		if self.prevRangeValues != (self.listFromSpinBox.value(), self.listToSpinBox.value()):
			self.rangeChanged = True
		else:
			self.rangeChanged = False
	
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
		
	def updateWizWebViews(self):
		"""Trace each of the selected algorithms with the given arguments and 
		show their analysis. Dynamically create tabs (with web views) for the algorithms.
		"""
		self.simpleAnalysisTabWidget.clear()
		html_files = []
		for algName in self.selectedAlgorithms:
			el = [i for i in range(len(self.algConf)) if algName in [self.algConf[i][1]]][0]
			filename, funcname = self.algConf[el][2], self.algConf[el][3]
			try:
				html_filename = tracer.tracer(filename, funcname, self.newArguments, nrselect=True, plottype = self.parent.tracePlotType)
				html_files.append(html_filename)
				tab = QWidget()
				verticalLayout = QVBoxLayout(tab)
				resultWebView = QWebView(tab)
				resultWebView.setUrl(QUrl(html_filename))
				verticalLayout.addWidget(resultWebView)
				self.simpleAnalysisTabWidget.addTab(tab,algName)
			except StandardError as detail:
				box = QMessageBox(QMessageBox.Warning, "Warning", 
				  "Invalid Code for "+algName+\
				  ". Review the code and upload it again. The Wizard will now close.")
				box.setDetailedText(str(detail))
				box.exec_()
				self.close()
				return
		self.html_files = html_files
				
	def updateWizLineSelection(self):
		""" Populate/Update the table containing the algorithms for which
		line selections can be made.
		"""
		self.lineTableWidget.clearContents()
		self.lineTableWidget.setRowCount(0)
		
		for algName in self.selectedAlgorithms:
			rows = self.lineTableWidget.rowCount()
			self.lineTableWidget.insertRow(rows)
			item = QTableWidgetItem(QString(algName))
			item.setFlags(Qt.ItemIsEnabled)
			self.lineTableWidget.setItem(rows,0,item)

	def updateWizPerformance(self):
		""" Create/Update the image corresponding to the performance 
		analysis of the selected algorithms, on their corresponding
		parameters (line selections, size ranges)
		TO-DO: Done for lists only. Do it for other arguments.
		"""
		self.imgfilename = "htmlfiles/algPerf.svg"
		self.imgfilename2 = "htmlfiles/algTime.svg"
		listSizes = (self.listFromSpinBox.value(), self.listToSpinBox.value())
		algnames = [sel[0] for sel in self.lineSelections]
		lines = [int(sel[1]) for sel in self.lineSelections]
		
		filenames, funcnames = [], []
		for algName in algnames:
			el = [i for i in range(len(self.algConf)) if algName in [self.algConf[i][1]]][0]
			filename, funcname = self.algConf[el][2], self.algConf[el][3]
			filenames.append(filename)
			funcnames.append(funcname)
		
		self.cmpTimer = CompareTimer(filenames, funcnames, listSizes, algnames, self.imgfilename2,1)
		self.timeResults = []
		self.cmpLines = CompareTracer(filenames, funcnames, listSizes, lines, algnames, self.imgfilename)
		self.lineResults = []
		self.pictureLineLabel.setPixmap(QPixmap())
		self.pictureTimeLabel.setPixmap(QPixmap())
		
		self.progressBar.setVisible(True)
		self.progressBar.setRange(0,listSizes[1]-listSizes[0])
		self.progressBar.setFormat('%v out of %m done')
		for i,listSize in enumerate(range(listSizes[0],listSizes[1])):
			if self.isHidden() == False and self.currentId() == 5:
				self.cmpLinesAndTime(listSize)
				self.progressBar.setValue(i)
				QApplication.processEvents()
			else:
				break
		
		try:
			self.progressBar.setRange(0,2)
			self.progressBar.setFormat('Generating benchmark suite')
			self.progressBar.setValue(0)
			QApplication.processEvents()
			if self.isHidden() == False and self.currentId() == 5:
				self.cmpLines.createGraph(self.lineResults)
				pic = QPixmap(self.imgfilename)
				self.pictureLineLabel.setPixmap(pic)
				
				self.progressBar.setValue(1)
				QApplication.processEvents()

			if self.isHidden() == False and self.currentId() == 5:
				self.cmpTimer.createGraph(self.timeResults)
				pic = QPixmap(self.imgfilename2)
				self.pictureTimeLabel.setPixmap(pic)
				
				self.progressBar.setValue(2)
				QApplication.processEvents()
				
				self.prevLineSelections = self.lineSelections
				self.prevRangeValues = (self.listFromSpinBox.value(), self.listToSpinBox.value())
				self.rangeChanged = False
			
			self.progressBar.setVisible(False)

		except StandardError as detail:
			box = QMessageBox(QMessageBox.Warning, "Warning", "Could not draw performance graph.")
			box.setDetailedText(str(detail))
			box.exec_()
			self.back()

			
	def cmpLinesAndTime(self,listSize):
		list = visList()
		list.genRandomList(listSize)
		self.timeResults = self.timeResults + self.cmpTimer.getTimes(list)
		self.lineResults = self.lineResults + self.cmpLines.getPerf(list)

	# SAVE THE RESULTS OBTAINED THROUGH THE WIZARD
	
	def saveWizResults(self, buttonId):
		"""Save the results obtained through the wizz, either from the simple
		or the complex analysis.
		QWizard::CustomButton1	Value: 6  Save simple analysis results
		QWizard::CustomButton2	Value: 7  Save complex analysis results
		"""
		if buttonId == 6 or buttonId == 7:
			browsingStartPoint = os.getenv('USERPROFILE') or os.getenv('HOME')
			dirname = QFileDialog.getExistingDirectory(self, "Select Directory To Save In", 
			  browsingStartPoint, QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
			dirname = str(dirname)
			if dirname != "":
				if buttonId == 6:
					files = [os.path.abspath(file) for file in self.html_files]
					for file in files:
						try:
							shutil.copyfile(file, os.path.join(dirname, os.path.basename(file)))
							img = file.replace('.html','.svg')
							shutil.copyfile(img, os.path.join(dirname, os.path.basename(img)))
						except StandardError as detail:
							box = QMessageBox(QMessageBox.Warning, "Error", "Could not save files.")
							box.setDetailedText(str(detail))
							box.exec_()
							return
					for filename in os.listdir(os.path.dirname(file)):
						if filename.endswith('.js') or filename.endswith('.css'):
							shutil.copyfile(os.path.join(os.path.dirname(file),filename), 
							  os.path.join(dirname, filename))
					box = QMessageBox(QMessageBox.Information, "Success", "Successfully saved files.").exec_()
				else:
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
