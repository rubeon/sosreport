## Copyright (C) 2007 Sadique Puthen <sputhenp@redhat.com>

### This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

from sos.plugins import Plugin, RedHatPlugin, DebianPlugin, UbuntuPlugin

class ipsec(Plugin):
    """ipsec related information
    """

    plugin_name = "ipsec"
    packages = ('ipsec-tools',)

class RedHatIpsec(ipsec, RedHatPlugin):
    """ipsec related information for Red Hat distributions
    """

    files = ('/etc/racoon/racoon.conf',)

    def setup(self):
        self.addCopySpec("/etc/racoon")

class DebianIpsec(ipsec, DebianPlugin, UbuntuPlugin):
    """ipsec related information for Debian distributions
    """

    files = ('/etc/ipsec-tools.conf',)

    def setup(self):
        self.addCopySpecs(["/etc/ipsec-tools.conf",
                           "/etc/ipsec-tools.d",
                           "/etc/default/setkey"])
