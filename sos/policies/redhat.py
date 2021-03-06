## Copyright (C) Steve Conklin <sconklin@redhat.com>

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

# This enables the use of with syntax in python 2.5 (e.g. jython)
import os
import sys

from sos.plugins import RedHatPlugin
from sos.policies import LinuxPolicy, PackageManager
from sos import _sos as _

sys.path.insert(0, "/usr/share/rhn/")
try:
    from up2date_client import up2dateAuth
    from up2date_client import config
    from rhn import rpclib
except:
    # might fail if non-RHEL
    pass

class RedHatPolicy(LinuxPolicy):
    distro = "Red Hat"
    vendor = "Red Hat"
    vendor_url = "http://www.redhat.com/"

    def __init__(self):
        super(RedHatPolicy, self).__init__()
        self.reportName = ""
        self.ticketNumber = ""
        self.package_manager = PackageManager('rpm -qa --queryformat "%{NAME}|%{VERSION}\\n"')
        self.valid_subclasses = [RedHatPlugin]

    @classmethod
    def check(self):
        """This method checks to see if we are running on Red Hat. It must be overriden
        by concrete subclasses to return True when running on a Fedora, RHEL or other
        Red Hat distribution or False otherwise."""
        return False

    def runlevelByService(self, name):
        from subprocess import Popen, PIPE
        ret = []
        p = Popen("LC_ALL=C /sbin/chkconfig --list %s" % name,
                  shell=True,
                  stdout=PIPE,
                  stderr=PIPE,
                  bufsize=-1)
        out, err = p.communicate()
        if err:
            return ret
        for tabs in out.split()[1:]:
            try:
                (runlevel, onoff) = tabs.split(":", 1)
            except:
                pass
            else:
                if onoff == "on":
                    ret.append(int(runlevel))
        return ret

    def getLocalName(self):
        return self.hostName()

class RHELPolicy(RedHatPolicy):

    msg = _("""\
This command will collect system configuration and diagnostic information \
from this %(distro)s system. An archive containing the collected information \
will be generated in %(tmpdir)s and may be provided to a %(vendor)s support \
representative or used for local diagnostic or recording purposes.

Any information provided to %(vendor)s will be treated in strict confidence \
in accordance with the published support policies at:

  %(vendor_url)s

The generated archive may contain data considered sensitive and its content \
should be reviewed by the originating organization before being passed to \
any third party.

No changes will be made to system configuration.
%(vendor_text)s
""")

    distro = "Red Hat Enterprise Linux"
    vendor = "Red Hat"
    vendor_url = "https://access.redhat.com/support/"

    def __init__(self):
        super(RHELPolicy, self).__init__()

    @classmethod
    def check(self):
        """This method checks to see if we are running on RHEL. It returns True
        or False."""
        return (os.path.isfile('/etc/redhat-release')
                and not os.path.isfile('/etc/fedora-release'))

    def rhelVersion(self):
        try:
            pkg = self.pkgByName("redhat-release") or \
            self.allPkgsByNameRegex("redhat-release-.*")[-1]
            pkgname = pkg["version"]
            if pkgname[0] == "4":
                return 4
            elif pkgname[0] in [ "5Server", "5Client" ]:
                return 5
            elif pkgname[0] == "6":
                return 6
        except:
            pass
        return False

    def rhnUsername(self):
        try:
            cfg = config.initUp2dateConfig()

            return rpclib.xmlrpclib.loads(up2dateAuth.getSystemId())[0][0]['username']
        except:
            # ignore any exception and return an empty username
            return ""

    def getLocalName(self):
        return self.rhnUsername() or self.hostName()

class FedoraPolicy(RedHatPolicy):

    distro = "Fedora"
    vendor = "the Fedora Project"
    vendor_url = "https://fedoraproject.org/"

    def __init__(self):
        super(FedoraPolicy, self).__init__()

    @classmethod
    def check(self):
        """This method checks to see if we are running on Fedora. It returns True
        or False."""
        return os.path.isfile('/etc/fedora-release')

    def fedoraVersion(self):
        pkg = self.pkgByName("fedora-release") or \
        self.allPkgsByNameRegex("fedora-release-.*")[-1]
        return int(pkg["version"])

# vim: ts=4 sw=4 et
