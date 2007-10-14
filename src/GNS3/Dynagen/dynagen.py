#!/usr/bin/env python

"""
dynagen
Copyright (C) 2006  Greg Anuzelli

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

import sys, os, re, traceback
from console import Console
from dynamips_lib import Dynamips, PA_C7200_IO_FE, PA_A1, PA_FE_TX, PA_4T, PA_8T, \
    PA_4E, PA_8E, PA_POS_OC3, Router, C7200, C3600, Leopard_2FE, NM_1FE_TX, NM_1E, NM_4E, \
    NM_16ESW, NM_4T, DynamipsError, DynamipsWarning, Bridge, FRSW, ATMSW, ETHSW, \
    NIO_udp, NIO_linux_eth, NIO_gen_eth, NIO_tap, NIO_unix, NIO_vde, nosend, setdebug, \
    IDLEPROPGET, IDLEPROPSHOW, IDLEPROPSET, C2691, C3725, C3745, GT96100_FE, C2600, \
    CISCO2600_MB_1E, CISCO2600_MB_2E, CISCO2600_MB_1FE, CISCO2600_MB_2FE, PA_2FE_TX, \
    PA_GE, PA_C7200_IO_2FE, PA_C7200_IO_GE_E, C1700, CISCO1710_MB_1FE_1E, C1700_MB_1ETH, \
    DynamipsVerError, DynamipsErrorHandled, WICS, NM_CIDS, NM_NAM
from pemu_lib import Pemu, FW
from validate import Validator
from configobj import ConfigObj, flatten_errors
from optparse import OptionParser

# Constants
VERSION = '0.11.0.100107'
CONFIGSPECPATH = [ "/usr/share/dynagen", "/usr/local/share" ]
CONFIGSPEC = 'configspec'
INIPATH = [ "/etc", "/usr/local/etc" ]
INIFILE = 'dynagen.ini'
MODELTUPLE = (C1700, C2600, C2691, C3725, C3745, C3600, C7200)             # A tuple of known model objects
DEVICETUPLE = ('525', '1710', '1720', '1721', '1750', '1751', '1760', '2610', '2611', '2620', '2621', '2610XM', '2611XM', '2620XM', '2621XM', '2650XM', '2651XM', '2691', '3725', '3745', '3620', '3640', '3660', '7200')  # A tuple of known device names
ADAPTER_TRANSFORM = {
    "C7200-IO-FE" : PA_C7200_IO_FE,
    "C7200-IO-2FE" : PA_C7200_IO_2FE,
    "C7200-IO-GE-E" : PA_C7200_IO_GE_E,
    "PA-A1" : PA_A1,
    "PA-FE-TX" : PA_FE_TX,
    "PA-2FE-TX" : PA_2FE_TX,
    "PA-GE" : PA_GE,
    "PA-4T" : PA_4T,
    "PA-8T" : PA_8T,
    "PA-4E" : PA_4E,
    "PA-8E" : PA_8E,
    "PA-POS-OC3" : PA_POS_OC3,
    "NM-1FE-TX"  : NM_1FE_TX,
    "NM-1E"  : NM_1E,
    "NM-4E": NM_4E,
    "NM-4T": NM_4T,
    "NM-16ESW": NM_16ESW,
    "Leopard-2FE": Leopard_2FE,
    "GT96100-FE": GT96100_FE,
    "CISCO2600-MB-1E": CISCO2600_MB_1E,
    "CISCO2600-MB-2E": CISCO2600_MB_2E,
    "CISCO2600-MB-1FE": CISCO2600_MB_1FE,
    "CISCO2600-MB-2FE": CISCO2600_MB_2FE,
    "CISCO1710-MB-1FE-1E": CISCO1710_MB_1FE_1E,
    "C1700-MB-1ETH": C1700_MB_1ETH,
    "NM-CIDS": NM_CIDS,
    "NM-NAM": NM_NAM
}

# Globals
debuglevel = 0     # The debug level
globaludp = 10000   # The default base UDP port for NIO
notelnet = False    # Flag to disable telnet (for gDynagen)
useridledbfile = '' # The filespec of the idle database
useridledb = None   # Dictionary of idle-pc values from the user database, indexed by image name
handled = False     # An exception has been handled already
globalconfig = {}   # A global copy of the config that console.py can access
configurations = {} # A global copy of all b64 exported configurations from the network file indexed by devicename
ghosteddevices = {} # A dict of devices that will use ghosted IOS indexed by device name
ghostsizes = {}     # A dict of the sizes of the ghosts
dynamips = {}       # A dictionary of dynamips objects, indexed by dynamips server name
devices = {}        # Dictionary of device objects, indexed by name
bridges = {}        # Dictionary of bridge objects, indexed by name
autostart = {}      # Dictionary that tracks autostart, indexed by router name
interface_re = re.compile(r"""^(g|gi|f|fa|a|at|s|se|e|et|p|po|i|id|IDS-Sensor|an|Analysis-Module)([0-9]+)\/([0-9]+)$""",  re.IGNORECASE)     # Regex matching intefaces
interface_noport_re = re.compile(r"""^(g|gi|f|fa|a|at|s|se|e|et|p|po)([0-9]+)$""",  re.IGNORECASE)     # Regex matching intefaces with out a port (e.g. "f0")
number_re = re.compile(r"""^[0-9]*$""")                         # Regex matching numbers
mapint_re = re.compile(r"""^([0-9]*):([0-9]*)$""")              # Regex matching Frame Relay mappings or ATM vpi mappings
mapvci_re = re.compile(r"""^([0-9]*):([0-9]*):([0-9]*)$""")     # Regex matching ATM vci mappings
ethswint_re = re.compile(r"""^([0-9]+)""")                      # Regex mating a number (means an Ethernet switchport config)

# determine if we are in the debugger
try:
    DBGPHideChildren
except NameError:
    DEBUGGER = False
else:
    DEBUGGER = True

class Dynagen:
    """ Dynagen class
    """

    def setdefaults(self, router, defaults):
        """ Apply the global defaults to this router instance
        """
        for option in defaults:
            self.setproperty(router, option, defaults[option])

    def setproperty(self, device, option, value):
        """ If it is valid, set the option and return True. Otherwise return False
        """

        global configurations, ghosteddevices, globalconfig

        if type(device) in MODELTUPLE:
            # Is it a "simple" property? If so set it and forget it.
            if option in ('rom', 'clock', 'npe', 'ram', 'nvram', 'confreg', 'midplane', 'console', 'aux', 'mac', 'mmap', 'idlepc', 'exec_area', 'disk0', 'disk1', 'iomem', 'idlemax', 'idlesleep', 'oldidle', 'sparsemem'):
                setattr(device, option, value)
                return True
            # Is it a filespec? If so encase it in quotes to protect spaces
            if option in ('image', 'cnfg'):
                value = '"' + value + '"'
                setattr(device, option, value)
                return True

            # Is it a config? If so save it for later
            if option == 'configuration':
                configurations[device.name] = value

            if option == 'ghostios':
                ghosteddevices[device.name] = value

            if option == 'ghostsize':
                ghostsizes[device.name] = value

            # is it a slot designation?
            if option[:4].lower() == 'slot':
                try:
                    slot = int(option.split('=')[0][4:])
                except ValueError:
                    print "warning: ignoring unknown config item: " + option
                    return False

                # Attempt to insert the requested adapter in the requested slot
                # BaseAdapter will throw a DynamipsError if the adapter is not
                # supported in this slot, or if it is an invalid slot for this
                # device
                if value in ADAPTER_TRANSFORM:
                    device.slot[slot] = ADAPTER_TRANSFORM[value](device, slot)
                else:
                    self.doerror('Unknown adapter %s specified for slot %i on router: %s' % (value, slot, device.name))
                return True

            # is it a wic designation?
            if option[:3].lower() == 'wic':
                try:
                    (slot,subslot) = (int(option.split('/')[0][-1]), int(option.split('/')[1]))
                except IndexError:
                    print "warning: ignoring unknown config item: %s = %s" % (option, value)
                    return False
                except ValueError:
                    print "warning: ignoring unknown config item: %s = %s" % (option, value)
                    return False
                device.installwic(value, slot, subslot)
                return True
        return False


    def connect(self, router, source, dest):
        """ Connect a router to something
            router: a router object
            source: a string specifying the local interface
            dest: a string specifying a device and a remote interface, LAN, a raw NIO
        """

        match_obj = interface_re.search(source)
        if not match_obj:
            # is this an interface without a port designation (e.g. "f0")?
            match_obj = interface_noport_re.search(source)
            if not match_obj:
                return False
            else:
                (pa1, port1) = match_obj.group(1,2)
                slot1 = 0
        else:
            (pa1, slot1, port1) = match_obj.group(1,2,3)

        if pa1[:2].lower() == 'an':
            # need to use two chars for Analysis-Module
            pa1 = pa1[:2].lower()
        else:
            pa1 = pa1.lower()[0]        # Only care about first character
        slot1 = int(slot1)
        port1 = int(port1)
        try:
            (devname, interface) = dest.split(' ')
        except ValueError:
            # Must be either a NIO or malformed
            if not dest[:4].lower() == 'nio_':
                self.debug('Malformed destination:' + str(dest))
                return False
            try:
                self.debug('A NETIO: ' + str(dest))
                (niotype, niostring) = dest.split(':',1)
            except ValueError:
                self.debug('Malformed NETIO:' + str(dest))
                return False
            # Process the netio
            if niotype.lower() == 'nio_linux_eth':
                self.debug('NIO_linux_eth ' + str(dest))
                self.smartslot(router, pa1, slot1, port1)
                router.slot[slot1].nio(port1, nio=NIO_linux_eth(router.dynamips, interface=niostring))

            elif niotype.lower() == 'nio_gen_eth':
                self.debug('gen_eth ' + str(dest))
                self.smartslot(router, pa1, slot1, port1)
                router.slot[slot1].nio(port1, nio=NIO_gen_eth(router.dynamips, interface=niostring))

            elif niotype.lower() == 'nio_udp':
                self.debug('udp ' + str(dest))
                (udplocal, remotehost, udpremote) = niostring.split(':',2)
                self.smartslot(router, pa1, slot1, port1)
                router.slot[slot1].nio(port1, nio=NIO_udp(router.dynamips, int(udplocal), str(remotehost), int(udpremote)))

            elif niotype.lower() == 'nio_null':
                self.debug('nio null')
                self.smartslot(router, pa1, slot1, port1)
                router.slot[slot1].nio(port1, nio=NIO_null(router.dynamips))

            elif niotype.lower() == 'nio_tap':
                self.debug('nio tap ' + str(dest))
                self.smartslot(router, pa1, slot1, port1)
                router.slot[slot1].nio(port1, nio=NIO_tap(router.dynamips, niostring))

            elif niotype.lower() == 'nio_unix':
                self.debug('unix ' + str(dest))
                (unixlocal, unixremote) = niostring.split(':',1)
                self.smartslot(router, pa1, slot1, port1)
                router.slot[slot1].nio(port1, nio=NIO_unix(router.dynamips, unixlocal, unixremote))

            elif niotype.lower() == 'nio_vde':
                self.debug('vde ' + str(dest))
                (controlsock, localsock) = niostring.split(':',1)
                self.smartslot(router, pa1, slot1, port1)
                router.slot[slot1].nio(port1, nio=NIO_vde(router.dynamips, controlsock, localsock))

            else:
                # Bad NIO
                return False
            return True

        match_obj = interface_re.search(interface)
        if match_obj:
            # Connecting to another interface
            (pa2, slot2, port2) = match_obj.group(1,2,3)
        else:
            match_obj = interface_noport_re.search(interface)
            if match_obj:
                # Connecting to another "portless" interface e.g. "f0"
                (pa2, port2) = match_obj.group(1,2)
                slot2 = 0

        # If either of the interface formats matched...
        if match_obj:
            if pa2[:2].lower() == 'an':
                # need to use two chars for Analysis-Module
                pa2 = pa2[:2].lower()
            else:
                pa2 = pa2.lower()[0]        # Only care about first character

            slot2 = int(slot2)
            port2 = int(port2)
            # Does the device we are trying to connect to actually exist?
            if not devices.has_key(devname):
                line = router.name + ' ' + source + ' = ' + dest
                self.doerror('Nonexistent device "' + devname + '" in line: \n ' + line)

            # If interfaces don't exist, create them
            self.smartslot(router, pa1, slot1, port1)
            self.smartslot(devices[devname], pa2, slot2, port2)

            # Perform the connection, taking into account connections to pemu firewalls
            if isinstance(router, FW) and isinstance(devices[devname], Router):
                router.connect_to_dynamips(port1, devices[devname].dynamips, devices[devname].slot[slot2], pa2, port2)
            elif isinstance(router, FW) and isinstance(devices[devname], FW):
                router.connect_to_fw(port1, devices[devname] , port2)
            elif isinstance(router, Router) and isinstance(devices[devname], FW):
                devices[devname].connect_to_dynamips(port2, router.dynamips, router.slot[slot1], pa1, port1)
            else:
                # Must be router to router
                router.slot[slot1].connect(pa1, port1, devices[devname].dynamips, devices[devname].slot[slot2], pa2, port2)

            return True

        if devname.lower() == 'lan':
            self.debug('a LAN interface ' + str(dest))
            # If interface doesn't exist, create it
            self.smartslot(router, pa1, slot1, port1)
            if not bridges.has_key(interface):
                # If this LAN doesn't already exist, create it
                bridges[interface] = Bridge(router.dynamips, name=interface)
                if isinstance(router, FW):
                    router.connect_to_dynamips(port1, bridges[interface].dynamips, bridges[interface], 'f', 0)
                else:
                    router.slot[slot1].connect(pa1, port1, bridges[interface].dynamips, bridges[interface], 'f')
            return True

        match_obj = number_re.search(interface)
        if match_obj:
            port2 = int(interface)
            # Should be a swtich port
            if devname not in devices:
                self.debug('Unknown device ' + str(devname))
                return False

            self.debug('a switch port: ' + str(dest))
            # If interface doesn't exist, create it
            self.smartslot(router, pa1, slot1, port1)
            if devices[devname].adapter ==  'ETHSW':
                pa2 = 'f'       # Ethernet switches are FastEthernets (for our purposes anyway)
            elif devices[devname].adapter ==  'FRSW':
                pa2 = 's'       # Frame Relays switches are Serials
            elif devices[devname].adapter ==  'ATMSW':
                pa2 = 'a'       # And ATM switches are, well, ATM interfaces
            else:
                return False

            if isinstance(router, FW):
                router.connect_to_dynamips(port1, devices[devname].dynamips, devices[devname], pa2, port2)
            else:
                router.slot[slot1].connect(pa1, port1, devices[devname].dynamips, devices[devname], pa2 , port2)
            return True

        else:
            # Malformed
            self.debug('Malformed destination interface: ' + str(dest))
            return False


    def smartslot(self, router, pa, slot, port):
        """ Pick the right adapter for the desired interface type, and insert it
            router: a router object
            pa: a one or two character string 'gi', 'fa', 'et', 'se', 'at', or 'po'
            slot: slot number
            port: port number
        """

        if pa[:2].lower() == 'an':
            # Need to handle the Analysis-Module with two chars, because 'a' is an
            pa = pa[:2].lower()
        else:
            pa = pa[0].lower()

        if isinstance(router, FW):
            if pa == 'e' and port >= 0 and port < 6:
                router.add_interface(pa,port)
                return
            else:
                self.doerror("Invalid adapter '%s' specified for FW %s. FW only supports e0-6." % (pa, router.name))

        try:
            if router.slot[slot] != None:
                # Already a PA in this slot. Does this adapter already provide the
                # interface we need?
                try:
                    router.slot[slot].interfaces[pa][port]
                except (KeyError, IndexError):
                    # No it is not. Does this adapter provide WIC slots?
                    try:
                        router.slot[slot].wics[0]
                    except KeyError:
                        # No wic slots. Must be an error
                        self.doerror("Invalid slot %i specified for device %s" % (slot, router.name))
                    except IndexError:
                        self.doerror("Attempt to connect to non-existent interface in slot %i on device %s" % (slot, router.name))
                    else:
                        # Can the requested interface be provided by a WIC?
                        if (router.model == 'c2600' or router.model in ['c3725', 'c3745', 'c2691'] or (router.model == 'c1700' and router.chassis in ['1720', '1721', '1750', '1751', '1760'])) and (pa == 's' or pa == 'e'):
                            if pa == 'e' and (router.model != 'c1700' or router.chassis not in ['1720', '1721', '1750', '1751', '1760']):
                                # Ethernet WIC only supported in these 1700 models
                                self.doerror("Ethernet adapter not supported on port %i for device %s" % (port, router.name))

                            if pa == 'e': chosenwic = 'WIC-1ENET'
                            elif pa == 's': chosenwic = 'WIC-2T'

                            if router.model == 'c1700' and router.chassis in ['1751', '1760']:
                                # WIC selection is pretty straight-forward here
                                router.installwic(chosenwic, slot)
                                return True
                            else:
                                # Less obvious here.
                                # If you want an interface of a given type on port n,
                                # there either needs to already be interfaces of that same type
                                # in ports 0 - (n-1)
                                # If not, you need to have enough empty WIC slots to get you there
                                # What a mess.
                                # Since the number of cases is simple for now, I'll use a bunch of
                                # if ... then stuff. But ss the number of WICs supported increases
                                # I'll need to come up with some loftier logic.

                                if pa == 'e':
                                    for i in range(0, port+1):
                                        # install WIC-1ENETs until we've added enough to get he port we need
                                        router.installwic(chosenwic, slot)
                                    return True

                                if pa == 's':
                                    # just fill it up with WIC-2Ts until I come up a
                                    # better solution
                                    for i in range(0, (port/2)+1):
                                        router.installwic(chosenwic, slot)
                                    return True
                else:
                    return True
        except KeyError:
            self.doerror("Invalid slot %i specified on device %s" % (slot, router.name))
        except IndexError:
            self.doerror("Invalid slot %i specified on device %s" % (slot, router.name))

        """ Note to self: One of these days you should do this section right. Programatically build a matrix of
            default adapters for a given Adapter, model, slot, and chassis using this structure:
        smartslotmatrix = {
            'e' : {                     # Adapter
                '2600' : {              # Router Model
                    { '0' : {           # Slot
                        '2620':'1FE',   # Chassis (if applicable)
                        '2621':'2FE'
                    }
                }
            }
        }
        This would be a good idiom to use elsewhere within the app as well
        """

        if pa == 'g':
            if slot == 0:
                if port == 0:
                    router.slot[slot] = PA_C7200_IO_GE_E(router, slot)
                elif port >= 1 and port <= 3 and router.npe == 'npe-g2':
                    pass
                else:
                    self.doerror('Use of Gi0/1-3 requires use of an NPE-G2 on router: ' + router.name)

            else:
                router.slot[slot] = PA_GE(router, slot)

        if pa == 'f':
            if router.model == 'c3600':
                if router.chassis == '3660' and slot == 0:
                    router.slot[slot] = Leopard_2FE(router,slot)
                else:
                    router.slot[slot] = NM_1FE_TX(router, slot)
            elif router.model in ['c2691', 'c3725', 'c3745']:
                if slot == 0:
                    router.slot[slot] = GT96100_FE(router,slot)
                else:
                    router.slot[slot] = NM_1FE_TX(router, slot)
            elif router.model in ['c2600']:
                if slot == 0:
                    chassis2600transform = {
                        "2620"  : CISCO2600_MB_1FE,
                        "2621"  : CISCO2600_MB_2FE,
                        "2610XM": CISCO2600_MB_1FE,
                        "2611XM": CISCO2600_MB_2FE,
                        "2620XM": CISCO2600_MB_1FE,
                        "2621XM": CISCO2600_MB_2FE,
                        "2650XM": CISCO2600_MB_1FE,
                        "2651XM": CISCO2600_MB_2FE
                    }
                    try:
                        router.slot[slot] = chassis2600transform[router.chassis](router, slot)
                    except KeyError:
                        self.doerror("Chassis %s does not support FastEthernet adapter in slot 0 for device %s." % (router.chassis, router.name))
                else:
                    router.slot[slot] = NM_1FE_TX(router, slot)
            else:
                if slot == 0:
                    router.slot[slot] = PA_C7200_IO_2FE(router, slot)
                else:
                    router.slot[slot] = PA_2FE_TX(router, slot)
            return True

        if pa == 'e':
            if router.model == 'c2600':
                if slot == 0:
                    chassis2600transform = {
                        "2610"  : CISCO2600_MB_1E,
                        "2611"  : CISCO2600_MB_2E
                    }
                    try:
                        router.slot[slot] = chassis2600transform[router.chassis](router, slot)
                    except KeyError:
                        self.doerror("Chassis %s does not support Ethernet adapter in slot 0 for device %s." % (router.chassis, router.name))
                else:
                    router.slot[slot] = NM_4E(router, slot)
            elif router.model == 'c3600':
                router.slot[slot] = NM_4E(router, slot)
            elif router.model in ['c2691', 'c3725', 'c3745']:
                self.doerror("Unsuppported interface %s%i/%i specified for device: %s" % (pa, slot, port, router.name))
            elif router.model == 'c7200':
                router.slot[slot] = PA_8E(router, slot)
            elif router.model == 'c1700' and slot == 0:
                self.doerror("Unsuppported interface %s%i/%i specified for device: %s" % (pa, slot, port, router.name))
            else:
                self.doerror("Unsuppported interface %s%i/%i specified for device: %s" % (pa, slot, port, router.name))
            return True
        if pa == 's':
            if router.model in ['c2600']:
                self.doerror("Unsuppported interface %s%i/%i specified for device: %s" % (pa, slot, port, router.name))
            elif router.model in ['c2691', 'c3725', 'c3745', 'c3600']:
                router.slot[slot] = NM_4T(router, slot)
            elif router.model == 'c7200':
                router.slot[slot] = PA_8T(router, slot)
            elif router.model in ['c2691', 'c3725', 'c3745', 'c1700', 'c2600'] and slot == 0:
                self.doerror("Unsuppported interface %s%i/%i specified for device: %s" % (pa, slot, port, router.name))
            else:
                self.doerror("Unsuppported interface %s%i/%i specified for device: %s" % (pa, slot, port, router.name))
            return True
        if pa == 'a':
            if router.model in ['c2600', 'c2691', 'c3725', 'c3745', 'c3600']:
                self.doerror("Unsuppported interface %s%i/%i specified for device: %s" % (pa, slot, port, router.name))
            router.slot[slot] = PA_A1(router, slot)
            return True
        if pa == 'p':
            if router.model in ['c2600', 'c2691', 'c3725', 'c3745', 'c3600']:
                self.doerror("Unsuppported interface %s%i/%i specified for device: %s" % (pa, slot, port, router.name))
            router.slot[slot] = PA_POS_OC3(router, slot)
            return True
        if pa == 'i':
            router.slot[slot] = NM_CIDS(router, slot)
        if pa == 'an':
            router.slot[slot] = NM_NAM(router, slot)

        # Bad pa passed
        return False


    def switch_map(self, switch, source, dest):
        """ Apply a Frame Relay or ATM switch mapping
            switch: a FRSW or ATMSW instance
            source: a string specifying the source mapping
            dest: a string sepcifying the dest mapping
        """
        # Is this a FR / ATM vpi mapping?
        matchobj = mapint_re.search(source)
        if matchobj:
            (port1, map1) = map(int, matchobj.group(1,2))
            matchobj = mapint_re.search(dest)
            if not matchobj:
                print('*** Warning: ignoring invalid switch mapping entry %s = %s' % (source, dest))
                return False
            (port2, map2) = map(int, matchobj.group(1,2))
            if type(switch) == FRSW:
                # Forward
                switch.map(port1, map1, port2, map2)
                # And map the reverse
                switch.map(port2, map2, port1, map1)
                return True
            elif type(switch) == ATMSW:
                switch.mapvp(port1, map1, port2, map2)
                switch.mapvp(port2, map2, port1, map1)
                return True
            else:
                print('*** Warning: ignoring attempt to apply switch mapping to invalid device type: %s = %s' % (source, dest))
                return False
        # Is this an ATM VCI mapping?
        matchobj = mapvci_re.search(source)
        if matchobj:
            if type(switch) != ATMSW:
                print('*** Warning: ignoring invalid switch mapping entry %s = %s' % (source, dest))
                return False
            (port1, vp1, vc1) = map(int, matchobj.group(1,2,3))
            matchobj = mapvci_re.search(dest)
            if not matchobj:
                print('*** Warning: ignoring invalid switch mapping entry %s = %s' % (source, dest))
                return False
            (port2, vp2, vc2) = map(int, matchobj.group(1,2,3))
            if not matchobj:
                print('*** Warning: ignoring invalid switch mapping entry %s = %s' % (source, dest))
                return False
            switch.mapvc(port1, vp1, vc1, port2, vp2, vc2)
            switch.mapvc(port2, vp2, vc2, port1, vp1, vc1)
            return True

        print('*** Warning: ignoring invalid switch mapping entry %s = %s' % (source, dest))
        return False

    def open_config(self, FILENAME):
        """ Open the config file
        """

        # look for configspec in CONFIGSPECPATH and the same directory as dynagen
        realpath = os.path.realpath(sys.argv[0])
        self.debug('realpath ' + realpath)
        pathname = os.path.dirname(realpath)
        self.debug('pathname -> ' + pathname)
        CONFIGSPECPATH.append(pathname)
        for dir in CONFIGSPECPATH:
            configspec = dir +'/' + CONFIGSPEC
            self.debug('configspec -> ' + configspec)

            # Check to see if configuration file exists
            try:
                h=open(FILENAME)
                h.close()
                try:
                    config = ConfigObj(FILENAME, configspec=configspec, raise_errors=True)
                except SyntaxError, e:
                    print "\nError:"
                    print e
                    print e.line, '\n'
                    raw_input("Press ENTER to continue")
                    handled = True
                    sys.exit(1)

            except IOError:
               #doerror("Can't open configuration file")
               continue

        vtor = Validator()
        res = config.validate(vtor, preserve_errors=True)
        if res == True:
            self.debug('Passed validation')
        else:
            for entry in flatten_errors(config, res):
                # each entry is a tuple
                section_list, key, error = entry
                if key is not None:
                   section_list.append(key)
                else:
                    section_list.append('[missing section]')
                section_string = ', '.join(section_list)
                if error == False:
                    error = 'Missing value or section.'
                print section_string, ' = ', error
            raw_input("Press ENTER to continue")
            handled = True
            sys.exit(1)

        return config

    def import_config(self, FILENAME):
        """ Read in the config file and set up the network
        """
        global globalconfig, globaludp, handled, debuglevel
        connectionlist = []     # A list of router connections
        maplist = []            # A list of Frame Relay and ATM switch mappings
        ethswintlist = []       # A list of Ethernet Switch vlan mappings

        config = self.open_config(FILENAME)

        debuglevel = config['debug']
        if debuglevel > 0: setdebug(True)

        globalconfig = config           # Store the config in a global for access by console.py

        if debuglevel >= 3:
            self.debug("Top-level items:")
            for item in config.scalars:
                self.debug(item + ' = ' + str(config[item]))

        self.debug("Dynamips/PemuWrapper Servers:")
        for section in config.sections:
            server = config[section]
            if ' ' in server.name:
                # Must be a pemu server specification
                (emulator, host) = server.name.split(' ')
                if emulator == 'pemu':
                        #connect to the PEMU Wrapper
                        try:
                            #add ':10525' string to the name so that it does not conflict with name of dynamips server
                            pemu_name = host + ':10525'
                            #create the Pemu instance and add it to global dictionary
                            dynamips[pemu_name] = Pemu(host)
                            dynamips[pemu_name].reset()
                        except DynamipsError:
                            self.doerror('Could not connect to server: %s' % server.name)

                        if server['workingdir'] == None:
                            # If workingdir is not specified, set it to the same directory
                            # as the network file
                            realpath = os.path.realpath(FILENAME)
                            workingdir = os.path.dirname(realpath)
                        else:
                            workingdir = server['workingdir']
                        try:
                            # Encase workingdir in quotes to protect spaces
                            workingdir = '"' + workingdir + '"'
                            dynamips[pemu_name].workingdir = workingdir
                        except DynamipsError:
                            self.doerror('Could not set working directory to: %s on server: %s' % (workingdir, server.name))

                        devdefaults = {}
                        for key in DEVICETUPLE:
                            devdefaults[key] = {}

                        #handle the FW
                        for subsection in server.sections:
                            device = server[subsection]

                            if device.name in ['525']:
                                # Populate the appropriate dictionary
                                for scalar in device.scalars:
                                    if device[scalar] != None:
                                        devdefaults['525'][scalar] = device[scalar]
                                continue

                            # Create the device
                            try:
                                (devtype, name) = device.name.split(' ')
                            except ValueError:
                                self.doerror('Unable to interpret line: "[[' + device.name + ']]"')

                            if devtype.lower() == 'fw':
                                dev = FW(dynamips[pemu_name], name=name)
                            else:
                                self.doerror('Unable to identify the type of device ' + device.name )

                            #set the defaults
                            for option in devdefaults['525']:
                                if option in ('console', 'key', 'serial', 'ram', 'image'):
                                    setattr(dev, option, devdefaults['525'][option])

                            #add the whole FW into global dictionary
                            devices[name] = dev

                            #set the special device options
                            for subitem in device.scalars:
                                if device[subitem] != None:
                                    self.debug('  ' + subitem + ' = ' + str(device[subitem]))
                                    if subitem in ('console', 'key', 'serial', 'ram', 'image'):
                                        setattr(dev, subitem, device[subitem])
                                        continue
                                    elif pemu_int_re.search(subitem):
                                        # Add the tuple to the list of connections to deal with later
                                        connectionlist.append((dev, subitem, device[subitem]))
                                    else:
                                        print('***Warning: ignoring unknown config item: %s = %s' % (str(subitem), str(device[subitem])))

                else:
                    self.doerror('Bad emulator definition format: %s' % server.name)
            else:
                # Dynamips hypervisor
                server.host = server.name
                controlPort = None
                if ':' in server.host:
                    # unpack the server and port
                    (server.host, controlPort) = server.host.split(':')
                if debuglevel >= 3:
                    self.debug("Server = " + server.name)
                    for item in server.scalars:
                        self.debug('  ' + str(item) + ' = ' + str(server[item]))
                try:
                    if server['port'] != None:
                        controlPort = server['port']
                    if controlPort == None:
                        controlPort = 7200
                    dynamips[server.name] = Dynamips(server.host, int(controlPort))
                    # Reset each server
                    dynamips[server.name].reset()

                except DynamipsVerError:
                    exctype, value, trace = sys.exc_info()
                    self.doerror(value[0])

                except DynamipsError:
                    self.doerror('Could not connect to server: %s' % server.name)

                if server['udp'] != None:
                    udp = server['udp']
                else:
                    udp = globaludp
                # Modify the default base UDP NIO port for this server
                try:
                    dynamips[server.name].udp = udp
                except DynamipsError:
                    self.doerror('Could not set base UDP NIO port to: "%s" on server: %s' % (server['udp'], server.name))


                if server['workingdir'] == None:
                    # If workingdir is not specified, set it to the same directory
                    # as the network file

                    realpath = os.path.realpath(FILENAME)
                    workingdir = os.path.dirname(realpath)
                else:
                    workingdir = server['workingdir']

                try:
                    # Encase workingdir in quotes to protect spaces
                    workingdir = '"' + workingdir + '"'
                    dynamips[server.name].workingdir = workingdir
                except DynamipsError:
                    self.doerror('Could not set working directory to: "%s" on server: %s' % (server['workingdir'], server.name))

                # Has the base console port been overridden?
                if server['console'] != None:
                    dynamips[server.name].baseconsole = server['console']

                # Initialize device default dictionaries for every router type supported
                devdefaults = {}
                for key in DEVICETUPLE:
                    devdefaults[key] = {}

                # Apply lab global defaults to device defaults
                for model in devdefaults:
                    devdefaults[model]['ghostios'] = config['ghostios']
                    devdefaults[model]['ghostsize'] = config['ghostsize']
                    devdefaults[model]['sparsemem'] = config['sparsemem']
                    devdefaults[model]['oldidle'] = config['oldidle']
                    if config['idlemax'] != None:
                        devdefaults[model]['idlemax'] = config['idlemax']
                    if config['idlesleep'] != None:
                        devdefaults[model]['idlesleep'] = config['idlesleep']

                for subsection in server.sections:
                    device = server[subsection]
                    # Create the device

                    if device.name in DEVICETUPLE:
                        self.debug('Router defaults:')
                        # Populate the appropriate dictionary
                        for scalar in device.scalars:
                            if device[scalar] != None:
                                devdefaults[device.name][scalar] = device[scalar]
                        continue

                    self.debug(device.name)
                    # Create the device
                    try:
                        (devtype, name) = device.name.split(' ')
                    except ValueError:
                        self.doerror('Unable to interpret line: "[[' + device.name + ']]"')

                    if devtype.lower() == 'router':
                        # if model not specifically defined for this router, set it to the default defined in the top level config
                        if device['model'] == None:
                            device['model'] = config['model']

                        if device['model'] == '7200':
                            dev = C7200(dynamips[server.name], name=name)
                        elif device['model'] in ['3620', '3640', '3660']:
                            dev = C3600(dynamips[server.name], chassis = device['model'], name=name)
                        elif device['model'] == '2691':
                            dev = C2691(dynamips[server.name], name=name)
                        elif device['model'] in ['2610', '2611', '2620', '2621', '2610XM', '2611XM', '2620XM', '2621XM', '2650XM', '2651XM']:
                            dev = C2600(dynamips[server.name], chassis = device['model'], name=name)
                        elif device['model'] == '3725':
                            dev = C3725(dynamips[server.name], name=name)
                        elif device['model'] == '3745':
                            dev = C3745(dynamips[server.name], name=name)
                        elif device['model'] in ['1710', '1720', '1721', '1750', '1751', '1760']:
                            dev = C1700(dynamips[server.name], chassis = device['model'], name=name)
                        # Apply the router defaults to this router
                        self.setdefaults(dev, devdefaults[device['model']])

                        if device['autostart'] == None:
                            autostart[name] = config['autostart']
                        else:
                            autostart[name] = device['autostart']
                    elif devtype.lower() == 'frsw':
                        dev = FRSW(dynamips[server.name], name=name)
                    elif devtype.lower() == 'atmsw':
                        dev = ATMSW(dynamips[server.name], name=name)
                    elif devtype.lower() == 'ethsw':
                        dev = ETHSW(dynamips[server.name], name=name)
                    else:
                        print '\n***Error: unknown device type:', devtype, '\n'
                        raw_input("Press ENTER to continue")
                        handled = True
                        sys.exit(1)
                    devices[name] = dev

                    for subitem in device.scalars:
                        if device[subitem] != None:
                            self.debug('  ' + subitem + ' = ' + str(device[subitem]))
                            if self.setproperty(dev, subitem, device[subitem]):
                                # This was a property that was set.
                                continue
                            else:
                                # Should be either an interface connection or a switch mapping
                                # is it an interface?
                                if interface_re.search(subitem):
                                    # Add the tuple to the list of connections to deal with later
                                    connectionlist.append((dev, subitem, device[subitem]))
                                # is it an interface with no port? (e.g. "f0")
                                elif interface_noport_re.search(subitem):
                                    connectionlist.append((dev, subitem, device[subitem]))
                                # is it a frame relay or ATM vpi mapping?
                                elif mapint_re.search(subitem) or mapvci_re.search(subitem):
                                    # Add the tupple to the list of mappings to deal with later
                                    maplist.append((dev, subitem, device[subitem]))
                                # is it an Ethernet switch port configuration?
                                elif ethswint_re.search(subitem):
                                    ethswintlist.append((dev, subitem, device[subitem]))

                                elif subitem in ['model', 'configuration', 'autostart', 'x', 'y']:
                                    # These options are already handled elsewhere
                                    continue
                                else:
                                    print('Warning: ignoring unknown config item: %s = %s' % (str(subitem), str(device[subitem])))


        # Establish the connections we collected earlier
        for connection in connectionlist:
            self.debug('connection: ' + str(connection))
            (router, source, dest) = connection
            try:
                result = self.connect(router, source, dest)
            except DynamipsError, e:
                err = e[0]
                self.doerror('Connecting %s %s to %s resulted in \n    %s' % (router.name, source, dest, err))
            if result == False:
                self.doerror('Attempt to connect %s %s to unknown device: "%s"' % (router.name, source, dest))

        # Apply the switch configuration we collected earlier
        for mapping in maplist:
            self.debug('mapping: ' + str(mapping))
            (switch, source, dest) = mapping
            self.switch_map(switch, source, dest)

        for ethswint in ethswintlist:
            self.debug('ethernet switchport configing: ' + str(ethswint))
            (switch, source, dest) = ethswint

            parameters = len(dest.split(' '))
            if parameters == 2:
                # should be a porttype and a vlan
                (porttype, vlan) = dest.split(' ')
                try:
                    switch.set_port(int(source), porttype, int(vlan))
                except DynamipsError, e:
                    self.doerror(e)
                except AttributeError, e:
                    print "\n[[%s]]" % switch.name
                    print source + " = " + dest + "\t <==== *Error*"
                    self.doerror(e)
                except DynamipsWarning, e:
                    #dowarning(e)
                    # Now silently ignoring unused switchports
                    pass

            elif parameters == 3:
                # Should be a porttype, vlan, and an nio
                (porttype, vlan, nio) = dest.split(' ')
                try:
                    (niotype, niostring) = nio.split(':',1)
                except ValueError:
                    self.doerror('Malformed NETIO in line: ' + str(source) + ' = ' + str(dest))
                    return False
                self.debug('A NETIO: ' + str(nio))
                try:
                    #Process the netio
                    if niotype.lower() == 'nio_linux_eth':
                        self.debug('NIO_linux_eth ' + str(dest))
                        switch.nio(int(source), nio=NIO_linux_eth(switch.dynamips, interface=niostring), porttype=porttype, vlan=vlan)

                    elif niotype.lower() == 'nio_gen_eth':
                        self.debug('gen_eth ' + str(dest))
                        switch.nio(int(source), nio=NIO_gen_eth(switch.dynamips, interface=niostring), porttype=porttype, vlan=vlan)

                    elif niotype.lower() == 'nio_udp':
                        self.debug('udp ' + str(dest))
                        (udplocal, remotehost, udpremote) = niostring.split(':',2)
                        switch.nio(int(source), nio=NIO_udp(switch.dynamips, int(udplocal), str(remotehost), int(udpremote)), porttype=porttype, vlan=vlan)

                    elif niotype.lower() == 'nio_null':
                        self.debug('nio null')
                        switch.nio(int(source), nio=NIO_null(switch.dynamips), porttype=porttype, vlan=vlan)

                    elif niotype.lower() == 'nio_tap':
                        self.debug('nio tap ' + str(dest))
                        switch.nio(int(source), nio=NIO_tap(switch.dynamips, niostring), porttype=porttype, vlan=vlan)

                    elif niotype.lower() == 'nio_unix':
                        self.debug('unix ' + str(dest))
                        (unixlocal, unixremote) = niostring.split(':',1)
                        switch.nio(int(source), nio=NIO_unix(switch.dynamips, unixlocal, unixremote), porttype=porttype, vlan=vlan)

                    elif niotype.lower() == 'nio_vde':
                        self.debug('vde ' + str(dest))
                        (controlsock, localsock) = niostring.split(':',1)
                        switch.nio(int(source), nio=NIO_vde(switch.dynamips, controlsock, localsock), porttype=porttype, vlan=vlan)

                    else:
                        # Bad NIO
                        self.doerror('Invalid NIO in Ethernet switchport config: %s = %s' % (source, dest))

                except DynamipsError, e:
                    self.doerror(e)

            else:
                self.doerror('Invalid Ethernet switchport config: %s = %s' % (source, dest))

        return (connectionlist, maplist, ethswintlist)

    def import_ini(self, FILENAME):
        """ Read in the INI file
        """
        global telnetstring, globaludp, useridledbfile, handled

        # look for the INI file in the same directory as dynagen
        realpath = os.path.realpath(sys.argv[0])
        pathname = os.path.dirname(realpath)
        self.debug('pathname -> ' + realpath)
        INIPATH.append(pathname)
        for dir in INIPATH:
            inifile = dir +'/' + FILENAME

            # Check to see if configuration file exists
            try:
                self.debug('INI -> ' + inifile)
                h=open(inifile)
                h.close()
                break
            except IOError:
                continue
        else:
           self.doerror("Can't open INI file")

        try:
            config = ConfigObj(inifile, raise_errors=True)
        except SyntaxError, e:
            print "\nError:"
            print e
            print e.line, '\n'
            raw_input("Press ENTER to continue")
            handled = True
            sys.exit(1)

        try:
            telnetstring = config['telnet']
        except KeyError:
            telnetstring = None
            self.dowarning("No telnet option found in INI file.")

        try:
            globaludp = int(config['udp'])
        except KeyError:
            pass
        except ValueError:
            self.dowarning("Ignoring invalid udp value in dynagen.ini")

        try:
            useridledbfile = config['idledb']
        except KeyError:
            # Set default to the home directory
            useridledbfile = os.path.expanduser('~' + os.path.sep + 'dynagenidledb.ini')


    def import_generic_ini(self, inifile):
        """ Import a generic ini file and return it as a dictionary, if it exists
            Returns None if the file doesn't exit, or raises an error that can be handled
        """

        global handled

        try:
            h=open(inifile, 'r')
            h.close()
        except IOError:
            # File does not exist, or is not readable
            return None

        try:
            config = ConfigObj(inifile, raise_errors=True)
        except SyntaxError, e:
            print "\nError in user idlepc database:"
            print e
            print e.line, '\n'
            raw_input("Press ENTER to continue")
            handled = True
            sys.exit(1)

        return config

    def push_embedded_configurations(self):
        """ Push configurations stored in the network file
        """

        global configurations

        if configurations != {}:
            result = raw_input("There are saved configurations in your network file. \nDo you wish to import them (Y/N)? ")
            if result.lower() == 'y':
                for routerName in configurations:
                    device = devices[routerName]
                    device.config_b64 = configurations[routerName]


    def ghosting(self):
        """ Implement IOS Ghosting
        """

        global ghosteddevices, ghostsizes

        ghosts = {}         # a dictionary of ghost instances which will match the image name+hostname+port
        try:
            # If using mmap, create ghost IOS instances and apply it to instances that use them
            for device in devices.values():
                try:
                    if device.mmap == False:
                        continue
                except AttributeError:
                    # This device doesn't have an mmap property
                    continue

                if not ghosteddevices[device.name]:
                    continue

                if device.imagename == None:
                    self.doerror("No IOS image specified for device: " + device.name)

                ghostinstance = device.imagename + '-' + device.dynamips.host
                ghost_file = device.imagename + '.ghost'
                if ghostinstance not in ghosts:
                    # Only create a ghost if at least two instances on this server use this image
                    ioscount = 0
                    maxram = 0
                    for router in devices.values():
                        try:
                            if (router.dynamips.host == device.dynamips.host) and (router.imagename == device.imagename):
                                if ghosteddevices[router.name]:
                                    ioscount += 1
                                    if router.ram > maxram: maxram = router.ram
                        except AttributeError:
                            continue
                    if ioscount < 2:
                        ghosts[ghostinstance] = False
                    else:
                        # Create a new ghost
                        ghosts[ghostinstance] = True
                        ghost = Router(device.dynamips, device.model, 'ghost-'+ ghostinstance, consoleFlag = False)
                        ghost.image = device.image
                        # For 7200s, the NPE must be set when using an NPE-G2.
                        if device.model == 'c7200':
                            ghost.npe = device.npe
                        # test
                        #ghost.sparsemem = True
                        ghost.ghost_status = 1
                        ghost.ghost_file = ghost_file
                        if ghostsizes[device.name] == None:
                            ghost.ram = maxram
                        else:
                            ghost.ram = ghostsizes[device.name]
                        ghost.start()
                        ghost.stop()
                        ghost.delete()
                # Reference the appropriate ghost for the image and dynamips server, if the multiple IOSs flag is true
                if ghosts[ghostinstance]:
                    device.ghost_status = 2
                    device.ghost_file = ghost_file
        except DynamipsError, e:
            self.doerror(e)


    def apply_idlepc(self):
        """  Apply idlepc values from the database
        """

        global useridledbfile

        # Read in the user idlepc database, if it exists
        useridledb = self.import_generic_ini(useridledbfile)

        # Apply idlepc values
        for device in devices.values():
            try:
                if device.idlepc == None:
                    if useridledb and device.imagename in useridledb:
                        device.idlepc = useridledb[device.imagename]
            except AttributeError:
                pass

    def autostart(self):
        """  Autostart the instances
        """

        global autostart

        for device in devices.values():
            # if necessary start the instances
            if autostart.has_key(device.name):
                if autostart[device.name]:
                    try:
                        if device.idlepc == None:
                            self.dowarning("Starting %s with no idle-pc value" % device.name)
                        device.start()
                    except DynamipsError, e:
                        # Strip leading error code if present
                        e = str(e)
                        if e[3] == '-':
                            e = e[4:] + "\nSee dynamips output for more info.\n"
                        self.doerror(e)

    def debug(self, string):
        """ Print string if debugging is true
        """
        global debuglevel
        # Level 3, dynagen debugs.
        if debuglevel >= 3: print '  DEBUG: ' + str(string)

    def doerror(self, msg):
        global handled

        """Print out an error message"""
        print '\n*** Error:', str(msg)
        handled = True
        self.doreset()
        raw_input("Press ENTER to continue")
        sys.exit(1)

    def dowarning(self, msg):
        """Print out minor warning messages"""
        print 'Warning:', str(msg)

    def doreset(self):
        """reset all hypervisors"""
        for d in dynamips.values():
            d.reset()

if __name__ == "__main__":
    # Catch and display any unhandled tracebacks for bug reporting.
    try:
        # Get command line options
        usage = "usage: %prog [options] <config file>"
        parser = OptionParser(usage=usage, version="%prog " + VERSION)
        parser.add_option("-d", "--debug", action="store_true", dest="debug",
                      help="output debug info")
        parser.add_option("-n", "--nosend", action="store_true", dest="nosend",
                      help="do not send any command to dynamips")
        parser.add_option("--notelnet", action="store_true", dest="notelnet",
                      help="ignore telnet commands (for use with gDynagen)")
        try:
            (options, args) = parser.parse_args()
        except SystemExit:
            handled = True
            sys.exit(0)

        if len(args) != 1:
            parser.print_help()
            handled = True
            sys.exit(1)

        FILENAME = args[0]
        if options.debug:
            setdebug(True)
            print "\nPython version: %s" % sys.version
        if options.nosend:
            nosend(True)
            #pemunosend(True)
        if options.notelnet: notelnet = True

        dynagen = Dynagen()
        # Check to see if the network file exists and is readable
        try:
            h = open(FILENAME, 'r')
            h.close()
        except IOError:
            dynagen.doerror('Could not open file: ' + FILENAME)

        # Import INI file
        try:
            dynagen.import_ini(INIFILE)
        except DynamipsError, e:
            dynagen.doerror(e)

        print "\nReading configuration file...\n"
        try:
            dynagen.import_config(FILENAME)
        except DynamipsError, e:
            # Strip leading error code if present
            e = str(e)
            if e[3] == '-':
                # Are the first three characters an error code?
                try:
                    if e[:3] == str(int(e[:3])):
                        e = e[4:] + "\nSee dynamips output for more info.\n"
                except ValueError:
                    pass

            dynagen.doerror(e)
        except DynamipsWarning, e:
            dynagen.dowarning(e)

        dynagen.push_embedded_configurations()
        dynagen.ghosting()
        dynagen.apply_idlepc()
        dynagen.autostart()

        print "Network successfully loaded\n"

        """"
        print "Pickle test..."
        import pickle

        output = open('pickletest.pkl', 'wb')
        pickle.dump(devices, output)
        output.close()
        #doclose()
        """

        console = Console()
        try:
            console.cmdloop()
        except KeyboardInterrupt:
            print "Exiting..."

        dynagen.doreset()
    except DynamipsErrorHandled:
        raw_input("Press ENTER to exit")
        sys.exit(1)
    except:
        exctype, value, trace = sys.exc_info()

        # Display the unhandled exception, and pause so it can be observed
        if not handled:
            print """*** Dynagen has crashed ****
Please open a bug report against Dynagen at http://www.ipflow.utc.fr/bts/
Include a description of what you were doing when the error occured, your
network file, any errors output by dynamips, and the following traceback data:
            """

            traceback.print_exc()
            raw_input("Press ENTER to exit")

            if debuglevel >=2:
                print "\nDumping namespace..."
                print 'Globals:'
                print trace.tb_frame.f_globals
                print 'Locals:'
                print trace.tb_frame.f_locals

            sys.exit(1)