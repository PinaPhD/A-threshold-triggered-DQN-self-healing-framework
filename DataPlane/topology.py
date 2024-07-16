#!/usr/bin/env python

from mininet.topo import Topo


class sdnnet( Topo ):
    "Creating a simple topology to facilitate the IoT-to-ECP Node data"
    def __init__( self ):
        "Defining the network topology"
        Topo.__init__( self )
        
        
        '''
            OSS rearchitectured as a DataCenter
            Spine-Leaf Switch Network Topology
        '''

        #Creating and adding hosts to the topology
        m1 = self.addHost('m1', ip='10.0.1.10/24', defaultRoute='via 10.0.1.1')
        m2 = self.addHost('m2', ip='10.0.1.11/24', defaultRoute='via 10.0.1.1')
        m3 = self.addHost('m3', ip='10.0.1.12/24', defaultRoute='via 10.0.1.1')
        m4 = self.addHost('m4', ip='10.0.1.13/24', defaultRoute='via 10.0.1.1')
        m5 = self.addHost('m5', ip='10.0.1.14/24', defaultRoute='via 10.0.1.1')
        
        q1 = self.addHost('q1', ip='10.0.1.20/24', defaultRoute='via 10.0.1.1')
        q2 = self.addHost('q2', ip='10.0.1.21/24', defaultRoute='via 10.0.1.1')
        q3 = self.addHost('q3', ip='10.0.1.22/24', defaultRoute='via 10.0.1.1')
        q4 = self.addHost('q4', ip='10.0.1.23/24', defaultRoute='via 10.0.1.1')
        q5 = self.addHost('q5', ip='10.0.1.24/24', defaultRoute='via 10.0.1.1')
        
        e1 = self.addHost('e1', ip='10.0.1.30/24', defaultRoute='via 10.0.1.1')
        e2 = self.addHost('e2', ip='10.0.1.31/24', defaultRoute='via 10.0.1.1')
        e3 = self.addHost('e3', ip='10.0.1.32/24', defaultRoute='via 10.0.1.1')
        e4 = self.addHost('e4', ip='10.0.1.33/24', defaultRoute='via 10.0.1.1')
        e5 = self.addHost('e5', ip='10.0.1.34/24', defaultRoute='via 10.0.1.1')
        
        v1 = self.addHost('v1', ip='10.0.1.40/24', defaultRoute='via 10.0.1.1')
        v2 = self.addHost('v2', ip='10.0.1.41/24', defaultRoute='via 10.0.1.1')
        v3 = self.addHost('v3', ip='10.0.1.42/24', defaultRoute='via 10.0.1.1')
        v4 = self.addHost('v4', ip='10.0.1.43/24', defaultRoute='via 10.0.1.1')
        v5 = self.addHost('v5', ip='10.0.1.44/24', defaultRoute='via 10.0.1.1')
        
        '''
            Creating LDAQ and Actuators for the WTGs
        '''
        r1 = self.addHost('r1', ip='10.0.1.50/24', defaultRoute='via 10.0.1.1')
        r2 = self.addHost('r2', ip='10.0.1.51/24', defaultRoute='via 10.0.1.1')
        r3 = self.addHost('r3', ip='10.0.1.52/24', defaultRoute='via 10.0.1.1')
        r4 = self.addHost('r4', ip='10.0.1.53/24', defaultRoute='via 10.0.1.1')
        r5 = self.addHost('r5', ip='10.0.1.54/24', defaultRoute='via 10.0.1.1')
        r6 = self.addHost('r6', ip='10.0.1.55/24', defaultRoute='via 10.0.1.1')
        r7 = self.addHost('r7', ip='10.0.1.56/24', defaultRoute='via 10.0.1.1')
        r8 = self.addHost('r8', ip='10.0.1.57/24', defaultRoute='via 10.0.1.1')
        r9 = self.addHost('r9', ip='10.0.1.58/24', defaultRoute='via 10.0.1.1')
        r10 = self.addHost('r10', ip='10.0.1.59/24', defaultRoute='via 10.0.1.1')
        r11 = self.addHost('r11', ip='10.0.1.60/24', defaultRoute='via 10.0.1.1')
        r12 = self.addHost('r12', ip='10.0.1.61/24', defaultRoute='via 10.0.1.1')
        r13 = self.addHost('r13', ip='10.0.1.62/24', defaultRoute='via 10.0.1.1')
        r14 = self.addHost('r14', ip='10.0.1.63/24', defaultRoute='via 10.0.1.1')
        r15 = self.addHost('r15', ip='10.0.1.64/24', defaultRoute='via 10.0.1.1')
        r16 = self.addHost('r16', ip='10.0.1.65/24', defaultRoute='via 10.0.1.1')
        r17 = self.addHost('r17', ip='10.0.1.66/24', defaultRoute='via 10.0.1.1')
        r18 = self.addHost('r18', ip='10.0.1.67/24', defaultRoute='via 10.0.1.1')
        r19 = self.addHost('r19', ip='10.0.1.68/24', defaultRoute='via 10.0.1.1')
        r20 = self.addHost('r20', ip='10.0.1.69/24', defaultRoute='via 10.0.1.1')



        b1 = self.addHost('b1', ip='10.0.1.70/24', defaultRoute='via 10.0.1.1')
        b2 = self.addHost('b2', ip='10.0.1.71/24', defaultRoute='via 10.0.1.1')
        b3 = self.addHost('b3', ip='10.0.1.72/24', defaultRoute='via 10.0.1.1')
        b4 = self.addHost('b4', ip='10.0.1.73/24', defaultRoute='via 10.0.1.1')
        b5 = self.addHost('b5', ip='10.0.1.74/24', defaultRoute='via 10.0.1.1')
        b6 = self.addHost('b6', ip='10.0.1.75/24', defaultRoute='via 10.0.1.1')
        b7 = self.addHost('b7', ip='10.0.1.76/24', defaultRoute='via 10.0.1.1')
        b8 = self.addHost('b8', ip='10.0.1.77/24', defaultRoute='via 10.0.1.1')
        b9 = self.addHost('b9', ip='10.0.1.78/24', defaultRoute='via 10.0.1.1')
        b10 = self.addHost('b10', ip='10.0.1.79/24', defaultRoute='via 10.0.1.1')
        b11 = self.addHost('b11', ip='10.0.1.80/24', defaultRoute='via 10.0.1.1')
        b12 = self.addHost('b12', ip='10.0.1.81/24', defaultRoute='via 10.0.1.1')
        b13 = self.addHost('b13', ip='10.0.1.82/24', defaultRoute='via 10.0.1.1')
        b14 = self.addHost('b14', ip='10.0.1.83/24', defaultRoute='via 10.0.1.1')
        b15 = self.addHost('b15', ip='10.0.1.84/24', defaultRoute='via 10.0.1.1')
        b16 = self.addHost('b16', ip='10.0.1.85/24', defaultRoute='via 10.0.1.1')
        b17 = self.addHost('b17', ip='10.0.1.86/24', defaultRoute='via 10.0.1.1')
        b18 = self.addHost('b18', ip='10.0.1.87/24', defaultRoute='via 10.0.1.1')
        b19 = self.addHost('b19', ip='10.0.1.88/24', defaultRoute='via 10.0.1.1')
        b20 = self.addHost('b20', ip='10.0.1.89/24', defaultRoute='via 10.0.1.1')
            
        
        '''
            Creating the ethernet switch network
            Spine-Distribution-Access leaf switch network
        '''
        
        #Spine Switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        
        #Distribution Switches
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')
        s7 = self.addSwitch('s7')
        s8 = self.addSwitch('s8')
        
        #Access Leaf Switches
        s9 = self.addSwitch('s9')
        s10 = self.addSwitch( 's10' )
        s11 = self.addSwitch( 's11' )
        s12 = self.addSwitch( 's12' )
        s13 = self.addSwitch( 's13' )
        s14 = self.addSwitch( 's14' )
        s15 = self.addSwitch( 's15' )
        s16 = self.addSwitch( 's16' )
        s17 = self.addSwitch( 's17' )
        s18 = self.addSwitch( 's18' )
        s19 = self.addSwitch( 's19' )
        s20 = self.addSwitch( 's20' )

        #Creating the Spine Layer
        self.addLink(s1,s2)
        self.addLink(s2,s3)
        self.addLink(s3,s4)

        #Connecting Spine and Distribution Layers
        self.addLink(s1,s5)
        self.addLink(s2,s6)
        self.addLink(s3,s7)
        self.addLink(s4,s8)

        #connecting the Distribution and Access Layers
        self.addLink(s5,s9)
        self.addLink(s5,s10)
        self.addLink(s5,s11)
        
        self.addLink(s6,s12)
        self.addLink(s6,s13)
        self.addLink(s6,s14)

        self.addLink(s7,s15)
        self.addLink(s7,s16)
        self.addLink(s7,s17)

        self.addLink(s8,s18)
        self.addLink(s8,s19)
        self.addLink(s8,s20)

        #Linking the switches to hosts
        self.addLink(m1,s9)
        self.addLink(m2,s10)
        self.addLink(m3,s11)
        self.addLink(m4,s12)
        self.addLink(m5,s13)
        
        self.addLink(q1,s14)
        self.addLink(q2,s15)
        self.addLink(q3,s16)
        self.addLink(q4,s17)
        self.addLink(q5,s18)
        
        self.addLink(e1,s19)
        self.addLink(e2,s20)
        self.addLink(e3,s10)
        self.addLink(e4,s9)
        self.addLink(e5,s13)
        
        self.addLink(v1,s12)
        self.addLink(v2,s11)
        self.addLink(v3,s15)
        self.addLink(v4,s17)
        self.addLink(v5,s19)

        ''' 
           Wind Farm WTG access networks
        '''
       
        #Creating the wind turbine generator Tower Switches
        s21 = self.addSwitch('s21')
        s22 = self.addSwitch('s22')
        s23 = self.addSwitch('s23')
        s24 = self.addSwitch('s24')
        s25 = self.addSwitch('s25')
        s26 = self.addSwitch('s26')
        s27 = self.addSwitch('s27')
        s28 = self.addSwitch('s28')
        s29 = self.addSwitch('s29')
        s30 = self.addSwitch('s30')
        s31 = self.addSwitch('s31')
        s32 = self.addSwitch('s32')
        s33 = self.addSwitch('s33')
        s34 = self.addSwitch('s34')
        s35 = self.addSwitch('s35')
        s36 = self.addSwitch('s36')
        s37 = self.addSwitch('s37')
        s38 = self.addSwitch('s38')
        s39 = self.addSwitch('s39')
        s40 = self.addSwitch('s40')

        #Linking these switches to the spine switches
        self.addLink(s21,s1)
        self.addLink(s22,s1)
        self.addLink(s23,s1)
        self.addLink(s24,s1)
        self.addLink(s25,s1)

        self.addLink(s26,s2)
        self.addLink(s27,s2)
        self.addLink(s28,s2)
        self.addLink(s29,s2)
        self.addLink(s30,s2)

        self.addLink(s31,s3)
        self.addLink(s32,s3)
        self.addLink(s33,s3)
        self.addLink(s34,s3)
        self.addLink(s35,s3)

        self.addLink(s36,s4)
        self.addLink(s37,s4)
        self.addLink(s38,s4)
        self.addLink(s39,s4)
        self.addLink(s40,s4)

        #Linking local data acquisition modules and actuators to each wtg switches
        self.addLink(r1, s21)
        self.addLink(b1, s21)

        self.addLink(r2, s22)
        self.addLink(b2, s22)

        self.addLink(r3, s23)
        self.addLink(b3, s23)

        self.addLink(r4, s24)
        self.addLink(b4, s24)

        self.addLink(r5, s25)
        self.addLink(b5, s25)

        self.addLink(r6, s26)
        self.addLink(b6, s26)

        self.addLink(r7, s27)
        self.addLink(b7, s27)

        self.addLink(r8, s28)
        self.addLink(b8, s28)

        self.addLink(r9, s29)
        self.addLink(b9, s29)

        self.addLink(r10, s30)
        self.addLink(b10, s30)

        self.addLink(r11, s31)
        self.addLink(b11, s31)

        self.addLink(r12, s32)
        self.addLink(b12, s32)

        self.addLink(r13, s33)
        self.addLink(b13, s33)

        self.addLink(r14, s34)
        self.addLink(b14, s34)

        self.addLink(r15, s35)
        self.addLink(b15, s35)

        self.addLink(r16, s36)
        self.addLink(b16, s36)

        self.addLink(r17, s37)
        self.addLink(b17, s37)

        self.addLink(r18, s38)
        self.addLink(b18, s38)

        self.addLink(r19, s39)
        self.addLink(b19, s39)

        self.addLink(r20, s40)
        self.addLink(b20, s40)
        

    
topos = {'mytopo': (lambda: sdnnet() )}
