#!/usr/bin/env python

import sys
import panapi
import socket
from BeautifulSoup import BeautifulSoup as xmlparse

if len(sys.argv) < 2:
    print ("Usage: getaddr.py <filename>")
else:
    for arg in sys.argv[1:]:
        try:
            fo = open(arg, 'r')
            fr = open('panobj.txt', 'w+')
        except IOError:
            print 'Error: Unable to open the file', arg
	else:
            for line in fo.readlines():
                nline = line.replace('\n', '')
                xpath="/config/shared/address/entry[@name='%s']" % (nline)
                xmlout = panapi.apicall('panorama', 'config', xpath)
                
                soup = xmlparse(xmlout)
                
                if xmlout == "The API call was successfull but there was no XML returned":
                    try: 
                        fqdnip = socket.gethostbyname(nline)
                        obnoex = '%s does not exist yet\n' % (nline)
                        fr.write(obnoex)
                        entry = "set shared address %s ip-address %s" % (nline, fqdnip)
                        print entry
                    except socket.gaierror:
                        obnoex = '%s does not exist or resolve in DNS\n' % (nline)
                        fr.write(obnoex)
                        print obnoex

                else: 
                    for entry in soup.findAll('entry'):
                        if nline == entry['name']:
                            obex = nline + ' EXISTS\n'
                            fr.write(obex) 
fo.close()
