
"""
Designing the offshore wind farm network topology using the spine-leaf network topology
Author: Agrippina W. Mwangi
Created on: April 2024
"""

from mininet.topo import Topo
from mininet.node import OVSSwitch


class MyTopo(Topo):
    
    # Create a constructor to launch STP that prevents network loops due to the spine-leaf mesh connections
    def __init__(self):
	Topo.__init__(self,switch=OVSSwitch, stp=True)
	self.build()


    # Creating the WF1_AS1 Network Topology
    def build(self):
        '''
        Key:
        1. LDAQ- Local Data acquisition, 
        2. MU - Merging Unit, 
        3. ECP - Edge Computing node, 
        4. vIED - virtual Intelligent Electronic Device
        '''

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

        '''
        Creating the WT Nacelle and Tower switches, Spine and Leaf Switches
        '''

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
        
        #Connecting the local data acquisition nodes to the wind turbine nacelle access switches
        self.addLink(ldaqwt1,wt1_sw1)
        self.addLink(ldaqwt2,wt2_sw1)
        self.addLink(ldaqwt3,wt3_sw1)
        self.addLink(ldaqwt4,wt4_sw1)
        self.addLink(ldaqwt5,wt5_sw1)

        # Creating spine-leaf network topology
        spine_switches = [self.addSwitch(f's{i}', cls=OVSSwitch, stp=True) for i in range(1, 5)]
        leaf_switches = [self.addSwitch(f'l{i}', cls=OVSSwitch, stp=True) for i in range(1, 21)]

        # Creating mesh connections between spine switches
        for i in range(len(spine_switches)):
            for j in range(i + 1, len(spine_switches)):
                self.addLink(spine_switches[i], spine_switches[j])

        # Creating mesh connections between leaf switches
        for i in range(len(leaf_switches)):
            for j in range(i + 1, len(leaf_switches)):
                self.addLink(leaf_switches[i], leaf_switches[j])

        # Connecting each spine switch to the first four leaf switches
        for spine in spine_switches:
            for leaf in leaf_switches[:4]:  # Only the first 4 leaf switches
                self.addLink(spine, leaf)

        # Linking all wt*_sw2 tower switches to each of the spine switches
        tower_switches = [wt1_sw2, wt2_sw2, wt3_sw2, wt4_sw2, wt5_sw2]
        for tower_switch in tower_switches:
            for spine_switch in spine_switches:
                self.addLink(tower_switch, spine_switch)

        # Connect MU hosts to leaf switches l4 to l10
        mu_hosts = [mu1, mu2, mu3, mu4, mu5]
        for idx, mu_host in enumerate(mu_hosts):
            leaf_index = 4 + idx  # Starting from leaf switch l4
            self.addLink(mu_host, leaf_switches[leaf_index - 1])

        # Connect ECP hosts to leaf switches l11 to l15
        ecp_hosts = [ecp1, ecp2, ecp3, ecp4, ecp5]
        for idx, ecp_host in enumerate(ecp_hosts):
            leaf_index = 11 + idx  # Starting from leaf switch l11
            self.addLink(ecp_host, leaf_switches[leaf_index - 1])

        # Connect vIED hosts to leaf switches l16 to l20
        vied_hosts = [vied1, vied2, vied3, vied4, vied5]
        for idx, vied_host in enumerate(vied_hosts):
            leaf_index = 16 + idx  # Starting from leaf switch l16
            self.addLink(vied_host, leaf_switches[leaf_index - 1])

topos = {'mytopo': (lambda: MyTopo())}
