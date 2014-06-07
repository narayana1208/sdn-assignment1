'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment 2

Professor: Nick Feamster)
Teaching Assistant: Arpit Gupta, Muhammad Shahbaz
'''

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
#import math

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__( self,linkopts1,linkopts2,linkopts3,fanout):
        super( CustomTopo, self ).__init__()
        # Numbering:  h1..N, s1..M
        self.hostNum = 1
        self.switchNum = 1
	self.depth=3
        # Build topology
        self.addTree(self.depth,fanout,linkopts1,linkopts2,linkopts3)

    def addTree( self,depth,fanout,linkopts1,linkopts2,linkopts3):
        """Add a subtree starting with node n.
           returns: last node added"""
        isSwitch = depth> 0
	print "isSwitch %s "%isSwitch+"in depth %s"%self.depth
	list=[linkopts1,linkopts2,linkopts3]
	#print "in depth %s"%depth
        if isSwitch:
            node = self.addSwitch( 's%s' %self.switchNum )
	    print "switch %s created "%self.switchNum
            self.switchNum += 1
	    #print "switch %s created "%self.switchNum
            for _ in range( fanout ):
		print "in fanout %s"%_
                child = self.addTree( depth - 1, fanout ,linkopts1,linkopts2,linkopts3)
                self.addLink( node, child,**list[depth-1])
		print"in depth link is created %s"%depth+"**linkopts %s"%depth+'**linkopts%s'%depth
        else:
            node = self.addHost( 'h%s' % self.hostNum )
	    print"host%s added"%self.hostNum
            self.hostNum += 1
	    
        return node
        
        # Add your logic here ...

def customTest():
	"Create and Test a Simple Network"
	linkopts1={'bw':10,'delay':'5ms','loss':1,'max_queue_size':1000,'use_htb':True}
	linkopts2={'bw':10,'delay':'5ms','loss':1,'max_queue_size':1000,'use_htb':True}
	linkopts3={'bw':10,'delay':'5ms','loss':1,'max_queue_size':1000,'use_htb':True}
	fanout=2

	topo=CustomTopo(linkopts1,linkopts2,linkopts3,fanout)
	net=Mininet(topo,link=TCLink)
	net.start()
	print "dumping host connections"
	dumpNodeConnections(net.hosts)
	print"Testing network Connectivity"
	net.pingAll()
	print"Testing Bandwidth between h1 and h4"
	h1,h4=net.get('h1','h4')
	net.iperf((h1,h4))
	net.stop()
        
                    
	#topos = { 'custom': ( lambda: CustomTopo() ) }
if __name__=='__main__':
	#tell mininet to print useful information
	setLogLevel('info')
	customTest()
