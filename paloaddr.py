#!/usr/bin/env python

import sys
import panapi
import socket
from BeautifulSoup import BeautifulSoup as xmlparse

group = []

if len(sys.argv) < 2:
    print ("Usage: getaddr.py <filename>")
else:
    for arg in sys.argv[1:]:
        try:
            fo = open(arg, 'r')
        except IOError:
            print 'Error: Unable to open the file', arg
    else:
        for line in fo.readlines():
            nline = line.replace('\n', '')
            name = nline.replace('/', '-')
            prep = 'set shared address BCN-VPN-%s description "BCN Object for VPN connectivity to EE" ip-netmask %s' % (name, nline)
            
            group.append('BCN-VPN-%s' % (name))
            
            print prep
    
        groupadd = 'set shared address-group BCN-VPN-Networks [ '
        for name in group:
            groupadd = groupadd + name + " "
        
        groupadd = groupadd + ']'

        print groupadd

        