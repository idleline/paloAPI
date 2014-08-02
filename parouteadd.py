import panapi
import sys

def send_route(device, routeName, destNet, nextHop, interface):
        xpath = "/config/devices/entry[@name='localhost.localdomain']/network/virtual-router/entry[@name='default']/routing-table/ip/static-route/entry[@name='%s']&element=<destination>%s</destination><nexthop><ip-address>%s</ip-address></nexthop><interface>%s</interface>" % (routeName, destNet, nextHop, interface)
        panapi.apicall(device, 'configset', xpath)
        #print xpath

if __name__ == "__main__": 
    if len(sys.argv) < 2:
        print ("Usage: parouteadd.py <filename>")
    else:
        for arg in sys.argv[1:]:
            try:
                fo = open(arg, 'r')
            except IOError:
                print 'Error: Unable to open the file', arg
        else:
            for line in fo.readlines():
                nline = line.replace('\n', '')
                
                vline = nline.split(" ")
                
                send_route('monksblood-a', vline[0], vline[1], vline[2], vline[3])