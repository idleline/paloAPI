import panapi
from BeautifulSoup import BeautifulSoup as xmlparse
import urllib

rname = 'IT+DMZ+to+dns+servers'
source = 'g_DUB-EB-IT-10.243.98.0-23'

xpath = "/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='DUB-IT-Firewall']/pre-rulebase/security/rules/entry[@name='%s']/source&element=<member>%s</member>" % (rname, source)

print xpath
print panapi.apicall('panorama', 'configset', xpath)

