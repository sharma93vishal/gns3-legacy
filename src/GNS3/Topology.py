# -*- coding: utf-8 -*-
# vim: expandtab ts=4 sw=4 sts=4:
#
# Copyright (C) 2007-2010 GNS3 Development Team (http://www.gns3.net/team).
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
# code@gns3.net
#

import os, glob, socket, sys
import GNS3.Dynagen.dynamips_lib as lib
import GNS3.Dynagen.qemu_lib as qlib
import GNS3.Globals as globals
import GNS3.UndoFramework as undo 
from PyQt4 import QtGui, QtCore
from GNS3.Utils import translate, debug
from GNS3.Link.Ethernet import Ethernet
from GNS3.Link.Serial import Serial
from GNS3.Node.DecorativeNode import DecorativeNode,  init_decoration_id
from GNS3.Node.IOSRouter import IOSRouter, init_router_id
from GNS3.Node.ATMSW import ATMSW, init_atmsw_id
from GNS3.Node.ATMBR import ATMBR, init_atmbr_id
from GNS3.Node.ETHSW import ETHSW, init_ethsw_id
from GNS3.Node.FRSW import FRSW, init_frsw_id
from GNS3.Node.Cloud import Cloud, init_cloud_id
from GNS3.Node.AnyEmuDevice import QemuDevice, FW, ASA, AnyEmuDevice, JunOS, IDS, init_emu_id
from GNS3.Node.AbstractNode import AbstractNode
from GNS3.Annotation import Annotation


