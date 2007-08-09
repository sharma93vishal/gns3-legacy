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

addingLinkFlag = False
useHypervisorManager = True

# A singleton instance of GNS3 Application
#   used for storing / accessing highly used object.
GApp = None

# Enum
class Enum:
    class Mode:
        Design = 0
        Emulation = 1
        Simulation = 2

modesIds = [
    Enum.Mode.Design,
    Enum.Mode.Emulation,
    Enum.Mode.Simulation,
]
modesNames = {
    Enum.Mode.Design : 'Design Mode',
    Enum.Mode.Emulation : 'Emulation Mode',
    Enum.Mode.Simulation : 'Simulation Mode',
}

