# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_PreferencesGeneral.ui'
#
# Created: Sat Feb  6 15:26:23 2010
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PreferencesGeneral(object):
    def setupUi(self, PreferencesGeneral):
        PreferencesGeneral.setObjectName("PreferencesGeneral")
        PreferencesGeneral.resize(539, 456)
        self.vboxlayout = QtGui.QVBoxLayout(PreferencesGeneral)
        self.vboxlayout.setObjectName("vboxlayout")
        self.tabWidget = QtGui.QTabWidget(PreferencesGeneral)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtGui.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtGui.QLabel(self.tab)
        self.label.setEnabled(True)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.langsBox = QtGui.QComboBox(self.tab)
        self.langsBox.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.langsBox.sizePolicy().hasHeightForWidth())
        self.langsBox.setSizePolicy(sizePolicy)
        self.langsBox.setObjectName("langsBox")
        self.gridLayout_2.addWidget(self.langsBox, 1, 0, 1, 1)
        self.checkBoxProjectDialog = QtGui.QCheckBox(self.tab)
        self.checkBoxProjectDialog.setChecked(True)
        self.checkBoxProjectDialog.setObjectName("checkBoxProjectDialog")
        self.gridLayout_2.addWidget(self.checkBoxProjectDialog, 2, 0, 1, 1)
        self.label_7 = QtGui.QLabel(self.tab)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 3, 0, 1, 1)
        self.slowStartAll = QtGui.QSpinBox(self.tab)
        self.slowStartAll.setMaximum(10000)
        self.slowStartAll.setObjectName("slowStartAll")
        self.gridLayout_2.addWidget(self.slowStartAll, 4, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(self.tab)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridlayout = QtGui.QGridLayout(self.groupBox_2)
        self.gridlayout.setObjectName("gridlayout")
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.ProjectPath = QtGui.QLineEdit(self.groupBox_2)
        self.ProjectPath.setObjectName("ProjectPath")
        self.gridlayout.addWidget(self.ProjectPath, 1, 0, 1, 1)
        self.ProjectPath_browser = QtGui.QToolButton(self.groupBox_2)
        self.ProjectPath_browser.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.ProjectPath_browser.setObjectName("ProjectPath_browser")
        self.gridlayout.addWidget(self.ProjectPath_browser, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.IOSPath = QtGui.QLineEdit(self.groupBox_2)
        self.IOSPath.setObjectName("IOSPath")
        self.gridlayout.addWidget(self.IOSPath, 3, 0, 1, 1)
        self.IOSPath_browser = QtGui.QToolButton(self.groupBox_2)
        self.IOSPath_browser.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.IOSPath_browser.setObjectName("IOSPath_browser")
        self.gridlayout.addWidget(self.IOSPath_browser, 3, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_2, 5, 0, 1, 1)
        self.groupBox_3 = QtGui.QGroupBox(self.tab)
        self.groupBox_3.setObjectName("groupBox_3")
        self.hboxlayout = QtGui.QHBoxLayout(self.groupBox_3)
        self.hboxlayout.setObjectName("hboxlayout")
        self.labelConfigurationPath = QtGui.QLabel(self.groupBox_3)
        self.labelConfigurationPath.setObjectName("labelConfigurationPath")
        self.hboxlayout.addWidget(self.labelConfigurationPath)
        spacerItem = QtGui.QSpacerItem(16, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.pushButton_ClearConfiguration = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_ClearConfiguration.setObjectName("pushButton_ClearConfiguration")
        self.hboxlayout.addWidget(self.pushButton_ClearConfiguration)
        self.gridLayout_2.addWidget(self.groupBox_3, 6, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(471, 21, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 7, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout = QtGui.QGridLayout(self.tab_3)
        self.gridLayout.setObjectName("gridLayout")
        self.label_8 = QtGui.QLabel(self.tab_3)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 0, 0, 1, 1)
        self.comboBoxPreconfigTerminalCommands = QtGui.QComboBox(self.tab_3)
        self.comboBoxPreconfigTerminalCommands.setObjectName("comboBoxPreconfigTerminalCommands")
        self.gridLayout.addWidget(self.comboBoxPreconfigTerminalCommands, 1, 0, 1, 1)
        self.pushButtonUseTerminalCommand = QtGui.QPushButton(self.tab_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonUseTerminalCommand.sizePolicy().hasHeightForWidth())
        self.pushButtonUseTerminalCommand.setSizePolicy(sizePolicy)
        self.pushButtonUseTerminalCommand.setObjectName("pushButtonUseTerminalCommand")
        self.gridLayout.addWidget(self.pushButtonUseTerminalCommand, 1, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.tab_3)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.lineEditTermCommand = QtGui.QLineEdit(self.tab_3)
        self.lineEditTermCommand.setObjectName("lineEditTermCommand")
        self.gridLayout.addWidget(self.lineEditTermCommand, 3, 0, 1, 2)
        self.checkBoxUseShell = QtGui.QCheckBox(self.tab_3)
        self.checkBoxUseShell.setChecked(True)
        self.checkBoxUseShell.setObjectName("checkBoxUseShell")
        self.gridLayout.addWidget(self.checkBoxUseShell, 4, 0, 1, 1)
        self.label_9 = QtGui.QLabel(self.tab_3)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 5, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 315, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 6, 0, 1, 2)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridlayout1 = QtGui.QGridLayout(self.tab_2)
        self.gridlayout1.setObjectName("gridlayout1")
        self.label_5 = QtGui.QLabel(self.tab_2)
        self.label_5.setObjectName("label_5")
        self.gridlayout1.addWidget(self.label_5, 0, 0, 1, 1)
        self.workspaceWidth = QtGui.QSpinBox(self.tab_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.workspaceWidth.sizePolicy().hasHeightForWidth())
        self.workspaceWidth.setSizePolicy(sizePolicy)
        self.workspaceWidth.setMinimum(500)
        self.workspaceWidth.setMaximum(1000000)
        self.workspaceWidth.setSingleStep(100)
        self.workspaceWidth.setProperty("value", 2000)
        self.workspaceWidth.setObjectName("workspaceWidth")
        self.gridlayout1.addWidget(self.workspaceWidth, 0, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.tab_2)
        self.label_6.setObjectName("label_6")
        self.gridlayout1.addWidget(self.label_6, 1, 0, 1, 1)
        self.workspaceHeight = QtGui.QSpinBox(self.tab_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.workspaceHeight.sizePolicy().hasHeightForWidth())
        self.workspaceHeight.setSizePolicy(sizePolicy)
        self.workspaceHeight.setMinimum(500)
        self.workspaceHeight.setMaximum(1000000)
        self.workspaceHeight.setSingleStep(100)
        self.workspaceHeight.setProperty("value", 1000)
        self.workspaceHeight.setObjectName("workspaceHeight")
        self.gridlayout1.addWidget(self.workspaceHeight, 1, 1, 1, 1)
        self.checkBoxDrawRectangle = QtGui.QCheckBox(self.tab_2)
        self.checkBoxDrawRectangle.setChecked(True)
        self.checkBoxDrawRectangle.setObjectName("checkBoxDrawRectangle")
        self.gridlayout1.addWidget(self.checkBoxDrawRectangle, 2, 0, 1, 2)
        self.checkBoxManualConnections = QtGui.QCheckBox(self.tab_2)
        self.checkBoxManualConnections.setChecked(True)
        self.checkBoxManualConnections.setObjectName("checkBoxManualConnections")
        self.gridlayout1.addWidget(self.checkBoxManualConnections, 3, 0, 1, 2)
        self.checkBoxShowStatusPoints = QtGui.QCheckBox(self.tab_2)
        self.checkBoxShowStatusPoints.setChecked(True)
        self.checkBoxShowStatusPoints.setObjectName("checkBoxShowStatusPoints")
        self.gridlayout1.addWidget(self.checkBoxShowStatusPoints, 4, 0, 1, 2)
        spacerItem3 = QtGui.QSpacerItem(20, 251, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem3, 5, 1, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.vboxlayout.addWidget(self.tabWidget)

        self.retranslateUi(PreferencesGeneral)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(PreferencesGeneral)

    def retranslateUi(self, PreferencesGeneral):
        PreferencesGeneral.setWindowTitle(QtGui.QApplication.translate("PreferencesGeneral", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PreferencesGeneral", "Language:", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxProjectDialog.setText(QtGui.QApplication.translate("PreferencesGeneral", "Launch the project dialog at startup", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("PreferencesGeneral", "Waiting time between each start when starting every devices:", None, QtGui.QApplication.UnicodeUTF8))
        self.slowStartAll.setSuffix(QtGui.QApplication.translate("PreferencesGeneral", " seconds", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("PreferencesGeneral", "Paths", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("PreferencesGeneral", "Project directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.ProjectPath_browser.setText(QtGui.QApplication.translate("PreferencesGeneral", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("PreferencesGeneral", "Image directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.IOSPath_browser.setText(QtGui.QApplication.translate("PreferencesGeneral", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("PreferencesGeneral", "Configuration file", None, QtGui.QApplication.UnicodeUTF8))
        self.labelConfigurationPath.setText(QtGui.QApplication.translate("PreferencesGeneral", "Unknown location", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_ClearConfiguration.setText(QtGui.QApplication.translate("PreferencesGeneral", "&Clear it", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("PreferencesGeneral", "General Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("PreferencesGeneral", "Preconfigurated terminal commands:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonUseTerminalCommand.setText(QtGui.QApplication.translate("PreferencesGeneral", "&Use", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("PreferencesGeneral", "Terminal command:", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxUseShell.setText(QtGui.QApplication.translate("PreferencesGeneral", "Launch this command using the system default shell", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("PreferencesGeneral", "Terminal command magic strings:\n"
"%h = device server \n"
"%p = device port\n"
"%d = device hostname", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("PreferencesGeneral", "Terminal Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("PreferencesGeneral", "Workspace width:", None, QtGui.QApplication.UnicodeUTF8))
        self.workspaceWidth.setSuffix(QtGui.QApplication.translate("PreferencesGeneral", " px", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("PreferencesGeneral", "Workspace height:", None, QtGui.QApplication.UnicodeUTF8))
        self.workspaceHeight.setSuffix(QtGui.QApplication.translate("PreferencesGeneral", " px", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxDrawRectangle.setText(QtGui.QApplication.translate("PreferencesGeneral", "Draw a rectangle when an item is selected", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxManualConnections.setText(QtGui.QApplication.translate("PreferencesGeneral", "Always use manual mode when adding links", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxShowStatusPoints.setText(QtGui.QApplication.translate("PreferencesGeneral", "Show link status points on the workspace", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("PreferencesGeneral", "GUI Settings", None, QtGui.QApplication.UnicodeUTF8))

