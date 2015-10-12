#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller,OVSKernelSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

def topology():

    "Create a network."
    net = Mininet( controller=Controller, link=TCLink, switch=OVSKernelSwitch )

    print "*** Creating nodes"
    h1 = net.addHost( 'h1', mac='00:00:00:00:00:01', ip='10.0.0.1/8' )
    s1 = net.addSwitch( 's1', mac='00:00:00:00:00:10' )
    sta1 = net.addStation( 'sta1', wlans=2, mac='00:00:00:00:00:02', ip='10.0.0.2/8' )
    ap1 = net.addBaseStation( 'ap1', ssid= 'ssid_ap1', mode= 'g', channel= '1', position='30,25,0' )
    ap2 = net.addBaseStation( 'ap2', ssid= 'ssid_ap2', mode= 'g', channel= '6', position='70,25,0' )
    ap3 = net.addBaseStation( 'ap3', ssid= 'ssid_ap3', mode= 'g', channel= '11', position='110,25,0' )
    c1 = net.addController( 'c1', controller=Controller )

    print "*** Associating and Creating links"
    net.addLink(s1, h1)
    net.addLink(s1, ap1)
    net.addLink(s1, ap2)
    net.addLink(s1, ap3)
    net.addLink(ap1, sta1)

    sta1.cmd('modprobe bonding mode=3')
    sta1.cmd('ip link add bond0 type bond')
    sta1.cmd('ip link set bond0 address 02:01:02:03:04:08')
    sta1.cmd('ip link set sta1-wlan0 down')
    sta1.cmd('ip link set sta1-wlan0 address 00:00:00:00:00:11')
    sta1.cmd('ip link set sta1-wlan0 master bond0')
    sta1.cmd('ip link set sta1-wlan1 down')
    sta1.cmd('ip link set sta1-wlan1 address 00:00:00:00:00:12')
    sta1.cmd('ip link set sta1-wlan1 master bond0')
    sta1.cmd('ip addr add 10.0.0.10/8 dev bond0')
    sta1.cmd('ip link set bond0 up')

    print "*** Starting network"
    net.build()
    c1.start()
    ap1.start( [c1] )
    ap2.start( [c1] )
    ap3.start( [c1] )
    s1.start( [c1] )

    sta1.cmd('ip addr del 10.0.0.2/8 dev sta1-wlan0')

    """seed"""
    net.seed(12)

    """uncomment to plot graph"""
    net.plotGraph(max_x=140, max_y=140)
    
    "*** Available models: RandomWalk, TruncatedLevyWalk, RandomDirection, RandomWaypoint, GaussMarkov ***"
    net.startMobility(0, model='RandomDirection', max_x=120, max_y=50, min_v=0.4, max_v=0.6)

    print "*** Running CLI"
    CLI( net )

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()