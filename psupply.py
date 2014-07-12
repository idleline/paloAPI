import panapi
from bs4 import BeautifulSoup as xmlparse
import unicodedata

xpath = '<show><devices><connected></connected></devices></show>'
xmlout = panapi.apicall('panorama', 'op', xpath)
soup = xmlparse(xmlout)
devices = soup.devices.find_all('entry')

for i in range(len(devices)):
    if devices[i].family is None:
        pass
    else:
        deviceFamily = devices[i].family.contents[0].encode('ascii', 'ignore')
        deviceHostname = devices[i].hostname.contents[0].encode('ascii', 'ignore')
        deviceAddress = devices[i].ip-address.contents[0].encode('ascii', 'ignore')
      
    if deviceFamily != '2000':
        xpath = '<show><system><environmentals><power-supply></power-supply></environmentals></system></show>'
        xmlout = panapi.apicall(deviceAddress, 'op', xpath)
        soup = xmlparse(xmlout)
        psUnit = soup.find('power-supply').findAll('entry')

#print psUnit

        for x in range(len(psUnit)):
            if psUnit[x] is None:
                pass
            else:
                psAlarm = psUnit[x].alarm.contents[0].encode('ascii', 'ignore')
                psInserted = psUnit[x].inserted.contents[0].encode('ascii', 'ignore')
                psDesc = psUnit[x].description.contents[0].encode('ascii', 'ignore')
                
                if psAlarm == "True":
                    print "%s status: Alarm=%s and Inserted=%s" % (psDesc, psAlarm, psInserted)
                elif psInserted == "False":
                    print "%s status: Alarm=%s and Inserted=%s" % (psDesc, psAlarm, psInserted)
                else:
                    print "%s is Ok"
          
      

    
    
        
        
        