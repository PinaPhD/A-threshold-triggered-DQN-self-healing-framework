#!/usr/bin/env python3

'''
Designing the offshore wind farm network topology using the spine-leaf network topology
Author: Agrippina W. Mwangi
Created on: April 2024
'''

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.link import TCLink

class MyTopo(Topo):
    def build(self):
        '''
        Key:
        1. LDAQ - Local Data acquisition,
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

        # Creating the WT Nacelle and Tower switches
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

        # Creating the spine and leaf switches
        cs = self.addSwitch('CS1')  # Core Switch
        sp1 = self.addSwitch('SP1')  # Spine Switch
        sp2 = self.addSwitch('SP2')
        sp3 = self.addSwitch('SP3')
        sp4 = self.addSwitch('SP4')
        sp5 = self.addSwitch('SP5')

        dlf1 = self.addSwitch('DLF1')  # Distribution leaf switch
        dlf2 = self.addSwitch('DLF2')
        dlf3 = self.addSwitch('DLF3')
        dlf4 = self.addSwitch('DLF4')
        dlf5 = self.addSwitch('DLF5')

        alf1 = self.addSwitch('ALF1')  # Access leaf switch
        alf2 = self.addSwitch('ALF2')
        alf3 = self.addSwitch('ALF3')
        alf4 = self.addSwitch('ALF4')
        alf5 = self.addSwitch('ALF5')
        alf6 = self.addSwitch('ALF6')
        alf7 = self.addSwitch('ALF7')
        alf8 = self.addSwitch('ALF8')
        alf9 = self.addSwitch('ALF9')
        alf10 = self.addSwitch('ALF10')
        alf11 = self.addSwitch('ALF11')
        alf12 = self.addSwitch('ALF12')
        alf13 = self.addSwitch('ALF13')
        alf14 = self.addSwitch('ALF14')
        alf15 = self.addSwitch('ALF15')

        # Define link options
        linkopts = dict(bw=100, delay='0.05ms', loss=0.05, use_htb=True)

        # Connect LDAQ to the WT access network
        self.addLink(ldaqwt1, wt1_sw1, **linkopts)
        self.addLink(ldaqwt2, wt2_sw1, **linkopts)
        self.addLink(ldaqwt3, wt3_sw1, **linkopts)
        self.addLink(ldaqwt4, wt4_sw1, **linkopts)
        self.addLink(ldaqwt5, wt5_sw1, **linkopts)

        # Connect the WT nacelle switch to the tower switches
        self.addLink(wt1_sw1, wt1_sw2, **linkopts)
        self.addLink(wt2_sw1, wt2_sw2, **linkopts)
        self.addLink(wt3_sw1, wt3_sw2, **linkopts)
        self.addLink(wt4_sw1, wt4_sw2, **linkopts)
        self.addLink(wt5_sw1, wt5_sw2, **linkopts)

        # Connect the WT tower switches to the spine switches
        self.addLink(wt1_sw2, sp1, **linkopts)
        self.addLink(wt2_sw2, sp2, **linkopts)
        self.addLink(wt3_sw2, sp3, **linkopts)
        self.addLink(wt4_sw2, sp4, **linkopts)
        self.addLink(wt5_sw2, sp5, **linkopts)

        # Connect the spine switches with the core switch
        self.addLink(cs, sp1, **linkopts)
        self.addLink(cs, sp2, **linkopts)
        self.addLink(cs, sp3, **linkopts)
        self.addLink(cs, sp4, **linkopts)
        self.addLink(cs, sp5, **linkopts)

        # Connect the spine switches to the distribution leaf switches
        self.addLink(sp1, dlf1, **linkopts)
        self.addLink(sp2, dlf2, **linkopts)
        self.addLink(sp3, dlf3, **linkopts)
        self.addLink(sp4, dlf4, **linkopts)
        self.addLink(sp5, dlf5, **linkopts)

        # Connect distribution leaf switches to access leaf switches
        self.addLink(dlf1, alf1, **linkopts)
        self.addLink(dlf1, alf2, **linkopts)
        self.addLink(dlf1, alf3, **linkopts)
        self.addLink(dlf2, alf4, **linkopts)
        self.addLink(dlf2, alf5, **linkopts)
        self.addLink(dlf2, alf6, **linkopts)
        self.addLink(dlf3, alf7, **linkopts)
        self.addLink(dlf3, alf8, **linkopts)
        self.addLink(dlf3, alf9, **linkopts)
        self.addLink(dlf4, alf10, **linkopts)
        self.addLink(dlf4, alf11, **linkopts)
        self.addLink(dlf4, alf12, **linkopts)
        self.addLink(dlf5, alf13, **linkopts)
        self.addLink(dlf5, alf14, **linkopts)
        self.addLink(dlf5, alf15, **linkopts)

        # Connect MUs, ECPs, and vIEDs to the ALF switches
        self.addLink(mu1, alf1, **linkopts)
        self.addLink(mu2, alf2, **linkopts)
        self.addLink(mu3, alf3, **linkopts)
        self.addLink(mu4, alf4, **linkopts)
        self.addLink(mu5, alf5, **linkopts)
        
        self.addLink(ecp1, alf6, **linkopts)
        self.addLink(ecp2, alf7, **linkopts)
        self.addLink(ecp3, alf8, **linkopts)
        self.addLink(ecp4, alf9, **linkopts)
        self.addLink(ecp5, alf10, **linkopts)
        
        self.addLink(vied1, alf11, **linkopts)
        self.addLink(vied2, alf12, **linkopts)
        self.addLink(vied3, alf13, **linkopts)
        self.addLink(vied4, alf14, **linkopts)
        self.addLink(vied5, alf15, **linkopts)

topos = {'mytopo': (lambda: MyTopo())}

