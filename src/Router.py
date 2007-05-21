#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
# Contact: developers@gns3.net
#

import sys, os, time
from MNode import *
from Inspector import Inspector
import Dynamips_lib as lib
import __main__

ROUTERS = {
    "7200": lib.C7200,
    "2691": lib.C2691,
    "2600": lib.C2600,
    "3725": lib.C3725,
    "3745": lib.C3745,
    "3600": lib.C3600
}

class Router(MNode):
    """ Router class
        Router item for the scene
    """

    # get access to globals
    main = __main__
    InspectorInstance = None


    def __init__(self, svgfile, QGraphicsScene, xPos = None, yPos = None):
        """ svgfile: string
            QGraphicsScene: QtGui.QGraphicsScene instance
            xPos: integer
            yPos: integer
        """
        
        MNode.__init__(self, svgfile, QGraphicsScene, xPos, yPos)

        # save the object
        self.main.nodes[self.id] = self

        self.InspectorInstance = Inspector(self.id)
        self.InspectorInstance.setModal(True)
        self.InspectorInstance.saveIOSConfig()
        
    def mouseDoubleClickEvent(self, event):
        """ Show the inspector instance
        """

        if (event.button() == QtCore.Qt.LeftButton):
            self.InspectorInstance.loadNodeInfos() 
            self.InspectorInstance.show()

    def configIOS(self):
        """ Create the IOS configuration on the hypervisor
        """

        self.InspectorInstance.comboBoxIOS.addItems(self.main.ios_images.keys())
        self.InspectorInstance.saveIOSConfig()

        if self.iosConfig['iosimage'] == '':
            sys.stderr.write("Node " + str(self.id) + ": no selected IOS image\n")
            return

        image_settings = self.main.ios_images[self.iosConfig['iosimage']]
        host = image_settings['hypervisor_host']
        port = image_settings['hypervisor_port']
        working_directory = image_settings['working_directory']
        platform = image_settings['platform']
        chassis = image_settings['chassis']
        idlepc = image_settings['idlepc']

        # connect to hypervisor
        if self.main.hypervisor == None:
            self.main.hypervisor = lib.Dynamips(host, port)
            self.main.hypervisor.reset()
            if working_directory:
                self.main.hypervisor.workingdir = working_directory
        
        hypervisor = self.main.hypervisor
        
        #ROUTERS
        if platform == '7200':
            self.ios = ROUTERS[platform](hypervisor, name = 'R' + str(self.id))
        if chassis in ('2691', '3725', '3745'):
            self.ios = ROUTERS[chassis](hypervisor, name = 'R' + str(self.id))
        elif platform in ('3600', '2600'):
            self.ios = ROUTERS[platform](hypervisor, chassis = chassis, name = 'R' + str(self.id))

        self.ios.image = self.iosConfig['iosimage'].split(':')[1]
        if self.iosConfig['startup-config'] != '':
            self.ios.cnfg = self.iosConfig['startup-config']
        self.ios.ram = self.iosConfig['RAM']
        self.ios.rom = self.iosConfig['ROM']
        self.ios.nvram = self.iosConfig['NVRAM']
        if self.iosConfig['pcmcia-disk0'] != 0:
            self.ios.disk0 = self.iosConfig['pcmcia-disk0']
        if self.iosConfig['pcmcia-disk1'] != 0:
            self.ios.disk1 = self.iosConfig['pcmcia-disk1']
        self.ios.mmap = self.iosConfig['mmap']
        if self.iosConfig['confreg'] != '':
            self.ios.conf = self.iosConfig['confreg']
        self.ios.exec_area = self.iosConfig['execarea']
        if platform == '3600':
            pass
            # seems to have a bug here with the lib
            #self.ios.iomem = str(self.iosConfig['iomem'])
        if platform == '7200':
            self.ios.midplane = self.iosConfig['midplane']
            self.ios.npe = self.iosConfig['npe']

        slotnb = 0
        for module in self.iosConfig['slots']:
            self.configSlot(slotnb, module)
            slotnb += 1
        if idlepc:
            self.ios.idlepc = idlepc
        else: #FIXME: only for tests
            self.ios.idlepc = '0x60483ae4'
        
    def configSlot(self, slotnb, module):
        """ Add an new module into a slot
            slotnb: integer
            module: string
        """
        
        if (module == ''):
            return
        if module in ADAPTERS:
            self.ios.slot[slotnb] = ADAPTERS[module][0](self.ios, slotnb)
        else:
            sys.stderr.write(module + " module not found !\n")
            return
      
    def startIOS(self):
        """ Create connections between nodes
            Start the IOS instance
        """
        
        # localport, remoteserver, remoteadapter, remoteport
        # self.ios.slot[0].connect(0, self.main.hypervisor, esw.slot[1], 0)
        if self.ios == None:
            return

        for interface in self.interfaces.keys():
            connection = self.interfaces[interface]
            source_slot = int(interface[1])
            source_port = int(interface[3])
            dest_nodeid = int(connection[0])
            dest_slot = int(connection[1][1])
            dest_port = int(connection[1][3])
            node = self.main.nodes[dest_nodeid]
            assert(node != None)
            try:
                if self.ios.slot[source_slot] != None and self.ios.slot[source_slot].connected(source_port) == False:
                    lib.validate_connect(self.ios.slot[source_slot], node.ios.slot[dest_slot])
                    self.ios.slot[source_slot].connect(source_port, self.main.hypervisor, node.ios.slot[dest_slot], dest_port)
            except lib.DynamipsError, msg:
                print msg

        print self.ios.start()
        
    def stopIOS(self):
        """ Stop the IOS instance
        """
    
        if self.ios != None:
            print self.ios.stop()
        
    def resetIOSConfig(self):
        """ Delete the IOS instance
        """
    
        if self.ios != None:
            self.ios.delete()
     