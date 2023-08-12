#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Node, Controller, OVSSwitch, OVSKernelSwitch, Host
from mininet.cli import CLI
from mininet.link import Intf, TCLink
from mininet.log import setLogLevel, info
from mininet.node import Node, CPULimitedHost
from mininet.util import irange, dumpNodeConnections
from mininet.topo import Topo
import time
import os


class AWF_digital_substation_network(Topo):

	def build(self):
		#Defining the 9 forwarding devices and the gateway router
		info('Adding switches and routers to the AWF Digital substation communication selfwork ... \n\n')
		fd1 = self.addSwitch('FD1')
		fd2 = self.addSwitch('FD2')
		fd3 = self.addSwitch('FD3')
		fd4 = self.addSwitch('FD4')
		fd5 = self.addSwitch('FD5')
		fd6 = self.addSwitch('FD6')
		fd7 = self.addSwitch('FD7')
		fd8 = self.addSwitch('FD8')
		fd9 = self.addSwitch('FD9')
		#RG1 = self.addHost('Gateway',cls=LinuxRouter, ip='10.3.4.1/16')
		#RG2 = self.addHost('ISP',cls=LinuxRouter,ip='10.2.4.1/16')
		#RG3 = self.addHost('ENTERPRISE-selfWORK',cls=LinuxRouter,ip='10.2.4.2/16')

		"""
		Defining the merging units (MUs) and protection,fault equipment
		"""
		info('Adding Merging Units to the AWF Offshore Digital Substation selfwork ... \n\n')
		#Merging Units (MU Hosts)
		mu1 = self.addHost('MU1')
		mu2 = self.addHost('MU2')
		mu3 = self.addHost('MU3')

		mu4 = self.addHost('MU4')
		mu5 = self.addHost('MU5')
		mu6 = self.addHost('MU6')

		#Protection and Fault Recording Equipment (PR and FR Hosts)
		info('Adding Protection and Fault recording equipment to the Onshore Control room ... \n\n')
		pr2 = self.addHost('PR2')
		pr3 = self.addHost('PR3')

		vied1 = self.addHost('VIED1')
		vied2 = self.addHost('VIED2')
		vied3 = self.addHost('VIED3')
		vied4 = self.addHost('VIED4')
		vied5 = self.addHost('VIED5')

		pqr1 = self.addHost('PQR1')
		pqr2 = self.addHost('PQR2')
		rtu = self.addHost('RTU')

		fr1 = self.addHost('FR1')
		fr2 = self.addHost('FR2')


		"""
		Adding hosts to the forwarding devices and linking the routers
		"""

		#Part 1: The IT/OT links between routers and distribution level FDs
		#info('Linking the OT Gateway to the ISP and Enterprise selfwork (IT) ... \n\n')
		#self.addLink(RG1,RG2,bw=20, delay = '0.01ms')   #Linking gateway to ISP router on a 2gbps optical fiber link
		#self.addLink(RG2,RG3,bw=15, delay = '0.01ms')   #Linking ISP to Enterprise selfwork router on a 2gbps optical fiber link
        #self.addLink(fd9,RG1) #Linking the OT network to the Internet (via a RG1 gateway)
        
        #Part 2: The Distribution layer FD links
		info('Linking the distribution layer forwarding devices ... \n\n')
		self.addLink(fd4,fd3)    #LC-LC fiber patch cords at 1Gbps duplex (ODS)
		self.addLink(fd4,fd5)   #A single model subsea optical fiber cable on 2gbps
		self.addLink(fd3,fd6)   #A single model subsea optical fiber cable on 2gbps
		self.addLink(fd5,fd6)    #LC-LC fiber patch cords at 1Gbps duplex (OCR)

		#Linking the distribution layer and the access layer
		self.addLink(fd1,fd4)
		self.addLink(fd2,fd3)
		self.addLink(fd5,fd7)
		self.addLink(fd6,fd8)
		self.addLink(fd7,fd9)
		self.addLink(fd8,fd9)
		self.addLink(fd1,fd2)

		#Part 3: The Access layer FD links - OFFSHORE WIND FARM DIGITAL SUBSTATION
		info('Linking the access layer forwarding devices with their attached nodes or hosts ... \n\n')
		self.addLink(fd1,mu1)
		self.addLink(fd1,mu2)
		self.addLink(fd1,mu3)

		self.addLink(fd2,mu4)
		self.addLink(fd2,mu5)
		self.addLink(fd2,mu6)

		#Part 4: The Access layer FD links - ONSHORE CONTROL ROOM
		self.addLink(fd7,vied1)
		self.addLink(fd7,vied2)
		self.addLink(fd7,pr2)
		self.addLink(fd7,pr3)

		self.addLink(fd8,vied3)
		self.addLink(fd8,vied4)
		self.addLink(fd8,vied5)
		self.addLink(fd8,pqr1)
		self.addLink(fd8,pqr2)
		
		info("Linking the gateway to the protection and fault recording devices in the OT onshore control room ... \n\n")
		self.addLink(fd9,fr1)
		self.addLink(fd9,rtu)
		self.addLink(fd9,fr2)

topos = {'awfnet': AWF_digital_substation_network}