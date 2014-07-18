#!/usr/bin/env python
import panapi
from BeautifulSoup import BeautifulSoup as xmlparse
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import logging
from logging import handlers


''' Set API Parameters
xpath: this API call polls every device connected to Panorama
xmlout: Store XML returned from panapi module of all the devices
soup: use BS to index the XML so we can manipulate it
devices: Create a list of entries so we can go through them in iteration
'''
xpath = '<show><devices><connected></connected></devices></show>'
xmlout = panapi.apicall('panorama', 'op', xpath) # Execute API
soup = xmlparse(xmlout)
entries = soup.devices.findAll('entry') # Parse XML data from API call

'''Logger Settings
'''
logLevel = logging.INFO # Modify this with either (logging.INFO or logging.DEBUG) to change log verbosity

logger = logging.getLogger(__name__)
logger.setLevel(logLevel) 

log_path = '/Users/lwheelock/scripts/solera/dev/psupply.log'
handler = handlers.RotatingFileHandler(log_path, maxBytes=10000000, backupCount=4)
handler.setLevel(logLevel)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

def send_errorPS(deviceHostname, psDesc, psAlarm, psInserted, deviceAddress):
    failed = "%s FAILED: %s\nIP Address: %s\nAlarm: %s\nInserted: %s\n\nYou can stop e-mail alerts by adding the hostname in the subject to the 'ignore-hosts.txt' file on netapp-01.sc5:/home/paloapi" % (deviceHostname, psDesc, deviceAddress, psAlarm, psInserted)
    
    msg = MIMEText(failed)
    addr = 'netsecurity@ebay.com'
    to = ['opsalerts@ebay.com', 'netsecurity@ebay.com']
     
    msg['Subject'] = '[PALO ALTO - %s] Failed Power Supply Alarm' % (deviceHostname)
    msg['From'] = addr
    msg['To'] = ", ".join(to)
    
    s = smtplib.SMTP('atom.corp.ebay.com')
    s.sendmail(addr, to, msg.as_string())
    s.quit 
    
    logger.info('e-mail sent for %s - Failed Power Supply: %s' % (deviceHostname, psDesc))

def main(devices):
    total = 0
    checked = 0
    for i in range(len(devices)):
        if devices[i].family is None: # Sloppy error checking
            pass
        else: # Set up our env check on the device
            deviceFamily = devices[i].family.contents[0]
            deviceHostname = devices[i].hostname.contents[0]
            deviceAddress = devices[i].find('ip-address').contents[0]
            
            if deviceFamily != '2000' and deviceFamily != '3000' and deviceFamily != '500': # Models which are single cord and we can ignore
                total += 1
                xpath = '<show><system><environmentals><power-supply></power-supply></environmentals></system></show>'
                xmlout = panapi.apicall(deviceAddress, 'ip-op', xpath)
                soup = xmlparse(xmlout)
                logger.debug('Checking %s' % (deviceHostname))
                psUnit = soup.find('power-supply').findAll('entry') # Create a list of power supplies so we can iterate through them
                
                for x in range(len(psUnit)): 
                    if psUnit[x] is None:
                        pass
                    else:
                        checked += 1
                        psAlarm = psUnit[x].alarm.contents[0]
                        psInserted = psUnit[x].inserted.contents[0]
                        psDesc = psUnit[x].description.contents[0]
                        
                        if psAlarm == "True" or psInserted == "False":
                            try:
                                ignore = open('ignore-hosts.txt', 'r') # Check if a device is in the ignore list
                            except IOError, e:
                                logger.error('Error opening ignore-hosts.txt - Please make sure this file exists even if it is empty - Error %s' % (e))
                                exit()
                            if any(deviceHostname in s for s in ignore.readlines()):
                                logger.warn('IGNORED - %s has failed power supply %s but entry in ignore-hosts.txt was found - No alert sent' % (deviceHostname, psDesc))
                            else:
                                send_errorPS(deviceHostname, psDesc, psAlarm, psInserted, deviceAddress)
                                logger.info('Host: %s -- Unit: %s -- Inserted: %s -- Alarm: %s' % (deviceHostname, psDesc, psInserted, psAlarm))
                            ignore.close()
                                   
                        else:
                            status = "%s - %s is OK" % (deviceHostname, psDesc)
                            logger.debug(status)
    if checked / 2 == total:
       print "All devices checked"
       logger.info('Execution Summary - Dual cord devices reported: %s -- Checked Devices: %s' % (total, checked / 2 ))
    else:
       print "Total: %s - Checked: %s" % (total, checked / 2)
       logger.warn('Not all devices were successfully checked - Dual cord devices reported: %s -- Checked Devices: %s' % (total, checked / 2))

if __name__ == "__main__":
    logger.info('Executing main')
    main(entries)