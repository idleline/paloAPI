#/usr/bin/env python
from lxml import etree
import os
import sys
import argparse

def cleanup(outfile, filepath):
    os.system('rm ./index.html?*')
    filerem = 'rm {0}{1}'.format(filepath,outfile)
    os.system(filerem)
    
    
def callapi(outfile, filepath):
    device = 'toadstool-a'
    apiprefix = '.netsec.ebay.com/api/?type=user-id&action=set&client=wget&file-name=%s' % (outfile)
    artifact = filepath + outfile
    url = '"https://%s%s&key=IhCc0YOjZHAt9WLgvKkbDXSNsVbNEWWcqXkaK%sB/dnuw="' % (device, apiprefix, '%2')
    callit = "/opt/local/bin/wget --no-check-certificate --post-file %s %s" % (artifact, url)
    
    os.system(callit)
    cleanup(outfile, filepath)

def crxml(username,userip,ttl,event):
    # Open file to write data to
    outfile = "userdata.xml"
    filepath = "/tmp/"
    fr = open(filepath + outfile, 'w+')

    username = 'corp\\' + username
    root = etree.Element('uid-message')
    
    version = etree.Element('version')
    version.text = '1.0'
    root.append(version)
    
    ttype = etree.Element('type')
    ttype.text = 'update'
    root.append(ttype)
    
    payload = etree.Element('payload')
    root.append(payload)
    
    login = etree.Element(event)
    payload.append(login)
    
    entry = etree.Element('entry', name=username, ip=userip, timeout=ttl)
    login.append(entry)
    
    # print out form
    outdata = etree.tostring(root, pretty_print=True)
    fr.write(outdata)
    fr.close()
    callapi(outfile, filepath)

def main(argv):
    parser = argparse.ArgumentParser(description='Description: Add users to Palo Alto UID Mapping table via the XML API')
    
    parser.add_argument('user', action='store', help='Username of the user to inject into the table')
    parser.add_argument('ip', action='store', help='IP Address of the users machine')
    parser.add_argument('timeout', action='store', help='Timeout specified in minutes the user will exist in the table')
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--add', action='store_true', help='[default] Add the user to a table')
    group.add_argument('-r', '--remove', action='store_true', help='Remove the user from the table')
    
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    
    results = parser.parse_args()
    
    if results.remove:
        event = 'logout'
    elif results.add:
        event = 'login'
    else:
        print 'usage: plug_user.py [-h] [-a | -r] [--version] user ip timeout'
        sys.exit(2)
    
    username = results.user
    userip = results.ip
    ttl = results.timeout
    crxml(username,userip,ttl,event)
    
if __name__ == "__main__":
    main(sys.argv[1:])
    
