# Python module for Palo Alto API calls 
# Written by Lance Wheelock (c) 2012-2014
# Version: 1.0.3

import cStringIO
import pycurl

'''
Define the function for passing a URL to PyCurl and call the Panorama API
'''
def apicall(device, apitype, xpath):
        
    if apitype == 'config':
        apiprefix = '.netsec.ebay.com/api/?type=config&action=get&xpath='
    elif apitype == 'op':
        apiprefix = '.netsec.ebay.com/api/?type=op&cmd='
    elif apitype == 'ip-op':
        apiprefix = '/api/?type=op&cmd='
    elif apitype == 'log':
        apiprefix = '.netsec.ebay.com/api/?type=log'
    else:
        excode = 'API type %s is unknown' % (apitype)
        exit(excode)
    
    key = "LUFRPT1KZWhsZU95ZmU4SEJhd2xyUlZ6WWF2ZkkrTEE9VjZVZzNNZlNSUWd5VW9PemxXaUxIWEYzZFhpWU5adDlLd1F4Vm1LTEE2bz0=" 
        
    url = "https://%s%s%s&key=%s" % (device, apiprefix, xpath, key)
    print url
    buff = cStringIO.StringIO()
    
    '''
    Set pycurl options
    pass the API call URL
    Ignore SSL warnings
    Write to the buffer
    Execute
    '''
    c=pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(pycurl.SSL_VERIFYHOST, 0)
    c.setopt(pycurl.TIMEOUT, 90)
    c.setopt(pycurl.CONNECTTIMEOUT, 5)
    c.setopt(c.WRITEFUNCTION, buff.write)
    try:
        c.perform()
    except pycurl.error, error:
        errno, errstr = error
        return errstr
    # Set variabl to the xml output from c.perform captured by our cStringIO buffer
    xmlout = buff.getvalue()
    
    if len(xmlout) <= 58: # Denotes success but no data
        return nothing
    elif len(xmlout) == 91: # Denotes a bad xpath XML return
        return invxpath
    elif len(xmlout) == 99: # Denotes a bad key
        return invkey
    else:    
        return xmlout
'''
Error messages
'''
nothing = 'The API call was successfull but there was no XML returned'
invxpath = 'The xpath supplied is invalid'
invkey = 'The key supplied is invalid'

'''
Stand alone code for testing
'''
if __name__ == '__main__':
    print apicall('panorama', 'config', "/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='corp-site-palos']/address")
