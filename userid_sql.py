import panapi
import MySQLdb
from BeautifulSoup import BeautifulSoup as xmlparse
import logging
from logging import handlers

'''
Set logging
'''
logLevel = logging.INFO # Modify this with either (logging.INFO or logging.DEBUG) to change log verbosity

logger = logging.getLogger(__name__)
logger.setLevel(logLevel) 

log_path = "userid_sql.log"
handler = handlers.RotatingFileHandler(log_path, maxBytes=10000000, backupCount=4)
handler.setLevel(logLevel)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

'''
Set SQL Parameters
'''
db = MySQLdb.connect("localhost","root","dbr0ot!","uid")
cursor = db.cursor()
cursor.execute("TRUNCATE TABLE ipmap")

'''
xpath examples
show user all - /api/?type=op&cmd=<show><user><ip-user-mapping><all></all></ip-user-mapping></user></show>
show user detail - /api/?type=op&cmd=<show><user><ip-user-mapping><detail></detail></ip-user-mapping></user></show>
show user 
'''
def enum_users():
    xpath = "<show><user><ip-user-mapping><all></all></ip-user-mapping></user></show>"
    logger.debug("Calling API")
    soup = xmlparse(panapi.apicall('lantana-a', 'op', xpath))
    
    return soup

'''
Search the XML form and put the ip / user tag data into lists
'''

if __name__ == '__main__':
    logger.info("attempting to retrieve XML user IP data")
    soup = enum_users()
    
    logger.debug("Enumerating XML data")
    ipaddr = soup.findAll('ip')
    user = soup.findAll('user')
    
    '''
    Start comparing the input to the data in the lists.
    This seciton could be improved by using regex for 
    matching and not literal values
    '''
    
    logger.debug("Writing to SQL Database")
    for i in range(len(ipaddr)):
        x = ipaddr[i].string
        y = user[i].string
        cursor.execute("""INSERT INTO ipmap (username, ipaddress) VALUES (%s, %s)""", (y, x))
        db.commit()
    logger.info("user table updated")
     
    cursor.close()
    db.close()