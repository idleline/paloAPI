import panapi
import csv
from BeautifulSoup import BeautifulSoup as xmlparse

threatFile = open('threats.xml', 'r')
csvOut = open('threatfile.csv', 'w+')
wf = csv.writer(csvOut, delimiter=',')
header = [['Threat-ID', 'Threat Name', 'Category', 'Action', 'CVE Number']]
wf.writerows(header)

def index_threat(threat):
    vulndata = []
    for i in range(len(threat)):
        
        threatID = threat[i].attrs[0][1]
        threatName = threat[i].threatname.text
        category = threat[i].category.text
        if threat[i].find('default-action') != None:
            action = threat[i].find('default-action').text
        else:
            action = "none"
        if threat[i].cve != None:
            cve = threat[i].cve.member.text
        else:
            cve = ''
    
        data = [threatID, threatName, category, action, cve]
        vulndata.append(data)
    
    return vulndata

if __name__ == '__main__':
    soup = xmlparse(threatFile.read())
    mdata = index_threat(soup.threats.find('phone-home').findAll('entry'))
    wf.writerows(mdata)
    vdata = index_threat(soup.threats.vulnerability.findAll('entry'))
    wf.writerows(vdata)
    
    threatFile.close()
    csvOut.close()
