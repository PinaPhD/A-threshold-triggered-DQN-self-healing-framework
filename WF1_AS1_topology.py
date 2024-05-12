"""
    Designing the offshore wind farm network topology using the spine-leaf network topology 
    @Author: Agrippina W. Mwangi
    @Created on: April 2024
"""

from mininet.topo import Topo

class MyTopo( Topo ):
    #Creating the WF1_AS1 Network Topology
    def build( self ):
        
        #Creating hosts
        '''
        Key: 
        1. LDAQ- Local Data acquisition, 
        2. MU - Merging Unit, 
        3. ECP - Edge Computing node, 
        4. vIED - virtual Intelligent Electronic Device
        '''
        
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

        
        #Creating the WT Nacelle/Tower switches, Spine and Leaf Switches
        
        #Wind Turbine Nacelle/Tower Switches
        wt1_sw1 = self.addSwitch('WT1_SW1')    #Nacelle Switch
        wt1_sw2 = self.addSwitch('WT1_SW2')    #Tower Switch
        wt2_sw1 = self.addSwitch('WT2_SW1')
        wt2_sw2 = self.addSwitch('WT2_SW2')
        wt3_sw1 = self.addSwitch('WT3_SW1')
        wt3_sw2 = self.addSwitch('WT3_SW2')
        wt4_sw1 = self.addSwitch('WT4_SW1')
        wt4_sw2 = self.addSwitch('WT4_SW2')
        wt5_sw1 = self.addSwitch('WT5_SW1')
        wt5_sw2 = self.addSwitch('WT5_SW2')
        
        #Spine Switches (sp)
        sp1 = self.addSwitch('SP1')    #Spine Switch
        sp2 = self.addSwitch('SP2')
        sp3 = self.addSwitch('SP3')
        
        #Leaf Switches (fs)
        fs1 = self.addSwitch('fs1')
        fs2 = self.addSwitch('fs2')
        fs3 = self.addSwitch('fs3')
        fs4 = self.addSwitch('fs4')
        fs5 = self.addSwitch('fs5')
        fs6 = self.addSwitch('fs6')
        fs7 = self.addSwitch('fs7')
        fs8 = self.addSwitch('fs8')
        fs9 = self.addSwitch('fs9')
        fs10 = self.addSwitch('fs10')
        fs11 = self.addSwitch('fs11')
        fs12 = self.addSwitch('fs12')
        fs13 = self.addSwitch('fs13')
        fs14 = self.addSwitch('fs14')
        fs15 = self.addSwitch('fs15')
        fs16 = self.addSwitch('fs16')
            
        #Linking the devices  
        # LDAQ connects to the WT Access Network
        # Interface names for LDAQ to WT Access Network links
        self.addLink(ldaqwt1, wt1_sw1, intfName1='ldaqwt1-eth1', intfName2='wt1_sw1-eth1')
        self.addLink(ldaqwt2, wt2_sw1, intfName1='ldaqwt2-eth1', intfName2='wt2_sw1-eth1')
        self.addLink(ldaqwt3, wt3_sw1, intfName1='ldaqwt3-eth1', intfName2='wt3_sw1-eth1')
        self.addLink(ldaqwt4, wt4_sw1, intfName1='ldaqwt4-eth1', intfName2='wt4_sw1-eth1')
        self.addLink(ldaqwt5, wt5_sw1, intfName1='ldaqwt5-eth1', intfName2='wt5_sw1-eth1')

        # Interface names for Nacelle switch to tower switch links
        self.addLink(wt1_sw1, wt1_sw2, intfName1='wt1_sw1-eth2', intfName2='wt1_sw2-eth1')
        self.addLink(wt2_sw1, wt2_sw2, intfName1='wt2_sw1-eth1', intfName2='wt2_sw2-eth1')
        self.addLink(wt3_sw1, wt3_sw2, intfName1='wt3_sw1-eth1', intfName2='wt3_sw2-eth1')
        self.addLink(wt4_sw1, wt4_sw2, intfName1='wt4_sw1-eth1', intfName2='wt4_sw2-eth1')
        self.addLink(wt5_sw1, wt5_sw2, intfName1='wt5_sw1-eth1', intfName2='wt5_sw2-eth1')

        # Interface names for WT Tower Switch to spine switches
        self.addLink(wt1_sw2, sp1, intfName1='wt1_sw2-eth1', intfName2='sp1-eth1')
        self.addLink(wt1_sw2, sp2, intfName1='wt1_sw2-eth2', intfName2='sp2-eth1')
        self.addLink(wt1_sw2, sp3, intfName1='wt1_sw2-eth3', intfName2='sp3-eth1')
        self.addLink(wt2_sw2, sp1, intfName1='wt2_sw2-eth1', intfName2='sp1-eth2')
        self.addLink(wt2_sw2, sp2, intfName1='wt2_sw2-eth2', intfName2='sp2-eth2')
        self.addLink(wt2_sw2, sp3, intfName1='wt2_sw2-eth3', intfName2='sp3-eth2')
        self.addLink(wt3_sw2, sp1, intfName1='wt3_sw2-eth1', intfName2='sp1-eth3')
        self.addLink(wt3_sw2, sp2, intfName1='wt3_sw2-eth2', intfName2='sp2-eth3')
        self.addLink(wt3_sw2, sp3, intfName1='wt3_sw2-eth3', intfName2='sp3-eth3')
        self.addLink(wt4_sw2, sp1, intfName1='wt4_sw2-eth1', intfName2='sp1-eth4')
        self.addLink(wt4_sw2, sp2, intfName1='wt4_sw2-eth2', intfName2='sp2-eth4')
        self.addLink(wt4_sw2, sp3, intfName1='wt4_sw2-eth3', intfName2='sp3-eth4')
        self.addLink(wt5_sw2, sp1, intfName1='wt5_sw2-eth1', intfName2='sp1-eth5')
        self.addLink(wt5_sw2, sp2, intfName1='wt5_sw2-eth2', intfName2='sp2-eth5')
        self.addLink(wt5_sw2, sp3, intfName1='wt5_sw2-eth3', intfName2='sp3-eth5')

        # Interface names for spine network
        self.addLink(sp1, sp2, intfName1='sp1-eth6', intfName2='sp2-eth6')
        self.addLink(sp1, sp3, intfName1='sp1-eth7', intfName2='sp3-eth6')
        self.addLink(sp2, sp1, intfName1='sp2-eth8', intfName2='sp1-eth8')
        self.addLink(sp2, sp3, intfName1='sp2-eth9', intfName2='sp3-eth7')
        self.addLink(sp3, sp1, intfName1='sp3-eth8', intfName2='sp1-eth9')
        self.addLink(sp3, sp2, intfName1='sp3-eth9', intfName2='sp2-eth9')

        # Interface names for mesh links between spine and distribution leaf switches
        self.addLink(sp1, fs1, intfName1='sp1-eth10', intfName2='fs1-eth10')
        self.addLink(sp1, fs2, intfName1='sp1-eth11', intfName2='fs2-eth11')
        self.addLink(sp1, fs3, intfName1='sp1-eth12', intfName2='fs3-eth12')
        self.addLink(sp1, fs4, intfName1='sp1-eth13', intfName2='fs4-eth13')
        self.addLink(sp2, fs1, intfName1='sp2-eth14', intfName2='fs1-eth14')
        self.addLink(sp2, fs2, intfName1='sp2-eth15', intfName2='fs2-eth15')
        self.addLink(sp2, fs3, intfName1='sp2-eth16', intfName2='fs3-eth16')
        self.addLink(sp2, fs4, intfName1='sp2-eth17', intfName2='fs4-eth17')
        self.addLink(sp3, fs1, intfName1='sp3-eth18', intfName2='fs1-eth18')
        self.addLink(sp3, fs2, intfName1='sp3-eth19', intfName2='fs2-eth19')
        self.addLink(sp3, fs3, intfName1='sp3-eth20', intfName2='fs3-eth20')
        self.addLink(sp3, fs4, intfName1='sp3-eth21', intfName2='fs4-eth21')

        # Interface names for leaf network
        self.addLink(fs1, fs2, intfName1='fs1-eth22', intfName2='fs2-eth22')
        self.addLink(fs2, fs3, intfName1='fs2-eth23', intfName2='fs3-eth23')
        self.addLink(fs3, fs4, intfName1='fs3-eth24', intfName2='fs4-eth24')
        self.addLink(fs4, fs5, intfName1='fs4-eth25', intfName2='fs5-eth25')
        self.addLink(fs5, fs6, intfName1='fs5-eth26', intfName2='fs6-eth26')
        self.addLink(fs6, fs7, intfName1='fs6-eth27', intfName2='fs7-eth27')
        self.addLink(fs7, fs8, intfName1='fs7-eth28', intfName2='fs8-eth28')
        self.addLink(fs9, fs10, intfName1='fs9-eth29', intfName2='fs10-eth29')
        self.addLink(fs10, fs11, intfName1='fs10-eth30', intfName2='fs11-eth30')
        self.addLink(fs11, fs12, intfName1='fs11-eth31', intfName2='fs12-eth31')
        self.addLink(fs12, fs13, intfName1='fs12-eth32', intfName2='fs13-eth32')
        self.addLink(fs13, fs14, intfName1='fs13-eth33', intfName2='fs14-eth33')
        self.addLink(fs15, fs16, intfName1='fs15-eth34', intfName2='fs16-eth34')
        self.addLink(fs1, fs16, intfName1='fs1-eth35', intfName2='fs16-eth35')
        self.addLink(fs16, fs2, intfName1='fs16-eth36', intfName2='fs2-eth36')
        self.addLink(fs15, fs5, intfName1='fs15-eth37', intfName2='fs5-eth37')
        self.addLink(fs14, fs4, intfName1='fs14-eth38', intfName2='fs4-eth38')
        self.addLink(fs13, fs3, intfName1='fs13-eth39', intfName2='fs3-eth39')
        self.addLink(fs12, fs6, intfName1='fs12-eth40', intfName2='fs6-eth40')
        self.addLink(fs11, fs7, intfName1='fs11-eth41', intfName2='fs7-eth41')
        self.addLink(fs10, fs4, intfName1='fs10-eth42', intfName2='fs4-eth42')

        # Interface names for MU nodes and other devices
        self.addLink(fs5, mu1, intfName1='fs5-eth43', intfName2='mu1-eth43')
        self.addLink(fs6, mu2, intfName1='fs6-eth44', intfName2='mu2-eth44')
        self.addLink(fs7, mu3, intfName1='fs7-eth45', intfName2='mu3-eth45')
        self.addLink(fs8, mu4, intfName1='fs8-eth46', intfName2='mu4-eth46')
        self.addLink(fs9, mu5, intfName1='fs9-eth47', intfName2='mu5-eth47')
        self.addLink(fs10, vied1, intfName1='fs10-eth48', intfName2='vied1-eth48')
        self.addLink(fs11, vied2, intfName1='fs11-eth49', intfName2='vied2-eth49')
        self.addLink(fs12, vied3, intfName1='fs12-eth50', intfName2='vied3-eth50')
        self.addLink(fs13, vied4, intfName1='fs13-eth51', intfName2='vied4-eth51')
        self.addLink(fs14, vied5, intfName1='fs14-eth52', intfName2='vied5-eth52')
        self.addLink(fs10, ecp1, intfName1='fs10-eth53', intfName2='ecp1-eth53')
        self.addLink(fs11, ecp2, intfName1='fs11-eth54', intfName2='ecp2-eth54')
        self.addLink(fs12, ecp3, intfName1='fs12-eth55', intfName2='ecp3-eth55')
        self.addLink(fs13, ecp4, intfName1='fs13-eth56', intfName2='ecp4-eth56')
        self.addLink(fs14, ecp5, intfName1='fs14-eth57', intfName2='ecp5-eth57')
               
topos = { 'mytopo': (lambda: MyTopo() )}