class Topology(QtGui.QGraphicsScene):
    """ Topology class
    """

    def __init__(self, parent=None):

        self.__nodes = {}
        self.__links = set()

        self.node_baseid = 0
        self.link_baseid = 0
        self.dynagen = globals.GApp.dynagen
        self.changed = False

        width = globals.GApp.systconf['general'].scene_width
        height = globals.GApp.systconf['general'].scene_height
        
        QtGui.QGraphicsScene.__init__(self, parent)
        self.setSceneRect(-(width / 2), -(height / 2), width, height)

        self.undoStack = QtGui.QUndoStack(self)
        self.undoStack.setUndoLimit(30)

    def mousePressEvent(self, event):

        srcnode = globals.GApp.scene.getSourceNode()
        item = self.itemAt(event.scenePos())
        if item and ((isinstance(item, AbstractNode) and \
        globals.currentLinkType == globals.Enum.LinkType.Manual) or \
        isinstance(srcnode, AnyEmuDevice) or isinstance(srcnode, FRSW) or \
        isinstance(srcnode, ATMBR) or isinstance(srcnode, ATMSW) or isinstance(srcnode, Cloud)):
            # In few circumstances, QtGui.QGraphicsScene.mousePressEvent()
            # send the mousePressEvent to the wrong item; we need to
            # correct this behaviour for 'Manual Link' mode. We force the 
            # event to be send to the right item and activate workaround
            # so that the false recipiend ignore it.
            item.mousePressEvent(event)
            globals.workaround_ManualLink = True
        elif item and isinstance(item, Annotation):
            item.mousePressEvent(event)
        QtGui.QGraphicsScene.mousePressEvent(self, event)

    def cleanDynagen(self):
        """ Clean all dynagen data
        """

        for dynamips in globals.GApp.dynagen.dynamips.values():
            try:
                dynamips.reset()
            except:
                continue
        if globals.GApp.HypervisorManager:
            globals.GApp.HypervisorManager.stopProcHypervisors()
        if globals.GApp.QemuManager:
            globals.GApp.QemuManager.stopQemu()

        self.dynagen.dynamips.clear()
        self.dynagen.handled = False
        self.dynagen.devices.clear()
        self.dynagen.globalconfig.clear()
        self.dynagen.configurations.clear()
        self.dynagen.ghosteddevices.clear()
        self.dynagen.ghostsizes.clear()
        self.dynagen.bridges.clear()
        self.dynagen.autostart.clear()

    def clear(self):
        """ Clear the topology
        """

        # Clear Undo Stack first
        self.undoStack.clear()
        globals.interfaceLabels.clear()

        for n_key in self.__nodes.copy().iterkeys():
            self.deleteNode(n_key)
        self.__nodes = {}
        while len(self.__links) > 0:
            o = self.__links.pop()
            self.removeItem(o)
        self.__links = set()
        self.node_baseid = 0
        self.link_baseid = 0
        init_router_id()
        init_atmsw_id()
        init_atmbr_id()
        init_ethsw_id()
        init_frsw_id()
        init_emu_id()
        init_cloud_id()
        init_decoration_id()
        self.cleanDynagen()

    def getNode(self, id):
        """ Returns the node corresponding to id
        """

        if self.__nodes.has_key(id):
            return self.__nodes[id]
        else:
            return None

    def getNodeID(self, node_name):
        """ Returns the id corresponding to node_name
        """
        for (id, node) in globals.GApp.topology.nodes.iteritems():
            if node.hostname == node_name:
                return (id)
        return None

    def __getNodes(self):
        """ Return topology nodes
        """

        return self.__nodes

    def __setNodes(self, value):
        """ Set the topology nodes (disabled)
        """

        self.__nodes = value

    nodes = property(__getNodes, __setNodes, doc='Property of nodes topology')
    
    def __getLinks(self):
        """ Return topology links
        """

        return self.__links

    links = property(__getLinks, doc='Property of links topology')

    def useExternalHypervisor(self, node, hypervisors):
        """ Connection to an external hypervisor
        """

        # if multiple hypervisors, then load balance
        if len(hypervisors) > 1:
            selected_hypervisor = None
            hypervisor_min_ram = 99999
            for hypervisor_key in hypervisors:
                hypervisor_conf = globals.GApp.hypervisors[hypervisor_key]
                if  hypervisor_conf.used_ram < hypervisor_min_ram:
                    hypervisor_min_ram = hypervisor_conf.used_ram
                    selected_hypervisor = hypervisor_key
            if not selected_hypervisor:
                debug('No hypervisor found for load-balancing!')
                selected_hypervisor = hypervisors[0]
            external_hypervisor_key = selected_hypervisor
        else:
            external_hypervisor_key = hypervisors[0]
        globals.GApp.hypervisors[external_hypervisor_key].used_ram += node.default_ram
        (host, port) = external_hypervisor_key.rsplit(':',  1)

        if self.dynagen.dynamips.has_key(external_hypervisor_key):
            debug("Use an external hypervisor: " + external_hypervisor_key)
            dynamips_hypervisor = self.dynagen.dynamips[external_hypervisor_key]
        else:
            debug("Connection to an external hypervisor: " + external_hypervisor_key)
            hypervisor_conf = globals.GApp.hypervisors[external_hypervisor_key]
            # use project workdir in priority
            if globals.GApp.workspace.projectWorkdir:
                self.dynagen.defaults_config['workingdir'] =  globals.GApp.workspace.projectWorkdir
            elif hypervisor_conf.workdir:
                self.dynagen.defaults_config['workingdir'] =  hypervisor_conf.workdir
            dynamips_hypervisor = self.dynagen.create_dynamips_hypervisor(host, int(port))
            if not dynamips_hypervisor:
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Hypervisor"),
                                           unicode(translate("Topology", "Can't connect to the external hypervisor on %s")) % external_hypervisor_key)
                if self.dynagen.dynamips.has_key(external_hypervisor_key):
                    del self.dynagen.dynamips[external_hypervisor_key]
                return False
            self.dynagen.get_defaults_config()
            self.dynagen.update_running_config()
            dynamips_hypervisor.configchange = True
            dynamips_hypervisor.udp = hypervisor_conf.baseUDP
            dynamips_hypervisor.starting_udp = hypervisor_conf.baseUDP
            dynamips_hypervisor.baseconsole = hypervisor_conf.baseConsole
        node.set_hypervisor(dynamips_hypervisor)
        return True

    def preConfigureNode(self, node, image_conf):
        """ Apply settings on node
        """

        debug("Set image " + image_conf.filename)
        node.set_image(image_conf.filename, image_conf.chassis)
        if image_conf.default_ram:
            # force default ram
            save = node.default_ram
            node.default_ram = 0
            node.set_int_option('ram', image_conf.default_ram)
            node.default_ram = save
        if image_conf.idlepc:
            debug("Set idlepc " + image_conf.idlepc)
            node.set_string_option('idlepc', image_conf.idlepc)
        if globals.GApp.systconf['dynamips'].mmap:
            debug("Enable mmap")
            node.set_string_option('mmap', True)
        else:
            debug("Disable mmap")
            node.set_string_option('mmap', False)
        if globals.GApp.systconf['dynamips'].sparsemem:
            debug("Enable sparse memory")
            node.set_string_option('sparsemem', True)
        if globals.GApp.systconf['dynamips'].ghosting:
            debug("Enable Ghost IOS")
            node.set_ghostios(True)
        if globals.GApp.systconf['dynamips'].jitsharing:
            debug("Enable JIT blocks sharing")
            node.set_jitsharing(True)

    def emuDeviceSetup(self, node):
        """ Start a connection to an Emulated device & set defaults
        """

        if globals.GApp.systconf['qemu'].enable_QemuManager:
            host = globals.GApp.systconf['qemu'].QemuManager_binding
            port = globals.GApp.systconf['qemu'].qemuwrapper_port
            if globals.GApp.QemuManager.startQemu(port) == False:
                return False
        else:
            external_hosts = globals.GApp.systconf['qemu'].external_hosts
            
            if len(external_hosts) == 0:
                QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "External Qemuwrapper"), 
                                          translate("Topology", "Please register at least one external Qemuwrapper"))
                return False

            if len(external_hosts) > 1:
                (selection,  ok) = QtGui.QInputDialog.getItem(globals.GApp.mainWindow, translate("Topology", "External Qemuwrapper"),
                                                              translate("Topology", "Please choose your external Qemuwrapper"), external_hosts, 0, False)
                if ok:
                    qemuwrapper = unicode(selection)
                else:
                    return False
            else:
                qemuwrapper = external_hosts[0]

            host = qemuwrapper
            if ':' in host:
                (host, port) = host.split(':')
                port = int(port)
            else:
                port = 10525
        
        qemu_name = host + ':' + str(port)
        debug('Qemuwrapper: ' + qemu_name)
        if not self.dynagen.dynamips.has_key(qemu_name):
            #create the Qemu instance and add it to global dictionary
            self.dynagen.dynamips[qemu_name] = qlib.Qemu(host, port)
            self.dynagen.dynamips[qemu_name].reset()
            if globals.GApp.systconf['qemu'].enable_QemuManager or host == 'localhost':
                self.dynagen.dynamips[qemu_name].qemupath = globals.GApp.systconf['qemu'].qemu_path
                self.dynagen.dynamips[qemu_name].qemuimgpath = globals.GApp.systconf['qemu'].qemu_img_path

            self.dynagen.dynamips[qemu_name].baseconsole = globals.GApp.systconf['qemu'].qemuwrapper_baseConsole
            self.dynagen.dynamips[qemu_name].baseudp = globals.GApp.systconf['qemu'].qemuwrapper_baseUDP
            self.dynagen.get_defaults_config()
            self.dynagen.update_running_config()
            self.dynagen.dynamips[qemu_name].configchange = True
            
            if globals.GApp.systconf['qemu'].enable_QemuManager or host == 'localhost':
                if globals.GApp.workspace.projectWorkdir:
                    workdir = globals.GApp.workspace.projectWorkdir
                elif globals.GApp.systconf['qemu'].qemuwrapper_workdir:
                    workdir = globals.GApp.systconf['qemu'].qemuwrapper_workdir
                else:
                    realpath = os.path.realpath(self.dynagen.global_filename)
                    workdir = os.path.dirname(realpath)
                try:
                    self.dynagen.dynamips[qemu_name].workingdir = workdir
                except lib.DynamipsError, msg:
                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Qemuwrapper error"),  unicode(workdir + ': ') + unicode(msg))
                    del self.dynagen.dynamips[qemu_name]
                    return False

        node.set_hypervisor(self.dynagen.dynamips[qemu_name])

        return True
        
    def addNodeFromScene(self, node):
        """ Add node in the topology, called from Scene
            node: object
        """

        command = undo.AddNode(self, node)
        self.undoStack.push(command)
        
    def addNode(self, node, fromScene=False):
        """ Add node in the topology
            node: object
        """

        try:
            if isinstance(node, IOSRouter):
                if len(globals.GApp.iosimages.keys()) == 0:
                    # no IOS images configured, users have to register an IOS
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "IOS image"), translate("Topology", "Please register at least one IOS image"))
                    return False

                image_to_use = None
                selected_images = []
                for (image, conf) in globals.GApp.iosimages.iteritems():
                    if conf.platform == node.platform:
                        selected_images.append(image)

                if len(selected_images) == 0:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "IOS image"),
                                              unicode(translate("Topology", "No image for platform %s")) % node.platform)
                    return False

                if len(selected_images) > 1:
                    for image in selected_images:
                        conf = globals.GApp.iosimages[image]
                        if conf.default:
                            image_to_use = image
                            break
                    if not image_to_use:
                        (selection,  ok) = QtGui.QInputDialog.getItem(globals.GApp.mainWindow, translate("Topology", "IOS image"),
                                                                      translate("Topology", "Please choose an image"), selected_images, 0, False)
                        if ok:
                            image_to_use = unicode(selection)
                        else:
                            return False
                else:
                    image_to_use = selected_images[0]

                image_conf = globals.GApp.iosimages[image_to_use]
                debug("Use image: " + image_to_use)
                if image_conf.default_ram:
                    debug("Set default RAM: " + str(image_conf.default_ram))
                    node.default_ram = image_conf.default_ram
                if len(image_conf.hypervisors) == 0:
                    # no hypervisor selected, allocate a new hypervisor for the node
                    if globals.GApp.systconf['dynamips'].path == '':
                        QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "Hypervisor"), translate("Topology", "Please configure the path to Dynamips"))
                        return False
                    if not globals.GApp.HypervisorManager:
                        QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "Hypervisor"), translate("Topology", "Please test the path to Dynamips in preferences"))
                        return False
                    if not globals.GApp.HypervisorManager.allocateHypervisor(node):
                        return False
                    # give a warning if the IOS path is not accessible
                    if not os.access(image_conf.filename, os.F_OK):
                        QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "IOS image"), unicode(translate("Topology", "%s seems to not exist, please check")) % image_conf.filename)
                else:
                    # use an external hypervisor
                    if self.useExternalHypervisor(node, image_conf.hypervisors) == False:
                        return False
                self.preConfigureNode(node, image_conf)

            if isinstance(node, QemuDevice):

                if len(globals.GApp.qemuimages) == 0:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "Qemu image"), translate("Topology", "Please configure a Qemu image"))
                    return False
               
                images = []
                for name in globals.GApp.qemuimages.keys():
                    images.append(name)
                
                if len(globals.GApp.qemuimages) > 1:

                    (selection,  ok) = QtGui.QInputDialog.getItem(globals.GApp.mainWindow, translate("Topology", "Qemu image"),
                                                                      translate("Topology", "Please choose an image"), images, 0, False)
                    if ok:
                        image_to_use = unicode(selection)
                    else:
                        return False
                    conf = globals.GApp.qemuimages[image_to_use]
                else:
                    conf = globals.GApp.qemuimages[images[0]]

                # give a warning if the Qemu image path is not accessible
                if not os.access(conf.filename, os.F_OK) and globals.GApp.systconf['qemu'].enable_QemuManager:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "Qemu image"), unicode(translate("Topology", "%s seems to not exist, please check")) % conf.filename)

                if self.emuDeviceSetup(node) == False:
                    return False
                
                debug("Set default image " + conf.filename + " for node type %s, model %r" % (type(node), node.model))
                node.set_image(conf.filename, node.model)
                node.set_int_option('ram', conf.memory)
                node.set_string_option('netcard', conf.nic)
                node.set_string_option('kqemu', conf.kqemu)
                node.set_string_option('kvm', conf.kvm)                
                node.set_string_option('options', conf.options)

            if isinstance(node, JunOS):

                if not globals.GApp.systconf['qemu'].default_junos_image:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "JunOS image"), translate("Topology", "Please configure a default JunOS image"))
                    return False
                
                # give a warning if the JunOS image path is not accessible
                if not os.access(globals.GApp.systconf['qemu'].default_junos_image, os.F_OK) and globals.GApp.systconf['qemu'].enable_QemuManager:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "JunOS image"), unicode(translate("Topology", "%s seems to not exist, please check")) % globals.GApp.systconf['qemu'].default_junos_image)
                
                if self.emuDeviceSetup(node) == False:
                    return False
                
                debug("Set default image " + globals.GApp.systconf['qemu'].default_junos_image + " for node type %s, model %r" % (type(node), node.model))
                node.set_image(globals.GApp.systconf['qemu'].default_junos_image, node.model)
                node.set_int_option('ram', globals.GApp.systconf['qemu'].default_junos_memory)
                node.set_string_option('netcard', globals.GApp.systconf['qemu'].default_junos_nic)
                node.set_string_option('kqemu', globals.GApp.systconf['qemu'].default_junos_kqemu)
                node.set_string_option('kvm', globals.GApp.systconf['qemu'].default_junos_kvm)                
                node.set_string_option('options', globals.GApp.systconf['qemu'].default_junos_options)
                
            if isinstance(node, IDS):

                if not globals.GApp.systconf['qemu'].default_ids_image1 or not globals.GApp.systconf['qemu'].default_ids_image2:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "IDS images"), translate("Topology", "Please configure the default IDS images"))
                    return False
                
                # give a warning if the IDS image paths are not accessible
                if not os.access(globals.GApp.systconf['qemu'].default_ids_image1, os.F_OK) and globals.GApp.systconf['qemu'].enable_QemuManager:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "IDS images"), unicode(translate("Topology", "%s seems to not exist, please check")) % globals.GApp.systconf['qemu'].default_ids_image1)

                # give a warning if the IDS image paths are not accessible
                if not os.access(globals.GApp.systconf['qemu'].default_ids_image2, os.F_OK) and globals.GApp.systconf['qemu'].enable_QemuManager:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "IDS images"), unicode(translate("Topology", "%s seems to not exist, please check")) % globals.GApp.systconf['qemu'].default_ids_image2)
          
                if self.emuDeviceSetup(node) == False:
                    return False

                # No default image for IDS
                node.set_image('None', node.model)
                debug("Set image1 " + globals.GApp.systconf['qemu'].default_ids_image1 + " for node type %s, model %r" % (type(node), node.model))
                debug("Set image2 " + globals.GApp.systconf['qemu'].default_ids_image2 + " for node type %s, model %r" % (type(node), node.model))
                node.set_string_option('image1', globals.GApp.systconf['qemu'].default_ids_image1)
                node.set_string_option('image2', globals.GApp.systconf['qemu'].default_ids_image2)
                node.set_int_option('ram', globals.GApp.systconf['qemu'].default_ids_memory)
                node.set_string_option('netcard', globals.GApp.systconf['qemu'].default_ids_nic)
                node.set_string_option('kqemu', globals.GApp.systconf['qemu'].default_ids_kqemu)
                node.set_string_option('kvm', globals.GApp.systconf['qemu'].default_ids_kvm)                
                node.set_string_option('options', globals.GApp.systconf['qemu'].default_ids_options)

            if isinstance(node, ASA):

                if not globals.GApp.systconf['qemu'].default_asa_kernel:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "ASA kernel"), translate("Topology", "Please configure a default ASA kernel"))
                    return False
                
                if not globals.GApp.systconf['qemu'].default_asa_initrd:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "ASA initrd"), translate("Topology", "Please configure a default ASA initrd"))
                    return False
                

                # give a warning if the ASA initrd path is not accessible
                if not os.access(globals.GApp.systconf['qemu'].default_asa_initrd, os.F_OK) and globals.GApp.systconf['qemu'].enable_QemuManager:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "ASA initrd"), unicode(translate("Topology", "%s seems to not exist, please check")) % globals.GApp.systconf['qemu'].default_asa_initrd)
             
                # give a warning if the ASA kernel path is not accessible
                if not os.access(globals.GApp.systconf['qemu'].default_asa_kernel, os.F_OK) and globals.GApp.systconf['qemu'].enable_QemuManager:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "ASA kernel"), unicode(translate("Topology", "%s seems to not exist, please check")) % globals.GApp.systconf['qemu'].default_asa_kernel)
   
                if self.emuDeviceSetup(node) == False:
                    return False
                
                debug("Set default initrd " + globals.GApp.systconf['qemu'].default_asa_initrd + " for node type %s, model %r" % (type(node), node.model))
                debug("Set default kernel " + globals.GApp.systconf['qemu'].default_asa_kernel + " for node type %s, model %r" % (type(node), node.model))
                
                # No image for ASA
                node.set_image('None', node.model)
                node.set_int_option('ram', globals.GApp.systconf['qemu'].default_asa_memory)
                node.set_string_option('netcard', globals.GApp.systconf['qemu'].default_asa_nic)
                node.set_string_option('kqemu', globals.GApp.systconf['qemu'].default_asa_kqemu)
                node.set_string_option('kvm', globals.GApp.systconf['qemu'].default_asa_kvm)     
                node.set_string_option('initrd', globals.GApp.systconf['qemu'].default_asa_initrd)
                node.set_string_option('kernel', globals.GApp.systconf['qemu'].default_asa_kernel)
                node.set_string_option('kernel_cmdline', globals.GApp.systconf['qemu'].default_asa_kernel_cmdline)
                node.set_string_option('options', globals.GApp.systconf['qemu'].default_asa_options)

            if isinstance(node, FW):
                
                if not globals.GApp.systconf['qemu'].default_pix_image:
                    QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "PIX image"), translate("Topology", "Please configure a default PIX image"))
                    return False
                    
                # give a warning if the PIX image path is not accessible
                    if not os.access(globals.GApp.systconf['qemu'].default_pix_image, os.F_OK) and globals.GApp.systconf['qemu'].enable_QemuManager:
                        QtGui.QMessageBox.warning(globals.GApp.mainWindow, translate("Topology", "PIX image"), unicode(translate("Topology", "%s seems to not exist, please check")) % globals.GApp.systconf['qemu'].default_pix_image)
                if self.emuDeviceSetup(node) == False:
                    return False
                
                debug("Set default image " + globals.GApp.systconf['qemu'].default_pix_image + " for node type %s, model %r" % (type(node), node.model))
                node.set_image(globals.GApp.systconf['qemu'].default_pix_image, node.model)
                node.set_int_option('ram', globals.GApp.systconf['qemu'].default_pix_memory)
                node.set_string_option('netcard', globals.GApp.systconf['qemu'].default_pix_nic)
                node.set_string_option('key', globals.GApp.systconf['qemu'].default_pix_key)
                node.set_string_option('serial', globals.GApp.systconf['qemu'].default_pix_serial)
                node.set_string_option('kqemu', globals.GApp.systconf['qemu'].default_pix_kqemu)
                node.set_string_option('options', globals.GApp.systconf['qemu'].default_pix_options)

            QtCore.QObject.connect(node, QtCore.SIGNAL("Add link"), globals.GApp.scene.slotAddLink)
            QtCore.QObject.connect(node, QtCore.SIGNAL("Delete link"), globals.GApp.scene.slotDeleteLink)

            self.__nodes[node.id] = node
            self.addItem(node)

            if node.configNode() == False:
                self.deleteNode(node.id)

        except (lib.DynamipsVerError, lib.DynamipsError), msg:
            if isinstance(node, IOSRouter):
                # check if dynamips can create its files
                if node.hypervisor:
                    dynamips_files = glob.glob(os.path.normpath(node.hypervisor.workingdir) + os.sep + node.platform + '?' + node.hostname + '*')
                    for file in dynamips_files:
                        if not os.access(file, os.W_OK):
                            print "Warning: " + file + " is not writable because of different rights, please delete this file manually if dynamips was not able to create this router"
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Dynamips error"),  unicode(msg))
            self.deleteNode(node.id)
            return False
        except (lib.DynamipsErrorHandled, socket.error):
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Dynamips error"), translate("Topology", "Connection lost"))
            self.deleteNode(node.id)
            return False

        globals.GApp.mainWindow.treeWidget_TopologySummary.refresh()
        debug("Running config: " + str(self.dynagen.running_config))
        self.changed = True
        return True

    def deleteNodeFromScene(self, id):
        """ Delete a node from the topology, called from Scene
        """

        node = self.__nodes[id]
        command = undo.DeleteNode(self, node)
        self.undoStack.push(command)
        
    def deleteNode(self, id):
        """ Delete a node from the topology
        """

        if not self.__nodes.has_key(id):
            return

        node = self.__nodes[id]
        if isinstance(node, IOSRouter):
            try:

                router = node.get_dynagen_device()
                if globals.GApp.systconf['dynamips'].HypervisorManager_binding == router.dynamips.host and \
                    globals.GApp.iosimages.has_key(globals.GApp.systconf['dynamips'].HypervisorManager_binding + ':' + router.image):
                    # internal hypervisor
                    image_conf = globals.GApp.iosimages[globals.GApp.systconf['dynamips'].HypervisorManager_binding + ':' + router.image]
                    if globals.GApp.HypervisorManager and len(image_conf.hypervisors) == 0:
                        globals.GApp.HypervisorManager.unallocateHypervisor(node, router.dynamips.port)
                else:
                    # external hypevisor
                    external_hypervisor_key = router.dynamips.host + ':' + str(router.dynamips.port)
                    if globals.GApp.hypervisors.has_key(external_hypervisor_key):
                        globals.GApp.hypervisors[external_hypervisor_key].used_ram -= node.default_ram
                        if globals.GApp.hypervisors[external_hypervisor_key].used_ram < 0:
                            globals.GApp.hypervisors[external_hypervisor_key].used_ram = 0
                    
                if router.jitsharing_group != None:
                    last_jitgroup_number = True
                    for device in router.dynamips.devices:
                        if device.jitsharing_group != None and router.jitsharing_group == device.jitsharing_group and device.name != router.name:
                            last_jitgroup_number = False
                            break
                    if last_jitgroup_number:
                        # basename doesn't work on Unix with Windows paths, so let's use this little trick
                        image = router.image
                        if not sys.platform.startswith('win') and image[1] == ":":
                            image = image[2:]
                            image = image.replace("\\", "/")
                        imagename = os.path.basename(image)
                        del router.dynamips.jitsharing_groups[imagename]
                        
            except:
                pass

        self.removeItem(node)
        del self.__nodes[id]
        globals.GApp.mainWindow.treeWidget_TopologySummary.refresh()
        # Work-around QGraphicsSvgItem caching bug:
        # Forcing to clear the QPixmapCache on node delete.
        # FIXME: in Qt 4.4
        QtGui.QPixmapCache.clear()
        self.changed = True

    def recordLink(self, srcid, srcif, dstid, dstif, src_node, dest_node):
        """ Record the link in the topology
        """

        multi = 0
        d1 = 0
        d2 = 1
        edges = src_node.getEdgeList()
        for edge in edges:
            if edge.dest.hostname == dest_node.hostname:
                d1 += 1
            if edge.source.hostname == dest_node.hostname:
                d2 += 1
        
        if len(edges) > 0:
            if d2 - d1 == 2:
                srcid, dstid = dstid, srcid
                srcif, dstif = dstif, srcif
                src_node, dest_node = dest_node, src_node
                multi = d1 + 1
            elif d1 >= d2:
                srcid, dstid = dstid, srcid
                srcif, dstif = dstif, srcif
                src_node, dest_node = dest_node, src_node
                multi = d2
            else:
                multi = d1

        # MAX 7 links on the scene between 2 nodes
        if multi > 3:
            multi = 0
        
        if (globals.currentLinkType == globals.Enum.LinkType.Serial or globals.currentLinkType == globals.Enum.LinkType.ATM) or \
            (globals.currentLinkType == globals.Enum.LinkType.Manual and ((srcif[0] == 's' or srcif[0] == 'a' or dstif[0] == 's' or dstif[0] == 'a') or \
            (isinstance(src_node, ATMSW) or isinstance(src_node, FRSW) or isinstance(dest_node, ATMSW) or isinstance(dest_node, FRSW)))):
            # interface is serial or ATM
            link = Serial(self.__nodes[srcid], srcif, self.__nodes[dstid], dstif, Multi=multi)
        else:
            # by default use an ethernet link
            link = Ethernet(self.__nodes[srcid], srcif, self.__nodes[dstid], dstif, Multi=multi)

        self.__links.add(link)
        self.addItem(link)

    def updateStates(self, src_node, dst_node):
        """ Start nodes that are always on and update interface states
        """
    
        try:
            # start nodes that are always on
            if not isinstance(src_node, IOSRouter) and not isinstance(src_node, AnyEmuDevice):
                src_node.startNode()
            elif src_node.state == 'running':
                src_node.startupInterfaces()
            if not isinstance(dst_node, IOSRouter) and not isinstance(dst_node, AnyEmuDevice):
                dst_node.startNode()
            elif dst_node.state == 'running':
                dst_node.startupInterfaces()
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Dynamips error"),  unicode(msg))
            return False
        return True
        
    def addLinkFromScene(self, srcid, srcif, dstid, dstif):
        """ Add a link to the topology, called from Scene
        """

        command = undo.AddLink(self, srcid, srcif, dstid, dstif)
        self.undoStack.push(command)
        if command.getStatus() == False:
            self.undoStack.undo()
            return False
        return True
        
    def addLink(self, srcid, srcif, dstid, dstif, draw=True):
        """ Add a link to the topology
        """

        src_node = globals.GApp.topology.getNode(srcid)
        dst_node = globals.GApp.topology.getNode(dstid)
        # special cases
        if isinstance(src_node, DecorativeNode) or isinstance(dst_node, DecorativeNode):
            self.recordLink(srcid, srcif, dstid, dstif, src_node, dst_node)
            if isinstance(src_node, DecorativeNode):
                src_node.startNode()
            elif src_node.state == 'running':
                src_node.startupInterfaces()
            if isinstance(dst_node, DecorativeNode):
                dst_node.startNode()
            elif dst_node.state == 'running':
                dst_node.startupInterfaces()
            return
        elif not isinstance(src_node, IOSRouter) and not isinstance(dst_node, IOSRouter):

