# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PyAlgGuiWiz.ui'
#
# Created: Wed May 19 18:56:32 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Wizard(object):
    def setupUi(self, Wizard):
        Wizard.setObjectName("Wizard")
        Wizard.resize(420, 478)
        Wizard.setMinimumSize(QtCore.QSize(420, 478))
        self.wizardPage1 = QtGui.QWizardPage()
        self.wizardPage1.setObjectName("wizardPage1")
        self.page1Label = QtGui.QLabel(self.wizardPage1)
        self.page1Label.setGeometry(QtCore.QRect(120, 10, 281, 221))
        self.page1Label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.page1Label.setWordWrap(True)
        self.page1Label.setObjectName("page1Label")
        Wizard.addPage(self.wizardPage1)
        self.wizardPage2 = QtGui.QWizardPage()
        self.wizardPage2.setObjectName("wizardPage2")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.wizardPage2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.page2Label = QtGui.QLabel(self.wizardPage2)
        self.page2Label.setWordWrap(True)
        self.page2Label.setObjectName("page2Label")
        self.verticalLayout_3.addWidget(self.page2Label)
        self.algTreeWiz = QtGui.QTreeWidget(self.wizardPage2)
        self.algTreeWiz.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.algTreeWiz.setObjectName("algTreeWiz")
        item_0 = QtGui.QTreeWidgetItem(self.algTreeWiz)
        item_0 = QtGui.QTreeWidgetItem(self.algTreeWiz)
        item_0 = QtGui.QTreeWidgetItem(self.algTreeWiz)
        self.algTreeWiz.header().setVisible(False)
        self.verticalLayout_3.addWidget(self.algTreeWiz)
        Wizard.addPage(self.wizardPage2)
        self.wizardPage3 = QtGui.QWizardPage()
        self.wizardPage3.setObjectName("wizardPage3")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.wizardPage3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.page3Label = QtGui.QLabel(self.wizardPage3)
        self.page3Label.setWordWrap(True)
        self.page3Label.setObjectName("page3Label")
        self.verticalLayout_2.addWidget(self.page3Label)
        self.frameWizardPage3 = QtGui.QFrame(self.wizardPage3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameWizardPage3.sizePolicy().hasHeightForWidth())
        self.frameWizardPage3.setSizePolicy(sizePolicy)
        self.frameWizardPage3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frameWizardPage3.setFrameShadow(QtGui.QFrame.Raised)
        self.frameWizardPage3.setObjectName("frameWizardPage3")
        self.horizontalLayout = QtGui.QHBoxLayout(self.frameWizardPage3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.simpleAnalysisTabWidget = QtGui.QTabWidget(self.frameWizardPage3)
        self.simpleAnalysisTabWidget.setObjectName("simpleAnalysisTabWidget")
        self.tab1 = QtGui.QWidget()
        self.tab1.setObjectName("tab1")
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.tab1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.resultWebView1 = QtWebKit.QWebView(self.tab1)
        self.resultWebView1.setUrl(QtCore.QUrl("about:blank"))
        self.resultWebView1.setObjectName("resultWebView1")
        self.horizontalLayout_4.addWidget(self.resultWebView1)
        self.simpleAnalysisTabWidget.addTab(self.tab1, "")
        self.tab2 = QtGui.QWidget()
        self.tab2.setObjectName("tab2")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tab2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.resultWebView2 = QtWebKit.QWebView(self.tab2)
        self.resultWebView2.setUrl(QtCore.QUrl("about:blank"))
        self.resultWebView2.setObjectName("resultWebView2")
        self.verticalLayout_5.addWidget(self.resultWebView2)
        self.simpleAnalysisTabWidget.addTab(self.tab2, "")
        self.horizontalLayout.addWidget(self.simpleAnalysisTabWidget)
        self.verticalLayout_2.addWidget(self.frameWizardPage3)
        Wizard.addPage(self.wizardPage3)
        self.wizardPage4 = QtGui.QWizardPage()
        self.wizardPage4.setObjectName("wizardPage4")
        self.verticalLayout = QtGui.QVBoxLayout(self.wizardPage4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.page4Label = QtGui.QLabel(self.wizardPage4)
        self.page4Label.setWordWrap(True)
        self.page4Label.setObjectName("page4Label")
        self.verticalLayout.addWidget(self.page4Label)
        self.listGroupBox = QtGui.QGroupBox(self.wizardPage4)
        self.listGroupBox.setAutoFillBackground(False)
        self.listGroupBox.setFlat(False)
        self.listGroupBox.setObjectName("listGroupBox")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.listGroupBox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame_3 = QtGui.QFrame(self.listGroupBox)
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout = QtGui.QGridLayout(self.frame_3)
        self.gridLayout.setObjectName("gridLayout")
        self.listSizeLabel = QtGui.QLabel(self.frame_3)
        self.listSizeLabel.setObjectName("listSizeLabel")
        self.gridLayout.addWidget(self.listSizeLabel, 0, 0, 2, 1)
        self.listFromSpinBox = QtGui.QSpinBox(self.frame_3)
        self.listFromSpinBox.setMinimum(2)
        self.listFromSpinBox.setMaximum(1000)
        self.listFromSpinBox.setProperty("value", 10)
        self.listFromSpinBox.setObjectName("listFromSpinBox")
        self.gridLayout.addWidget(self.listFromSpinBox, 1, 2, 1, 1)
        self.listToLabel = QtGui.QLabel(self.frame_3)
        self.listToLabel.setObjectName("listToLabel")
        self.gridLayout.addWidget(self.listToLabel, 1, 3, 1, 1)
        self.listToSpinBox = QtGui.QSpinBox(self.frame_3)
        self.listToSpinBox.setMinimum(2)
        self.listToSpinBox.setMaximum(1000)
        self.listToSpinBox.setProperty("value", 100)
        self.listToSpinBox.setObjectName("listToSpinBox")
        self.gridLayout.addWidget(self.listToSpinBox, 1, 4, 1, 1)
        self.listFromLabel = QtGui.QLabel(self.frame_3)
        self.listFromLabel.setObjectName("listFromLabel")
        self.gridLayout.addWidget(self.listFromLabel, 1, 1, 1, 1)
        self.horizontalLayout_3.addWidget(self.frame_3)
        self.verticalLayout.addWidget(self.listGroupBox)
        Wizard.addPage(self.wizardPage4)
        self.wizardPage5 = QtGui.QWizardPage()
        self.wizardPage5.setObjectName("wizardPage5")
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.wizardPage5)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.page5Label = QtGui.QLabel(self.wizardPage5)
        self.page5Label.setWordWrap(True)
        self.page5Label.setObjectName("page5Label")
        self.verticalLayout_7.addWidget(self.page5Label)
        self.frame_4 = QtGui.QFrame(self.wizardPage5)
        self.frame_4.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.frame_4)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.perfTabWidget = QtGui.QTabWidget(self.frame_4)
        self.perfTabWidget.setObjectName("perfTabWidget")
        self.lineTab = QtGui.QWidget()
        self.lineTab.setObjectName("lineTab")
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.lineTab)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.pictureLineLabel = QtGui.QLabel(self.lineTab)
        self.pictureLineLabel.setTextFormat(QtCore.Qt.AutoText)
        self.pictureLineLabel.setScaledContents(True)
        self.pictureLineLabel.setWordWrap(True)
        self.pictureLineLabel.setObjectName("pictureLineLabel")
        self.verticalLayout_8.addWidget(self.pictureLineLabel)
        self.perfTabWidget.addTab(self.lineTab, "")
        self.timeTab = QtGui.QWidget()
        self.timeTab.setObjectName("timeTab")
        self.verticalLayout_9 = QtGui.QVBoxLayout(self.timeTab)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.pictureTimeLabel = QtGui.QLabel(self.timeTab)
        self.pictureTimeLabel.setScaledContents(True)
        self.pictureTimeLabel.setWordWrap(True)
        self.pictureTimeLabel.setObjectName("pictureTimeLabel")
        self.verticalLayout_9.addWidget(self.pictureTimeLabel)
        self.perfTabWidget.addTab(self.timeTab, "")
        self.horizontalLayout_5.addWidget(self.perfTabWidget)
        self.verticalLayout_7.addWidget(self.frame_4)
        self.progressBar = QtGui.QProgressBar(self.wizardPage5)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_7.addWidget(self.progressBar)
        Wizard.addPage(self.wizardPage5)

        self.retranslateUi(Wizard)
        self.simpleAnalysisTabWidget.setCurrentIndex(1)
        self.perfTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Wizard)

    def retranslateUi(self, Wizard):
        Wizard.setWindowTitle(QtGui.QApplication.translate("Wizard", "PyAlgLib Benchmarking Wizard", None, QtGui.QApplication.UnicodeUTF8))
        self.page1Label.setText(QtGui.QApplication.translate("Wizard", "Welcome to the PyAlgLib\n"
"Benchmarking Wizard.\n"
"\n"
"This wizard helps you compare between the algorithms available in the Algorithm Library. \n"
"\n"
"\n"
"\n"
"To continue, click Next.", None, QtGui.QApplication.UnicodeUTF8))
        self.wizardPage2.setTitle(QtGui.QApplication.translate("Wizard", "Step 1:", None, QtGui.QApplication.UnicodeUTF8))
        self.wizardPage2.setSubTitle(QtGui.QApplication.translate("Wizard", "Selection of the algorithms", None, QtGui.QApplication.UnicodeUTF8))
        self.page2Label.setText(QtGui.QApplication.translate("Wizard", "Select the algorithms you would like to compare:", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.algTreeWiz.isSortingEnabled()
        self.algTreeWiz.setSortingEnabled(False)
        self.algTreeWiz.topLevelItem(0).setText(0, QtGui.QApplication.translate("Wizard", "Insertion Sort", None, QtGui.QApplication.UnicodeUTF8))
        self.algTreeWiz.topLevelItem(1).setText(0, QtGui.QApplication.translate("Wizard", "Quick Sort", None, QtGui.QApplication.UnicodeUTF8))
        self.algTreeWiz.topLevelItem(2).setText(0, QtGui.QApplication.translate("Wizard", "Merge Sort", None, QtGui.QApplication.UnicodeUTF8))
        self.algTreeWiz.setSortingEnabled(__sortingEnabled)
        self.wizardPage3.setTitle(QtGui.QApplication.translate("Wizard", "Step 2:", None, QtGui.QApplication.UnicodeUTF8))
        self.wizardPage3.setSubTitle(QtGui.QApplication.translate("Wizard", "Benchmarking - Options (1 of 2)", None, QtGui.QApplication.UnicodeUTF8))
        self.page3Label.setText(QtGui.QApplication.translate("Wizard", "Select the lines from each algorithm on which you would like to make the comparison. Select at least one line per algorithm.", None, QtGui.QApplication.UnicodeUTF8))
        self.simpleAnalysisTabWidget.setTabText(self.simpleAnalysisTabWidget.indexOf(self.tab1), QtGui.QApplication.translate("Wizard", "Tab 1", None, QtGui.QApplication.UnicodeUTF8))
        self.simpleAnalysisTabWidget.setTabText(self.simpleAnalysisTabWidget.indexOf(self.tab2), QtGui.QApplication.translate("Wizard", "Tab 2", None, QtGui.QApplication.UnicodeUTF8))
        self.wizardPage4.setTitle(QtGui.QApplication.translate("Wizard", "Step 3:", None, QtGui.QApplication.UnicodeUTF8))
        self.wizardPage4.setSubTitle(QtGui.QApplication.translate("Wizard", "Benchmarking - Options (2 of 2)", None, QtGui.QApplication.UnicodeUTF8))
        self.page4Label.setText(QtGui.QApplication.translate("Wizard", "Select a range to apply the algorithms on:", None, QtGui.QApplication.UnicodeUTF8))
        self.listGroupBox.setTitle(QtGui.QApplication.translate("Wizard", "Assuming input argument is a list:", None, QtGui.QApplication.UnicodeUTF8))
        self.listSizeLabel.setText(QtGui.QApplication.translate("Wizard", "List size", None, QtGui.QApplication.UnicodeUTF8))
        self.listToLabel.setText(QtGui.QApplication.translate("Wizard", "To:", None, QtGui.QApplication.UnicodeUTF8))
        self.listFromLabel.setText(QtGui.QApplication.translate("Wizard", "From:", None, QtGui.QApplication.UnicodeUTF8))
        self.wizardPage5.setTitle(QtGui.QApplication.translate("Wizard", "Step 4:", None, QtGui.QApplication.UnicodeUTF8))
        self.wizardPage5.setSubTitle(QtGui.QApplication.translate("Wizard", "Benchmark results", None, QtGui.QApplication.UnicodeUTF8))
        self.page5Label.setText(QtGui.QApplication.translate("Wizard", "Results obtained by running the algorithms with the data provided in the previous steps:", None, QtGui.QApplication.UnicodeUTF8))
        self.perfTabWidget.setTabText(self.perfTabWidget.indexOf(self.lineTab), QtGui.QApplication.translate("Wizard", "Line Count", None, QtGui.QApplication.UnicodeUTF8))
        self.perfTabWidget.setTabText(self.perfTabWidget.indexOf(self.timeTab), QtGui.QApplication.translate("Wizard", "Performance Time", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit
