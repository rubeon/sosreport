## Copyright (C) 2012 Red Hat, Inc., Bryn M. Reeves <bmr@redhat.com>

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

class sunrpc(Plugin):
    """Sun RPC related information
    """

    plugin_name = "sunrpc"
    service = None

    def checkenabled(self):
        if self.policy().runlevelDefault() in \
		self.policy().runlevelByService(self.service):
            return True
        return False

    def setup(self):
        self.addCmdOutput("/usr/sbin/rpcinfo -p localhost")
        return

class RedHatSunrpc(sunrpc, RedHatPlugin):
    """Sun RPC related information for Red Hat systems
    """

    service = 'rpcbind'

# FIXME: depends on addition of runlevelByService (or similar)
# in Debian/Ubuntu policy classes
#class DebianSunrpc(sunrpc, DebianPlugin, UbuntuPlugin):
#    """Sun RPC related information for Red Hat systems
#    """
#
#    service = 'rpcbind-boot'
#
#    def setup(self):
#        self.addCmdOutput("/usr/sbin/rpcinfo -p localhost")
#        return


