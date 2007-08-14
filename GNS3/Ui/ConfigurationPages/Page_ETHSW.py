#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
#
# Copyright (C) 2007 GNS-3 Dev Team
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation;
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#
# Contact: contact@gns3.net
#

import GNS3.Globals as globals
from PyQt4 import QtCore,  QtGui
from Form_ETHSWPage import Ui_ETHSWPage

class Page_ETHSW(QtGui.QWidget, Ui_ETHSWPage):
    """ Class implementing the Ethernet switch configuration page.
    """

    def __init__(self):
    
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setObjectName("ETHSW")
        
        # connect slots
        self.connect(self.pushButtonAdd, QtCore.SIGNAL('clicked()'), self.slotAddPort)
        self.connect(self.pushButtonDelete, QtCore.SIGNAL('clicked()'), self.slotDeletePort)
        self.connect(self.treeWidgetPorts,  QtCore.SIGNAL('itemActivated(QTreeWidgetItem *, int)'),  self.slotPortselected)
        self.connect(self.treeWidgetPorts,  QtCore.SIGNAL('itemSelectionChanged()'),  self.slotPortSelectionChanged)
        self.connect(self.checkBoxIntegratedHypervisor, QtCore.SIGNAL('stateChanged(int)'), self.slotCheckBoxIntegratedHypervisor)
        self.ports = {}
        self.vlans= {}

    def slotCheckBoxIntegratedHypervisor(self, state):
        """ Enable the comboBoxHypervisors if the check box is checked
        """
    
        if state == QtCore.Qt.Checked:
            self.comboBoxHypervisors.setEnabled(False)
        else:
            self.comboBoxHypervisors.setEnabled(True)
        
    def slotPortselected(self, item, column):
        """ Load a selected port
        """

        port = int(item.text(0))
        vlan = int(item.text(1))
        type = str(item.text(2))
        self.spinBoxPort.setValue(port)
        self.spinBoxVLAN.setValue(vlan)
        index = self.comboBoxPortType.findText(type)
        if index != -1:
            self.comboBoxPortType.setCurrentIndex(index)
        
    def slotPortSelectionChanged(self):
        """ Enable the use of the delete button
        """

        item = self.treeWidgetPorts.currentItem()
        if item != None:
            self.pushButtonDelete.setEnabled(True)
        else:
            self.pushButtonDelete.setEnabled(False)
        
    def slotAddPort(self):
        """ Add a new port
        """
    
        port = self.spinBoxPort.value()
        vlan = self.spinBoxVLAN.value()
        type = str(self.comboBoxPortType.currentText())
        
        if self.ports.has_key(port):
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, 'Add port',  'Port already exists')
            return

        item = QtGui.QTreeWidgetItem(self.treeWidgetPorts)
        item.setText(0, str(port))
        item.setText(1, str(vlan))
        item.setText(2, type)
        self.treeWidgetPorts.addTopLevelItem(item)
        
        self.spinBoxPort.setValue(port + 1)
        self.ports[port] = type
        if not self.vlans.has_key(vlan):
            self.vlans[vlan] = []
        if not port in self.vlans[vlan]:
            self.vlans[vlan].append(port)
        
        self.treeWidgetPorts.resizeColumnToContents(0)
        
    def slotDeletePort(self):
        """ Delete a port
        """
        
        item = self.treeWidgetPorts.currentItem()
        if (item != None):
            port = int(item.text(0))
            vlan = int(item.text(1))
            del self.ports[port]
            self.vlans[vlan].remove(port)
            if len(self.vlans[vlan]) == 0:
                del self.vlans[vlan]
            self.treeWidgetPorts.takeTopLevelItem(self.treeWidgetPorts.indexOfTopLevelItem(item))
        
    def loadConfig(self,  id,  config = None):
        """ Load the config
        """

        node = globals.GApp.topology.getNode(id)
        if config:
            ETHSWconfig = config
        else:
            ETHSWconfig  = node.config
            
        self.treeWidgetPorts.clear()
        self.vlans = {}
        self.ports = {}
        
        for (vlan,  portlist) in ETHSWconfig.vlans.iteritems():
            for port in portlist:
                item = QtGui.QTreeWidgetItem(self.treeWidgetPorts)
                item.setText(0, str(port))
                item.setText(1, str(vlan))
                item.setText(2, ETHSWconfig.ports[port])
                self.treeWidgetPorts.addTopLevelItem(item)
                self.ports[port] = ETHSWconfig.ports[port]
                if not self.vlans.has_key(vlan):
                    self.vlans[vlan] = []
                if not port in self.vlans[vlan]:
                    self.vlans[vlan].append(port)

        if ETHSWconfig.hypervisor_host == '':
            self.checkBoxIntegratedHypervisor.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBoxIntegratedHypervisor.setCheckState(QtCore.Qt.Unchecked)
        self.comboBoxHypervisors.clear()
        for hypervisor in globals.GApp.hypervisors:
            self.comboBoxHypervisors.addItem(hypervisor)
            
    def saveConfig(self, id, config = None):
        """ Save the config
        """
    
        node = globals.GApp.topology.getNode(id)
        if config:
            ETHSWconfig = config
        else:
            ETHSWconfig  = node.config

        ETHSWconfig.ports = self.ports
        ETHSWconfig.vlans = self.vlans
                
        if self.checkBoxIntegratedHypervisor.checkState() == QtCore.Qt.Checked:
            ETHSWconfig.hypervisor_host = ''
        elif str(self.comboBoxHypervisors.currentText()):
            (host,  port) = str(self.comboBoxHypervisors.currentText()).split(':')
            ETHSWconfig.hypervisor_host = host
            ETHSWconfig.hypervisor_port = int(port)

def create(dlg):

    return  Page_ETHSW()
