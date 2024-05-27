#!/usr/bin/env python3

"""
    Designing the offshore wind farm network topology using the spine-leaf network topology
    Author: Agrippina W. Mwangi
    Created on: April 2024
"""

from mininet.topo import Topo
#from mininet.node import OVSSwitch

class MyTopo(Topo):
    # Create a constructor to launch STP that prevents network loops due to the spine-leaf mesh connections
    #def __init__(self):
       # Topo.__init__(self, switch=OVSSwitch, stp=True)
        #self.build()

    # Creating the WF1_AS1 Network Topology
    def build(self):
        """
        Key:
        1. LDAQ- Local Data acquisition,
        2. MU - Merging Unit,
        3. ECP - Edge Computing node,
        4. vIED - virtual Intelligent Electronic Device
        """

        # Creating hosts
        ldaqwt1 = self.addHost('LDAQWT1', ip='192.168.1.10/24', defaultRoute='via 192.168.1.1')
        ldaqwt2 = self.addHost('LDAQWT2', ip='192.168.1.11/24', defaultRoute='via 192.168.1.1')
        ldaqwt3 = self.addHost('LDAQWT3', ip='192.168.1.12/24', defaultRoute='via 192.168.1.1')
        ldaqwt4 = self.addHost('LDAQWT4', ip='192.168.1.13/24', defaultRoute='via 192.168.1.1')
        ldaqwt5 = self.addHost('LDAQWT5', ip='192.168.1.14/24', defaultRoute='via 192.168.1.1')

        mu1 = self.addHost('MU1', ip='192.168.1.20/24', defaultRoute='via 192.168.1.1')
        mu2 = self.addHost('MU2', ip='192.168.1.21/24', defaultRoute='via 192.168.1.1')
        mu3 = self.addHost('MU3', ip='192.168.1.22/24', defaultRoute='via 192.168.1.1')
        mu4 = self.addHost('MU4', ip='192.168.1.23/24', defaultRoute='via 192.168.1.1')
        mu5 = self.addHost('MU5', ip='192.168.1.24/24', defaultRoute='via 192.168.1.1')

        vied1 = self.addHost('vIED1', ip='192.168.1.30/24', defaultRoute='via 192.168.1.1')
        vied2 = self.addHost('vIED2', ip='192.168.1.31/24', defaultRoute='via 192.168.1.1')
        vied3 = self.addHost('vIED3', ip='192.168.1.32/24', defaultRoute='via 192.168.1.1')
        vied4 = self.addHost('vIED4', ip='192.168.1.33/24', defaultRoute='via 192.168.1.1')
        vied5 = self.addHost('vIED5', ip='192.168.1.34/24', defaultRoute='via 192.168.1.1')

        ecp1 = self.addHost('ECP1', ip='192.168.1.40/24', defaultRoute='via 192.168.1.1')
        ecp2 = self.addHost('ECP2', ip='192.168.1.41/24', defaultRoute='via 192.168.1.1')
        ecp3 = self.addHost('ECP3', ip='192.168.1.42/24', defaultRoute='via 192.168.1.1')
        ecp4 = self.addHost('ECP4', ip='192.168.1.43/24', defaultRoute='via 192.168.1.1')
        ecp5 = self.addHost('ECP5', ip='192.168.1.44/24', defaultRoute='via 192.168.1.1')

        # Creating the WT Nacelle and Tower switches, Spine and Leaf Switches
        wt1_sw1 = self.addSwitch('WT1_SW1')  # Nacelle Switch
        wt1_sw2 = self.addSwitch('WT1_SW2')  # Tower Switch
        wt2_sw1 = self.addSwitch('WT2_SW1')
        wt2_sw2 = self.addSwitch('WT2_SW2')
        wt3_sw1 = self.addSwitch('WT3_SW1')
        wt3_sw2 = self.addSwitch('WT3_SW2')
        wt4_sw1 = self.addSwitch('WT4_SW1')
        wt4_sw2 = self.addSwitch('WT4_SW2')
        wt5_sw1 = self.addSwitch('WT5_SW1')
        wt5_sw2 = self.addSwitch('WT5_SW2')

        # Connecting the local data acquisition nodes to the wind turbine nacelle access switches
        self.addLink(ldaqwt1, wt1_sw1)
        self.addLink(ldaqwt2, wt2_sw1)
        self.addLink(ldaqwt3, wt3_sw1)
        self.addLink(ldaqwt4, wt4_sw1)
        self.addLink(ldaqwt5, wt5_sw1)

        # Creating spine-leaf network topology
        spine_switches = [self.addSwitch(f's{i}') for i in range(1, 6)]
        leaf_switches = [self.addSwitch(f'l{i}') for i in range(1, 21)]

        #Connecting the wind turbine tower switch and spine switch
        self.addLink(wt1_sw2,spine_switches[1])
        self.addLink(wt2_sw2,spine_switches[2])
        self.addLink(wt3_sw2,spine_switches[3])
        self.addLink(wt4_sw2,spine_switches[4])
        self.addLink(wt5_sw2,spine_switches[5])
        
        #Connecting all the spine switches to each other
        self.addLink(spine_switches[1],spine_switches[2])
        self.addLink(spine_switches[2],spine_switches[3])
        self.addLink(spine_switches[3],spine_switches[4])
        self.addLink(spine_switches[4],spine_switches[5])
        
        #Connecting each of the spine switches to all the distribution level leaf switches
        self.addLink(spine_switches[1],leaf_switches[1])
        self.addLink(spine_switches[1],leaf_switches[2])
        self.addLink(spine_switches[1],leaf_switches[3])
        self.addLink(spine_switches[1],leaf_switches[4])
        self.addLink(spine_switches[1],leaf_switches[5])

        self.addLink(spine_switches[2],leaf_switches[1])
        self.addLink(spine_switches[2],leaf_switches[2])
        self.addLink(spine_switches[2],leaf_switches[3])
        self.addLink(spine_switches[2],leaf_switches[4])
        self.addLink(spine_switches[2],leaf_switches[5])

        self.addLink(spine_switches[3],leaf_switches[1])
        self.addLink(spine_switches[3],leaf_switches[2])
        self.addLink(spine_switches[3],leaf_switches[3])
        self.addLink(spine_switches[3],leaf_switches[4])
        self.addLink(spine_switches[3],leaf_switches[5])

        self.addLink(spine_switches[4],leaf_switches[1])
        self.addLink(spine_switches[4],leaf_switches[2])
        self.addLink(spine_switches[4],leaf_switches[3])
        self.addLink(spine_switches[4],leaf_switches[4])
        self.addLink(spine_switches[4],leaf_switches[5])

        self.addLink(spine_switches[5],leaf_switches[1])
        self.addLink(spine_switches[5],leaf_switches[2])
        self.addLink(spine_switches[5],leaf_switches[3])
        self.addLink(spine_switches[5],leaf_switches[4])
        self.addLink(spine_switches[5],leaf_switches[5])

        #connecting the distribution level leaf switches to the access level leaf switches
        self.addLink(leaf_switches[1],leaf_switches[6])
        self.addLink(leaf_switches[1],leaf_switches[7])
        self.addLink(leaf_switches[1],leaf_switches[8])

        self.addLink(leaf_switches[2],leaf_switches[9])
        self.addLink(leaf_switches[2],leaf_switches[10])
        self.addLink(leaf_switches[2],leaf_switches[11])

        self.addLink(leaf_switches[3],leaf_switches[12])
        self.addLink(leaf_switches[3],leaf_switches[13])
        self.addLink(leaf_switches[3],leaf_switches[14])
        
        self.addLink(leaf_switches[4],leaf_switches[15])
        self.addLink(leaf_switches[4],leaf_switches[16])
        self.addLink(leaf_switches[4],leaf_switches[17])

        self.addLink(leaf_switches[5],leaf_switches[18])
        self.addLink(leaf_switches[5],leaf_switches[19])
        self.addLink(leaf_switches[5],leaf_switches[20])
        
        #Connecting the Merging units in the OSS to the access level leaf switches
        self.addLink(mu1,leaf_switches[6])
        self.addLink(mu2,leaf_switches[7])
        self.addLink(mu3,leaf_switches[8])
        self.addLink(mu4,leaf_switches[9])
        self.addLink(mu5,leaf_switches[10])

        self.addLink(ecp1,leaf_switches[11])
        self.addLink(ecp2,leaf_switches[12])
        self.addLink(ecp3,leaf_switches[13])
        self.addLink(ecp4,leaf_switches[14])
        self.addLink(ecp5,leaf_switches[15])

        self.addLink(vied1,leaf_switches[16])
        self.addLink(vied2,leaf_switches[17])
        self.addLink(vied3,leaf_switches[18])
        self.addLink(vied4,leaf_switches[19])
        self.addLink(vied5,leaf_switches[20])



topos = {'mytopo': (lambda: MyTopo())}


