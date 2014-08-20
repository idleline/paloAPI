import panapi
from BeautifulSoup import BeautifulSoup as xmlparse
from applescript import asrun, asquote
import sys

deviceA = '{0}-a'.format(sys.argv[1])
deviceB = '{0}-b'.format(sys.argv[1])
type = 'op'

xpath = '<show><high-availability><state></state></high-availability></show>'
soup = xmlparse(panapi.apicall(deviceA, type, xpath))
state = soup.group.find('local-info').find('state')

print state.text

if state.text == 'active':
    panurl = 'https://{0}'.format(deviceA)
    print "I'm active"
elif state.text == 'passive':
    panurl = 'https://{0}'.format(deviceB)
    print "I'm passive"
else:
    sys.exit()

ascript = '''
tell application "Google Chrome"
    activate
    set theUrl to "%s"
    
    if (count every window) = 0 then
        make new window
    end if
    
    set found to false
    set theTabIndex to -1
    repeat with theWindow in every window
        set theTabIndex to 0
        repeat with theTab in every tab of theWindow
            set theTabIndex to theTabIndex + 1
            if theTab's URL = theUrl then
                set found to true
                exit
            end if
        end repeat
        
        if found then
            exit repeat
        end if
    end repeat
    
    if found then
        tell theTab to reload
        set theWindow's active tab index to theTabIndex
        set index of theWindow to 1
    else
        tell window 1 to make new tab with properties {URL:theUrl}
    end if
end tell
''' % panurl

asrun(ascript)

