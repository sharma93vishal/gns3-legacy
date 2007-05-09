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

import sys
sys.path.append('../forms')
import locale
import translations
from PyQt4 import QtCore, QtGui
from MainWindow import MainWindow
import Dynamips_lib as lib

# globals
baseid = 0                # Base to create IDs
nodes = {}                # Node objects, indexed by the node ID
hypervisor = None         # Hypervisor connection
conception_mode = True    # If we are in conception mode

class Main:
    ''' Entry point '''

    def __init__(self, argv):

        # temporary emplacement for a connection to a local hypervisor
        global hypervisor
        try:
            hypervisor = lib.Dynamips('localhost', 7200)
            hypervisor.reset()
            hypervisor.workingdir = '/tmp'
        except lib.DynamipsError, msg:
            print "Dynamips error: %s" % msg
            hypervisor = None

        app = QtGui.QApplication(sys.argv)

        # translation management
        translator = QtCore.QTranslator(app)
        #print locale.getlocale()[0]
        #if translator.load(":/" + locale.getlocale()[0][:2]):
        #    app.installTranslator(translator)
        win = MainWindow()
        
        # We start in conception mode
        win.statusbar.showMessage('Conception Mode')
        
        # signal/slot for the menu
        win.connect(win.action_Open, QtCore.SIGNAL('activated()'), win.OpenNewFile)
        win.connect(win.action_Save, QtCore.SIGNAL('activated()'), win.SaveToFile)
        win.connect(win.action_About, QtCore.SIGNAL('activated()'), win.About)
        win.connect(win.action_Add_link, QtCore.SIGNAL('activated()'), win.AddEdge)
        win.connect(win.action_SwitchMode, QtCore.SIGNAL('activated()'), win.SwitchMode)        
        win.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    Main(sys.argv)