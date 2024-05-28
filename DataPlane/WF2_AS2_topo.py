#!/usr/bin/env python3

"""
    Designing the offshore wind farm network topology using the spine-leaf network topology
    Author: Agrippina W. Mwangi
    Created on: April 2024
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.link import TCLink

class MyTopo(Topo):
    def build(self):
        """
        Key:
        1. LDAQ- Local Data acquisition,
        2. MU - Merging Unit,
        3. ECP - Edge Computing node,
        4. vIED - virtual Intelligent Electronic Device
        """
        
        # Host configurations
        host_config = {'defaultRoute': 'via 192.168.1.1'}
        hosts = {
            'LDAQWT1': '192.168.1.10',
            'LDAQWT2': '192.168.1.11',
            'LDAQWT3': '192.168.1.12',
            'LDAQWT4': '192.168.1.13',
            'LDAQWT5': '192.168.1.14',
            'MU1': '192.168.1.20',
            'MU2': '192.168.1.21',
            'MU3': '192.168.1.22',
            'MU4': '192.168.1.23',
            'MU5': '192.168.1.24',
            'vIED1': '192.168.1.30',
            'vIED2': '192.168.1.31',
            'vIED3': '192.168.1.32',
            'vIED4': '192.168.1.33',
            'vIED5': '192.168.1.34',
            'ECP1': '192.168.1.40',
            'ECP2': '192.168.1.41',
            'ECP3': '192.168.1.42',
            'ECP4': '192.168.1.43',
            'ECP5': '192.168.1.44'
        }

        # Creating hosts
        for h, ip in hosts.items():
            self.addHost(h, ip=ip + '/24', **host_config)

        # Switch definitions
        switches = ['WT1_SW1', 'WT1_SW2', 'WT2_SW1', 'WT2_SW2', 'WT3_SW1', 'WT3_SW2', 'WT4_SW1', 'WT4_SW2', 'WT5_SW1', 'WT5_SW2']
        spine_switches = [self.addSwitch(f's{i}', cls=OVSSwitch, failMode='standalone', stp=False) for i in range(1, 6)]
        leaf_switches = [self.addSwitch(f'l{i}', cls=OVSSwitch, failMode='standalone', stp=False) for i in range(1, 21)]

        # Adding all switches
        for sw in switches:
            self.addSwitch(sw)

        # Link configurations
        linkopts = dict(bw=10, delay='5ms', loss=1, use_htb=True)

        # Adding links with specific configurations
        # Linking hosts to their respective switches
        self.addLink('LDAQWT1', 'WT1_SW1', **linkopts)
        self.addLink('LDAQWT2', 'WT2_SW1', **linkopts)
        self.addLink('LDAQWT3', 'WT3_SW1', **linkopts)
        self.addLink('LDAQWT4', 'WT4_SW1', **linkopts)
        self.addLink('LDAQWT5', 'WT5_SW1', **linkopts)

        # Creating spine-leaf network topology
        for i in range(len(spine_switches)):
            for j in range(len(leaf_switches)):
                if j % 5 == i:
                    self.addLink(spine_switches[i], leaf_switches[j], **linkopts)

        # Connecting all leaf switches to create a mesh
        for i in range(len(leaf_switches)):
            for j in range(i + 1, len(leaf_switches)):
                self.addLink(leaf_switches[i], leaf_switches[j], **linkopts)

        # Connect Merging Units, ECPs, and vIEDs to specific leaf switches
        for i in range(1, 6):
            self.addLink(f'MU{i}', f'l{i+5}', **linkopts)
            self.addLink(f'ECP{i}', f'l{i+10}', **linkopts)
            self.addLink(f'vIED{i}', f'l{i+15}', **linkopts)

# Setup Remote Controller
def setup_remote_controller():
    net = Mininet(topo=MyTopo(), link=TCLink, controller=None)
    net.addController('c0', controller=RemoteController, ip='192.168.0.4', port=6653)
    net.start()

    print("Network setup complete. Running CLI.")
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setup_remote_controller()

