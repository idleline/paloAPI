#!/usr/bin/env python
import panapi
import re
from bs4 import BeautifulSoup as xmlparse

#userInput = raw_input("Enter the user or IP to search for: ")

#############################
# xpath examples
# show user all - /api/?type=op&cmd=<show><user><ip-user-mapping><all></all></ip-user-mapping></user></show>
# show user detail - /api/?type=op&cmd=<show><user><ip-user-mapping><detail></detail></ip-user-mapping></user></show>
# show user 
###########################
xpath = "<show><user><ip-user-mapping><all></all></ip-user-mapping></user></show>"
xmlout = panapi.apicall('lantana-a', 'op', xpath)

########
# Make user input regex
########

#x  = re.compile("((?:\d|[1-9]\d|1\d\d|2(?:[0-4]\d|5[0-5]))(?:\.(?:\d|[1-9]\d|1\d\d|2(?:[0-4]\d|5[0-5]))){3})[ \t]+AD[ \t]+(corp)\\\\([_,a-z]+)")
#list = x.findall(xmlout)

count = 0

soup = xmlparse(xmlout)

print soup.entry.ip

ipaddr.append(soup.entry['ip'])
#for sibling in soup.entry.next_siblings:
#    ipaddr.append(sibling['ip'])

#user.append(soup.entry['user'])
#for sibling in soup.entry.next_siblings:
#    user.append(sibling['user'])

#print ipaddr

if count == 0:
    print "No Match Found in %s entries" % (len(list))
elif count == 1:
    print "1 entry matched in %s entries" % (len(list))
else:
    print "%s matches out of %s entries" % (count, len(list))
    
