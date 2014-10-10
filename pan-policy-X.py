import panapi
import re

fo = open('/Users/lwheelock/Dropbox/Projects/BCN/v2-checker.csv')

def portSub(port, app, proto):
    if app == 'dell-drac':
        port = '5900'
    if app == 'dns':
        port = '53'
        proto = '17'
    if app == 'ldap':
        port = '389'
        proto = '17'
    if app == 'ms-ds-smb':
        port == '445'
    if app == 'ms-rdp':
        port == '3389'
    if app == 'mysql':
        port = '3306'
    if app == 'netbios-dg':
        port = '138'
        proto = '17'
    if app == 'netbios-ns':
        port = '137'
        proto = '17'
    if app == 'netbios-ss':
        port = '139'
    if app == 'oracle':
        port = '1521'
    if app == 'snmp':
        port = '161'
        proto = '17'
    if app == 'ssh':
        port = '22'
    if app == 'ssl':
        port = '443'
    if app == 'syslog':
        port = '514'
        proto = '17'
    if app == 'vmware':
        port = '902'
    if app == 'web-browsing':
        port = '80'
    if app == 'x11':
        port = '6001'
        
    return port, proto

fwAllow = open('allow-bcn.txt', 'w')
fwDeny = open('deny-bcn.txt', 'w')

for line in fo.readlines():
    rule = line.split(',')
    
    srcIP = '10.227.81.10'
    dstIP = rule[1].lstrip('bcn-cn-')
    port = rule[2].lstrip('TCP')
    app = rule[3].rstrip()
    proto = '6'
    
    if port == 'application-default':
        port, proto = portSub(port, app, proto)
    
    xpath = '<test><security-policy-match><from>CORP</from><to>EE-GSI</to><source>%s</source><destination>%s</destination><destination-port>%s</destination-port>\
<application>%s</application><protocol>6</protocol></security-policy-match></test>' % (srcIP, dstIP, port, app)
    
    result = panapi.apicall('monksblood-a', 'op', xpath)
    allow = re.search("action allow;", result)
    
    if allow:
        entry = "%s %s %s %s" % (srcIP, dstIP, port, app)
        fwAllow.write(entry)
        print 'Allowed:', entry
    else:
        entry = "%s %s %s %s" % (srcIP, dstIP, port, app)
        fwDeny.write(entry)
        print 'Denied:', entry
          
fwAllow.close()
fwDeny.close()
    
    

