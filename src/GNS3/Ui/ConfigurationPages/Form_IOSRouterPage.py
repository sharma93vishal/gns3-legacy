# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ConfigurationPages/Form_IOSRouterPage.ui'
#
# Created: Tue May 29 03:21:49 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_IOSRouterPage(object):
    def setupUi(self, IOSRouterPage):
        IOSRouterPage.setObjectName(_fromUtf8("IOSRouterPage"))
        IOSRouterPage.resize(439, 488)
        self.vboxlayout = QtGui.QVBoxLayout(IOSRouterPage)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.tabWidget = QtGui.QTabWidget(IOSRouterPage)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.General = QtGui.QWidget()
        self.General.setObjectName(_fromUtf8("General"))
        self.gridlayout = QtGui.QGridLayout(self.General)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.label_4 = QtGui.QLabel(self.General)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridlayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.textLabel_Platform = QtGui.QLabel(self.General)
        self.textLabel_Platform.setText(_fromUtf8(""))
        self.textLabel_Platform.setObjectName(_fromUtf8("textLabel_Platform"))
        self.gridlayout.addWidget(self.textLabel_Platform, 0, 1, 1, 1)
        self.label_8 = QtGui.QLabel(self.General)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridlayout.addWidget(self.label_8, 1, 0, 1, 1)
        self.textLabel_Model = QtGui.QLabel(self.General)
        self.textLabel_Model.setText(_fromUtf8(""))
        self.textLabel_Model.setObjectName(_fromUtf8("textLabel_Model"))
        self.gridlayout.addWidget(self.textLabel_Model, 1, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.General)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridlayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.textLabel_ImageIOS = QtGui.QLabel(self.General)
        self.textLabel_ImageIOS.setText(_fromUtf8(""))
        self.textLabel_ImageIOS.setObjectName(_fromUtf8("textLabel_ImageIOS"))
        self.gridlayout.addWidget(self.textLabel_ImageIOS, 2, 1, 1, 1)
        self.label_18 = QtGui.QLabel(self.General)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.gridlayout.addWidget(self.label_18, 3, 0, 1, 1)
        self.textLabel_StartupConfig = QtGui.QLabel(self.General)
        self.textLabel_StartupConfig.setText(_fromUtf8(""))
        self.textLabel_StartupConfig.setObjectName(_fromUtf8("textLabel_StartupConfig"))
        self.gridlayout.addWidget(self.textLabel_StartupConfig, 3, 1, 1, 1)
        self.label = QtGui.QLabel(self.General)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridlayout.addWidget(self.label, 4, 0, 1, 1)
        self.comboBoxMidplane = QtGui.QComboBox(self.General)
        self.comboBoxMidplane.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxMidplane.sizePolicy().hasHeightForWidth())
        self.comboBoxMidplane.setSizePolicy(sizePolicy)
        self.comboBoxMidplane.setObjectName(_fromUtf8("comboBoxMidplane"))
        self.gridlayout.addWidget(self.comboBoxMidplane, 4, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.General)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridlayout.addWidget(self.label_2, 5, 0, 1, 1)
        self.comboBoxNPE = QtGui.QComboBox(self.General)
        self.comboBoxNPE.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxNPE.sizePolicy().hasHeightForWidth())
        self.comboBoxNPE.setSizePolicy(sizePolicy)
        self.comboBoxNPE.setObjectName(_fromUtf8("comboBoxNPE"))
        self.gridlayout.addWidget(self.comboBoxNPE, 5, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(263, 151, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 6, 1, 1, 1)
        self.tabWidget.addTab(self.General, _fromUtf8(""))
        self.MemoriesDisks = QtGui.QWidget()
        self.MemoriesDisks.setObjectName(_fromUtf8("MemoriesDisks"))
        self.vboxlayout1 = QtGui.QVBoxLayout(self.MemoriesDisks)
        self.vboxlayout1.setObjectName(_fromUtf8("vboxlayout1"))
        self.groupBox_2 = QtGui.QGroupBox(self.MemoriesDisks)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridlayout1 = QtGui.QGridLayout(self.groupBox_2)
        self.gridlayout1.setObjectName(_fromUtf8("gridlayout1"))
        self.label_7 = QtGui.QLabel(self.groupBox_2)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridlayout1.addWidget(self.label_7, 0, 0, 1, 1)
        self.spinBoxRamSize = QtGui.QSpinBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxRamSize.sizePolicy().hasHeightForWidth())
        self.spinBoxRamSize.setSizePolicy(sizePolicy)
        self.spinBoxRamSize.setMaximum(4096)
        self.spinBoxRamSize.setSingleStep(4)
        self.spinBoxRamSize.setProperty(_fromUtf8("value"), 128)
        self.spinBoxRamSize.setObjectName(_fromUtf8("spinBoxRamSize"))
        self.gridlayout1.addWidget(self.spinBoxRamSize, 0, 1, 1, 1)
        self.label_9 = QtGui.QLabel(self.groupBox_2)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridlayout1.addWidget(self.label_9, 1, 0, 1, 1)
        self.spinBoxNvramSize = QtGui.QSpinBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxNvramSize.sizePolicy().hasHeightForWidth())
        self.spinBoxNvramSize.setSizePolicy(sizePolicy)
        self.spinBoxNvramSize.setMaximum(4096)
        self.spinBoxNvramSize.setSingleStep(4)
        self.spinBoxNvramSize.setProperty(_fromUtf8("value"), 128)
        self.spinBoxNvramSize.setObjectName(_fromUtf8("spinBoxNvramSize"))
        self.gridlayout1.addWidget(self.spinBoxNvramSize, 1, 1, 1, 1)
        self.vboxlayout1.addWidget(self.groupBox_2)
        self.groupBox_6 = QtGui.QGroupBox(self.MemoriesDisks)
        self.groupBox_6.setObjectName(_fromUtf8("groupBox_6"))
        self.gridlayout2 = QtGui.QGridLayout(self.groupBox_6)
        self.gridlayout2.setObjectName(_fromUtf8("gridlayout2"))
        self.label_10 = QtGui.QLabel(self.groupBox_6)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridlayout2.addWidget(self.label_10, 0, 0, 1, 1)
        self.spinBoxPcmciaDisk0Size = QtGui.QSpinBox(self.groupBox_6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxPcmciaDisk0Size.sizePolicy().hasHeightForWidth())
        self.spinBoxPcmciaDisk0Size.setSizePolicy(sizePolicy)
        self.spinBoxPcmciaDisk0Size.setMaximum(99999)
        self.spinBoxPcmciaDisk0Size.setSingleStep(4)
        self.spinBoxPcmciaDisk0Size.setObjectName(_fromUtf8("spinBoxPcmciaDisk0Size"))
        self.gridlayout2.addWidget(self.spinBoxPcmciaDisk0Size, 0, 1, 1, 1)
        self.label_11 = QtGui.QLabel(self.groupBox_6)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridlayout2.addWidget(self.label_11, 1, 0, 1, 1)
        self.spinBoxPcmciaDisk1Size = QtGui.QSpinBox(self.groupBox_6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxPcmciaDisk1Size.sizePolicy().hasHeightForWidth())
        self.spinBoxPcmciaDisk1Size.setSizePolicy(sizePolicy)
        self.spinBoxPcmciaDisk1Size.setMaximum(99999)
        self.spinBoxPcmciaDisk1Size.setSingleStep(4)
        self.spinBoxPcmciaDisk1Size.setObjectName(_fromUtf8("spinBoxPcmciaDisk1Size"))
        self.gridlayout2.addWidget(self.spinBoxPcmciaDisk1Size, 1, 1, 1, 1)
        self.vboxlayout1.addWidget(self.groupBox_6)
        spacerItem1 = QtGui.QSpacerItem(20, 21, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vboxlayout1.addItem(spacerItem1)
        self.tabWidget.addTab(self.MemoriesDisks, _fromUtf8(""))
        self.Slots = QtGui.QWidget()
        self.Slots.setObjectName(_fromUtf8("Slots"))
        self.verticalLayout = QtGui.QVBoxLayout(self.Slots)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_3 = QtGui.QGroupBox(self.Slots)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_6 = QtGui.QLabel(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)
        self.comboBoxSlot0 = QtGui.QComboBox(self.groupBox_3)
        self.comboBoxSlot0.setObjectName(_fromUtf8("comboBoxSlot0"))
        self.gridLayout.addWidget(self.comboBoxSlot0, 0, 1, 1, 1)
        self.label_12 = QtGui.QLabel(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout.addWidget(self.label_12, 1, 0, 1, 1)
        self.comboBoxSlot1 = QtGui.QComboBox(self.groupBox_3)
        self.comboBoxSlot1.setObjectName(_fromUtf8("comboBoxSlot1"))
        self.gridLayout.addWidget(self.comboBoxSlot1, 1, 1, 1, 1)
        self.label_15 = QtGui.QLabel(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.gridLayout.addWidget(self.label_15, 2, 0, 1, 1)
        self.comboBoxSlot2 = QtGui.QComboBox(self.groupBox_3)
        self.comboBoxSlot2.setObjectName(_fromUtf8("comboBoxSlot2"))
        self.gridLayout.addWidget(self.comboBoxSlot2, 2, 1, 1, 1)
        self.label_19 = QtGui.QLabel(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.gridLayout.addWidget(self.label_19, 3, 0, 1, 1)
        self.comboBoxSlot3 = QtGui.QComboBox(self.groupBox_3)
        self.comboBoxSlot3.setObjectName(_fromUtf8("comboBoxSlot3"))
        self.gridLayout.addWidget(self.comboBoxSlot3, 3, 1, 1, 1)
        self.label_23 = QtGui.QLabel(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy)
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.gridLayout.addWidget(self.label_23, 4, 0, 1, 1)
        self.comboBoxSlot4 = QtGui.QComboBox(self.groupBox_3)
        self.comboBoxSlot4.setObjectName(_fromUtf8("comboBoxSlot4"))
        self.gridLayout.addWidget(self.comboBoxSlot4, 4, 1, 1, 1)
        self.label_26 = QtGui.QLabel(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_26.sizePolicy().hasHeightForWidth())
        self.label_26.setSizePolicy(sizePolicy)
        self.label_26.setObjectName(_fromUtf8("label_26"))
        self.gridLayout.addWidget(self.label_26, 5, 0, 1, 1)
        self.comboBoxSlot5 = QtGui.QComboBox(self.groupBox_3)
        self.comboBoxSlot5.setObjectName(_fromUtf8("comboBoxSlot5"))
        self.gridLayout.addWidget(self.comboBoxSlot5, 5, 1, 1, 1)
        self.label_28 = QtGui.QLabel(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_28.sizePolicy().hasHeightForWidth())
        self.label_28.setSizePolicy(sizePolicy)
        self.label_28.setObjectName(_fromUtf8("label_28"))
        self.gridLayout.addWidget(self.label_28, 6, 0, 1, 1)
        self.comboBoxSlot6 = QtGui.QComboBox(self.groupBox_3)
        self.comboBoxSlot6.setObjectName(_fromUtf8("comboBoxSlot6"))
        self.gridLayout.addWidget(self.comboBoxSlot6, 6, 1, 1, 1)
        self.label_30 = QtGui.QLabel(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_30.sizePolicy().hasHeightForWidth())
        self.label_30.setSizePolicy(sizePolicy)
        self.label_30.setObjectName(_fromUtf8("label_30"))
        self.gridLayout.addWidget(self.label_30, 7, 0, 1, 1)
        self.comboBoxSlot7 = QtGui.QComboBox(self.groupBox_3)
        self.comboBoxSlot7.setObjectName(_fromUtf8("comboBoxSlot7"))
        self.gridLayout.addWidget(self.comboBoxSlot7, 7, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox = QtGui.QGroupBox(self.Slots)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridlayout3 = QtGui.QGridLayout(self.groupBox)
        self.gridlayout3.setObjectName(_fromUtf8("gridlayout3"))
        self.label_13 = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridlayout3.addWidget(self.label_13, 0, 0, 1, 1)
        self.comboBoxWIC0 = QtGui.QComboBox(self.groupBox)
        self.comboBoxWIC0.setObjectName(_fromUtf8("comboBoxWIC0"))
        self.gridlayout3.addWidget(self.comboBoxWIC0, 0, 1, 1, 1)
        self.label_14 = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridlayout3.addWidget(self.label_14, 1, 0, 1, 1)
        self.comboBoxWIC1 = QtGui.QComboBox(self.groupBox)
        self.comboBoxWIC1.setObjectName(_fromUtf8("comboBoxWIC1"))
        self.gridlayout3.addWidget(self.comboBoxWIC1, 1, 1, 1, 1)
        self.label_16 = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.gridlayout3.addWidget(self.label_16, 2, 0, 1, 1)
        self.comboBoxWIC2 = QtGui.QComboBox(self.groupBox)
        self.comboBoxWIC2.setObjectName(_fromUtf8("comboBoxWIC2"))
        self.gridlayout3.addWidget(self.comboBoxWIC2, 2, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        spacerItem2 = QtGui.QSpacerItem(325, 31, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.tabWidget.addTab(self.Slots, _fromUtf8(""))
        self.Advanced = QtGui.QWidget()
        self.Advanced.setObjectName(_fromUtf8("Advanced"))
        self.gridlayout4 = QtGui.QGridLayout(self.Advanced)
        self.gridlayout4.setObjectName(_fromUtf8("gridlayout4"))
        self.label_25 = QtGui.QLabel(self.Advanced)
        self.label_25.setObjectName(_fromUtf8("label_25"))
        self.gridlayout4.addWidget(self.label_25, 0, 0, 1, 1)
        self.lineEditConfreg = QtGui.QLineEdit(self.Advanced)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditConfreg.sizePolicy().hasHeightForWidth())
        self.lineEditConfreg.setSizePolicy(sizePolicy)
        self.lineEditConfreg.setObjectName(_fromUtf8("lineEditConfreg"))
        self.gridlayout4.addWidget(self.lineEditConfreg, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.Advanced)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridlayout4.addWidget(self.label_3, 1, 0, 1, 1)
        self.lineEditMAC = QtGui.QLineEdit(self.Advanced)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditMAC.sizePolicy().hasHeightForWidth())
        self.lineEditMAC.setSizePolicy(sizePolicy)
        self.lineEditMAC.setText(_fromUtf8(""))
        self.lineEditMAC.setObjectName(_fromUtf8("lineEditMAC"))
        self.gridlayout4.addWidget(self.lineEditMAC, 1, 1, 1, 1)
        self.label_31 = QtGui.QLabel(self.Advanced)
        self.label_31.setObjectName(_fromUtf8("label_31"))
        self.gridlayout4.addWidget(self.label_31, 2, 0, 1, 1)
        self.spinBoxExecArea = QtGui.QSpinBox(self.Advanced)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxExecArea.sizePolicy().hasHeightForWidth())
        self.spinBoxExecArea.setSizePolicy(sizePolicy)
        self.spinBoxExecArea.setMaximum(4096)
        self.spinBoxExecArea.setSingleStep(4)
        self.spinBoxExecArea.setProperty(_fromUtf8("value"), 64)
        self.spinBoxExecArea.setObjectName(_fromUtf8("spinBoxExecArea"))
        self.gridlayout4.addWidget(self.spinBoxExecArea, 2, 1, 1, 1)
        self.label_22 = QtGui.QLabel(self.Advanced)
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.gridlayout4.addWidget(self.label_22, 3, 0, 1, 1)
        self.spinBoxIomem = QtGui.QSpinBox(self.Advanced)
        self.spinBoxIomem.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxIomem.sizePolicy().hasHeightForWidth())
        self.spinBoxIomem.setSizePolicy(sizePolicy)
        self.spinBoxIomem.setMaximum(100)
        self.spinBoxIomem.setSingleStep(5)
        self.spinBoxIomem.setProperty(_fromUtf8("value"), 5)
        self.spinBoxIomem.setObjectName(_fromUtf8("spinBoxIomem"))
        self.gridlayout4.addWidget(self.spinBoxIomem, 3, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(304, 251, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout4.addItem(spacerItem3, 4, 0, 1, 2)
        self.tabWidget.addTab(self.Advanced, _fromUtf8(""))
        self.vboxlayout.addWidget(self.tabWidget)

        self.retranslateUi(IOSRouterPage)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(IOSRouterPage)

    def retranslateUi(self, IOSRouterPage):
        IOSRouterPage.setWindowTitle(QtGui.QApplication.translate("IOSRouterPage", "Router configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("IOSRouterPage", "Platform:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("IOSRouterPage", "Model:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("IOSRouterPage", "IOS image:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_18.setText(QtGui.QApplication.translate("IOSRouterPage", "Startup-config:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("IOSRouterPage", "Midplane:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("IOSRouterPage", "NPE:", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.General), QtGui.QApplication.translate("IOSRouterPage", "General", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("IOSRouterPage", "Memories", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("IOSRouterPage", "RAM size:", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxRamSize.setSuffix(QtGui.QApplication.translate("IOSRouterPage", " MiB", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("IOSRouterPage", "NVRAM size:", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxNvramSize.setSuffix(QtGui.QApplication.translate("IOSRouterPage", " KiB", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_6.setTitle(QtGui.QApplication.translate("IOSRouterPage", "Disks", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("IOSRouterPage", "PCMCIA disk0 size:", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxPcmciaDisk0Size.setSuffix(QtGui.QApplication.translate("IOSRouterPage", " MiB", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("IOSRouterPage", "PCMCIA disk1 size:", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxPcmciaDisk1Size.setSuffix(QtGui.QApplication.translate("IOSRouterPage", " MiB", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.MemoriesDisks), QtGui.QApplication.translate("IOSRouterPage", "Memories and disks", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("IOSRouterPage", "Adapters", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("IOSRouterPage", "slot 0:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("IOSRouterPage", "slot 1:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("IOSRouterPage", "slot 2:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_19.setText(QtGui.QApplication.translate("IOSRouterPage", "slot 3:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_23.setText(QtGui.QApplication.translate("IOSRouterPage", "slot 4:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_26.setText(QtGui.QApplication.translate("IOSRouterPage", "slot 5:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_28.setText(QtGui.QApplication.translate("IOSRouterPage", "slot 6:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_30.setText(QtGui.QApplication.translate("IOSRouterPage", "slot 7:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("IOSRouterPage", "WICs", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("IOSRouterPage", "wic 0:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("IOSRouterPage", "wic 1:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("IOSRouterPage", "wic 2:", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Slots), QtGui.QApplication.translate("IOSRouterPage", "Slots", None, QtGui.QApplication.UnicodeUTF8))
        self.label_25.setText(QtGui.QApplication.translate("IOSRouterPage", "Confreg:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditConfreg.setText(QtGui.QApplication.translate("IOSRouterPage", "0x2102", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("IOSRouterPage", "Base MAC :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_31.setText(QtGui.QApplication.translate("IOSRouterPage", "exec area:", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxExecArea.setSuffix(QtGui.QApplication.translate("IOSRouterPage", " MiB", None, QtGui.QApplication.UnicodeUTF8))
        self.label_22.setText(QtGui.QApplication.translate("IOSRouterPage", "iomem :", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxIomem.setSuffix(QtGui.QApplication.translate("IOSRouterPage", " %", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Advanced), QtGui.QApplication.translate("IOSRouterPage", "Advanced", None, QtGui.QApplication.UnicodeUTF8))

