#!/usr/bin/env python
import panapi
from BeautifulSoup import BeautifulSoup as xmlparse
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

#startTime = datetime.now() # Checking script runtime for optimizations which there aren't really any :(

def send_error(deviceHostname, psDesc, psAlarm, psInserted):
    failed = "%s FAILED: %s\nAlarm: %s\nInserted: %s\n\nYou can stop e-mail alerts by adding the hostname in the subject to the 'ignore-hosts.txt' file on netapp-01.sc5:/home/paloapi" % (deviceHostname, psDesc, psAlarm, psInserted)
    
    msg = MIMEText(failed)
    addr = 'netsecurity@ebay.com'
    to = ['opsalerts@ebay.com', 'netsecurity@ebay.com']
     
    msg['Subject'] = '[PALO ALTO - %s] Failed Power Supply Alarm' % (deviceHostname)
    msg['From'] = addr
    msg['To'] = ", ".join(to)
    
    s = smtplib.SMTP('atom.corp.ebay.com')
    s.sendmail(addr, to, msg.as_string())
    s.quit 

xpath = '<show><devices><connected></connected></devices></show>'
xmlout = panapi.apicall('panorama', 'op', xpath)
soup = xmlparse(xmlout)
devices = soup.devices.findAll('entry')

for i in range(len(devices)):
    if devices[i].family is None: # Sloppy error checking
        pass
    else: # Set up our env check on the device
        deviceFamily = devices[i].family.contents[0]
        deviceHostname = devices[i].hostname.contents[0]
        deviceAddress = devices[i].find('ip-address').contents[0]
        #print deviceFamily, deviceHostname, deviceAddress
        
        count = 0
        if deviceFamily != '2000' and deviceFamily != '3000' and deviceFamily != '500': # Models which are single cord and we can ignore
            count += 1
            xpath = '<show><system><environmentals><power-supply></power-supply></environmentals></system></show>'
            xmlout = panapi.apicall(deviceAddress, 'ip-op', xpath)
            soup = xmlparse(xmlout)
            psUnit = soup.find('power-supply').findAll('entry') # Create a list of power supplies so we can iterate through them

            checked = 0
            for x in range(len(psUnit)): # Sloppy way to do a for loop
                if psUnit[x] is None:
                    pass
                else:
                    psAlarm = psUnit[x].alarm.contents[0]
                    psInserted = psUnit[x].inserted.contents[0]
                    psDesc = psUnit[x].description.contents[0]
                    
                    fo = open('ps-status.txt', 'a') # Write our status to a file
                    
                    if psAlarm == "True" or psInserted == "False":
                        ignore = open('ignore-hosts.txt', 'r') # Check if a device is in the ignore list
        
                        if any(deviceHostname in s for s in ignore.readlines()):
                            pass
                        else:
                            #send_error(deviceHostname, psDesc, psAlarm, psInserted)
                            print deviceFamily, deviceHostname, deviceAddress
                            status = "%s - %s has a FAILED" % (deviceHostname, psDesc)
                        ignore.close()
                               
                    else:
                        status = "%s - %s is OK" % (deviceHostname, psDesc)
                        status = status + '\n'
                        fo.write(status)
                    
                    fo.close()
                        
#print "Finished - Script executed in %s" % (datetime.now()-startTime)
