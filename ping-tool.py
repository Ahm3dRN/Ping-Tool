from netaddr import *
from scapy.all import *
from termcolor import colored
import subprocess
import colorama
import timeit
import sys

colorama.init()

#.iter_hosts()
class Ping_Tool:
    def __init__(self,network):
        self.network = network

    def subprocess_ping(self):
        ip = IPNetwork(self.network)
        live_hosts=[]
        dead_hosts=[]
        start = timeit.default_timer()
        try:
            for host in ip.iter_hosts():
                
                request = subprocess.Popen(['ping',str(host)], stdout=subprocess.PIPE)
                #request.wait()
                #print str(request.returncode())
                output,error = request.communicate()
                
                if "bytes=32" in output:
                    print colored(str(host), 'white')
                    live_hosts.append(host)
                else:
                     print colored(str(host), 'yellow')                
                    
            stop = timeit.default_timer()
            time_taken = stop - start
        except KeyboardInterrupt:
            print "exiting..."
            sys.exit()
            
        print "Scan Finished! Scan Took {} s.\n {} Host Alive.\n{} Host Dead".foramt(str(time_taken),str(len(live_hosts)), str(len(dead_hosts)))
    def scapy_ping(self):
        ip = IPNetwork(self.network)
        live_hosts=[]
        dead_hosts=[]
        start = timeit.default_timer()
        try:
            for host in ip.iter_hosts():
                ping = sr1(IP(dst=str(host))/ICMP(), timeout=2,verbose=0)
                if str(type(ping)) == "<type 'NoneType'>":
                    print colored(str(host), 'yellow')
                    dead_hosts.append(host)
                
                elif int(ping.getlayer(ICMP).type)==3 and int(ping.getlayer(ICMP).code) in [1,2,3,9,10,13]:
                    print colored(str(host), 'yellow')
                    dead_hosts.append(host)
                else:
                    print colored(str(host),'white')
                    live_hosts.append(host)
            stop = timeit.default_timer()
            time_taken = stop - start
        except KeyboardInterrupt:
            print "exiting..."
            sys.exit()
            
        print "Scan Finished! Scan Took {} s.\n {} Host Alive.\n{} Host Dead".foramt(str(time_taken),
                                                                                     str(len(live_hosts)),
                                                                                     str(len(dead_hosts)))    
if __name__ == "__main__":
    usage = 'usage: pingtool.py <ip-range> <type>\nargument:\ntype: [1] Scapy Ping!,[2] Terminal Ping!\n'
    if len(sys.argv) == 3:
        
        network = sys.argv[1]
        scan_type = sys.argv[2]
        parent = Ping_Tool(network)
        if scan_type == '1':
            parent.scapy_ping()
        elif scan_type == '2':
            parent.subprocess_ping()
        else:
            raw_input(usage)
    elif len(sys.argv) == 1:
        network = raw_input('Enter Ip Ragne To Ping> ')
        parent = Ping_Tool(network)
        scan_type = raw_input('[1] Scapy Ping!\n[2] Terminal Ping!\n> ')
        if scan_type == '1':
            parent.scapy_ping()
        elif scan_type == '2':
            parent.subprocess_ping()
        else:
            print('[-] Please Enter A Valid Choice!')
    else:
        print(usage)