#            if (isinstance(src_node, ETHSW) and not type(dst_node) in (IOSRouter, Cloud, QemuDevice, FW, ASA, JunOS, IDS)) or (isinstance(dst_node, ETHSW) and not type(src_node) in (IOSRouter, Cloud, QemuDevice, FW, ASA, JunOS, IDS)) \
#                or (type(src_node) in (ATMSW, FRSW, ATMBR) and not isinstance(dst_node, IOSRouter)) or (type(dst_node) in (ATMSW, FRSW, ATMBR) and not isinstance(src_node, IOSRouter)) \
#                or (isinstance(src_node, AnyEmuDevice) and isinstance(dst_node, Cloud)) or (isinstance(dst_node, AnyEmuDevice) and isinstance(src_node, Cloud)):
#                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Connection"),  translate("Topology", "Can't connect these devices"))
#                return False
            #if (isinstance(dst_node, Cloud) or isinstance(dst_node,AnyEmuDevice)) and isinstance(src_node, ETHSW):
            if not src_node.hypervisor:
                debug('Allocate a hypervisor for ethsw ' + src_node.hostname)
                if globals.GApp.HypervisorManager and not globals.GApp.HypervisorManager.allocateHypervisor(src_node):
                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Connection"),  translate("Topology", "You have to connect at least one router to the switch"))
                    return False

            #elif (isinstance(src_node, Cloud) or isinstance(src_node, AnyEmuDevice)) and isinstance(dst_node, ETHSW):
            if not dst_node.hypervisor:
                debug('Allocate a hypervisor for ethsw ' + dst_node.hostname)
                if globals.GApp.HypervisorManager and not globals.GApp.HypervisorManager.allocateHypervisor(dst_node):
                    QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Connection"),  translate("Topology", "You have to connect at least one router to the switch"))
                    return False

        else:
            if not isinstance(src_node, IOSRouter) and not isinstance(src_node, Cloud) and not isinstance(src_node, AnyEmuDevice) and not src_node.hypervisor:
                debug('Set hypervisor ' + dst_node.hypervisor.host + ':' + str(dst_node.hypervisor.port) + ' to ' + src_node.hostname)
                src_node.set_hypervisor(dst_node.hypervisor)
            elif not isinstance(dst_node, IOSRouter) and not isinstance(dst_node, Cloud) and not isinstance(dst_node, AnyEmuDevice) and not dst_node.hypervisor:
                debug('Set hypervisor ' + src_node.hypervisor.host + ':' + str(src_node.hypervisor.port) + ' to ' + dst_node.hostname)
                dst_node.set_hypervisor(src_node.hypervisor)

        try:
            if isinstance(src_node, IOSRouter) or isinstance(src_node, AnyEmuDevice) or type(src_node) in (ETHSW, ATMSW, ATMBR, FRSW):
                srcdev = src_node.get_dynagen_device()
                if type(dst_node) == Cloud:
                    debug('Connect link from ' + srcdev.name + ' ' + srcif +' to ' + dstif)
                    self.dynagen.connect(srcdev, srcif, dstif)
                else:
                    dstdev = dst_node.get_dynagen_device()
                    debug('Connect link from ' + srcdev.name + ' ' + srcif +' to ' + dstdev.name + ' ' + dstif)
                    self.dynagen.connect(srcdev, srcif, dstdev.name + ' ' + dstif)
            elif isinstance(dst_node, IOSRouter) or isinstance(dst_node, AnyEmuDevice) or type(dst_node) in (ETHSW, ATMSW, ATMBR, FRSW):
                dstdev = dst_node.get_dynagen_device()
                if type(src_node) == Cloud:
                    debug('Connect link from ' + dstdev.name + ' ' + srcif +' to ' + dstif)
                    self.dynagen.connect(dstdev, dstif, srcif)
                else:
                    srcdev = src_node.get_dynagen_device()
                    debug('Connect link from ' + dstdev.name + ' ' + srcif +' to ' + srcdev.name + ' ' + dstif)
                    self.dynagen.connect(dstdev, dstif, srcdev.name + ' ' + srcif)

        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Dynamips error"),  unicode(msg))
            return False
        except (lib.DynamipsErrorHandled, socket.error):
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Dynamips error"), translate("Topology", "Connection lost"))
            return False

        if draw:
            self.recordLink(srcid, srcif, dstid, dstif, src_node, dst_node)

        try:
            # start nodes that are always on
            if not isinstance(src_node, IOSRouter) and not isinstance(src_node, AnyEmuDevice):
                src_node.startNode()
            elif src_node.state == 'running':
                src_node.startupInterfaces()
            if not isinstance(dst_node, IOSRouter) and not isinstance(dst_node, AnyEmuDevice):
                dst_node.startNode()
            elif dst_node.state == 'running':
                dst_node.startupInterfaces()
        except lib.DynamipsError, msg:
            QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Dynamips error"),  unicode(msg))
            return False

        globals.GApp.mainWindow.treeWidget_TopologySummary.refresh()
        self.dynagen.update_running_config()
        self.changed = True

        return True

    def deleteLinkFromScene(self, link):
        """ Delete a link from the topology, called from Scene
        """
        
        command = undo.DeleteLink(self, link)
        self.undoStack.push(command)
        if command.getStatus() == False:
            self.undoStack.undo()
        
    def deleteLink(self, link):
        """ Delete a link from the topology
        """

        if not isinstance(link.source, DecorativeNode) and not isinstance(link.dest, DecorativeNode):
            # not a decorative device
            try:
                if isinstance(link.source, IOSRouter) or isinstance(link.source, AnyEmuDevice):
                    srcdev = link.source.get_dynagen_device()
                    if type(link.dest) == Cloud:
                        debug('Disconnect link from ' + srcdev.name + ' ' + link.srcIf +' to ' + link.destIf)
                        self.dynagen.disconnect(srcdev, link.srcIf, link.destIf, automatically_remove_unused_slot=False)
                    else:
                        dstdev = link.dest.get_dynagen_device()
                        debug('Disconnect link from ' + srcdev.name + ' ' + link.srcIf +' to ' + dstdev.name + ' ' + link.destIf)
                        self.dynagen.disconnect(srcdev, link.srcIf, dstdev.name + ' ' + link.destIf, automatically_remove_unused_slot=False)
                    link.source.set_config(link.source.get_config())
                elif isinstance(link.dest, IOSRouter) or isinstance(link.dest, AnyEmuDevice):
                    dstdev = link.dest.get_dynagen_device()
                    if type(link.source) == Cloud:
                        debug('Disconnect link from ' + dstdev.name + ' ' + link.destIf +' to ' + link.srcIf)
                        self.dynagen.disconnect(dstdev, link.destIf, link.srcIf, automatically_remove_unused_slot=False)
                    else:
                        srcdev = link.source.get_dynagen_device()
                        debug('Disconnect link from ' + dstdev.name + ' ' + link.destIf +' to ' + srcdev.name + ' ' + link.srcIf)
                        self.dynagen.disconnect(dstdev, link.destIf, srcdev.name + ' ' + link.srcIf, automatically_remove_unused_slot=False)
                    link.dest.set_config(link.dest.get_config())
            except lib.DynamipsError, msg:
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Dynamips error"),  unicode(msg))
                return False
            except (lib.DynamipsErrorHandled, socket.error):
                QtGui.QMessageBox.critical(globals.GApp.mainWindow, translate("Topology", "Dynamips error"), translate("Topology", "Connection lost"))
                return False

        link.source.deleteEdge(link)
        link.dest.deleteEdge(link)
        if link in self.__links:
            self.__links.remove(link)
            if link.labelSouceIf != None:
                globals.interfaceLabels[link.source.hostname + ' ' + link.srcIf] = link.labelSouceIf
                self.removeItem(link.labelSouceIf)
            if link.labelDestIf != None:
                globals.interfaceLabels[link.dest.hostname + ' ' + link.destIf] = link.labelDestIf
                self.removeItem(link.labelDestIf)
            self.removeItem(link)
        globals.GApp.mainWindow.treeWidget_TopologySummary.refresh()
        self.dynagen.update_running_config()
        self.changed = True
        return True
