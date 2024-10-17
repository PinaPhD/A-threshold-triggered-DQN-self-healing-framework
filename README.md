## Implementing self-healing autonomous software-defined OT networks in offshore wind power plants


---
![Self healing framework](https://github.com/PinaPhD/A-threshold-triggered-DQN-self-healing-framework/blob/main/Data/selfheal.png)
---

### Contributors
1. Agrippina Mwangi (Lead Developer and Researcher) - [LinkedIn](https://dk.linkedin.com/in/agrippina-mwangi-3b512517a)
2. León Navarro-Hilfiker (OT Security Engineer) -[LinkedIn](https://www.linkedin.com/in/le%C3%B3n-navarro-hilfiker-320979254)


## Table of Contents

1. [Executive Summary](#summary)
2. [Pre-requisites](#requirements)
3. [Data Plane Design](#data-plane-design)
4. [Temperature Module](#temperature-module)
4. [Control Plane Design](#control-plane-design)
5. [Knowledge Plane Design](#knowledge-plane-design)
6. [Conclusion](#conclusion)
7. [References](#references)



## Executive Summary

Flash events of benign traffic flows and switch thermal instability are key stochastic disruptions causing intermittent network service interruptions in software-defined Industrial Internet of Things (IIoT-Edge) networks for offshore wind power plants (WPPs). 
These stochastic disruptions violate the service level agreements and quality of service requirements enforced to ensure high availability and high performance; for reliable transmission of critical, time-sensitive and best-effort data traffic. 
To mitigate these stochastic disruptions, this study implements a threshold-triggered Deep Q-Network (DQN) self-healing framework that detects, analyzes, repairs, and adapts network behavior and resources in response to these stochastic disruptions.  
On a Microsoft Azure (Ms-Azure) proof-of-concept testbed, the DQN self-healing framework was trained and tested in software-defined IIoT-Edge networks designed for triple WPP cluster application scenario. 
The testbed comprised Mininet-emulated super spine-leaf switch network topologies at the data plane, ONOS-based controller clusters at the control plane, and the threshold-triggered DQN self-healing agent in the knowledge plane.
Simulation results from this testbed demonstrated that this threshold-triggered DQN self-healing agent outperformed the baseline super spine-leaf switch network algorithms by 53.84% for specific test case scenarios representing varied network states. 
Further, it was observed that the DQN self-healing agent maintained switch temperatures within the nominal operating range by activating select external rack fans. 
These findings highlight the potential of learning algorithms in building the resilience and autonomy of such critical industrial operational technology networks. 



## Pre-requisites

1. Create a Microsoft Azure (Ms-Azure) account and get a subscription.
2. Create an Ms-Azure resource group and assign it subnets, a network security group, and Bastion.
2. Create several Linux virtual machines in this Ms-Azure Resource Group with the following compute and storage specifications: 
    - Linux Ubuntu server 22.04 lts-Gen2 x64, 2 vCPUs (16GiB RAM), 128-512GB SSD/HDD
    - Docker ver. 24.0.7
    - Mininet Ver. 2.3.0
    - InfluxdB Ver.2.7.10
    - Python Ver.3.12.3

See the [Installation Guide](https://github.com/PinaPhD/A-threshold-triggered-DQN-self-healing-framework/blob/main/ControlPlane/ONOS.md)

Alternatively, get a physical server and proceed from step 2.



## Data Plane Design
- On one of the VMs with Mininet Installation run the [network topology](https://github.com/PinaPhD/A-threshold-triggered-DQN-self-healing-framework/blob/main/DataPlane/topology.py) for an offshore wind farm (reduce model with 20 WTGs communicating with one OSS)
- At the Mininet prompt, run xterm on select mininet hosts to initialize traffic generation using the following data sets:
    - [MQTT sensor data traffic](https://github.com/PinaPhD/A-threshold-triggered-DQN-self-healing-framework/tree/main/DataPlane/IIoT_ECP_Socket)
    - [IEC61850 SV/GOOSE docker based data traffic](https://github.com/mz-automation/libiec61850)
    - Ordinary ping tests

- To monitor network performance, use the [iperf3](https://iperf.fr/) tool for active measurements of network latency, throughput, jitter, packet loss (loss of datagrams).

## Temperature Module
- 


## Control Plane Design

- On one of the VMs, download the [ONOS ver.2.0.0](https://repo1.maven.org/maven2/org/onosproject/onos-releases/2.0.0/onos-2.0.0.tar.gz) SDN Controller.
- Create a cluster using the _"org.onosproject.cluster-ha"_ ONOS SDN controller feature.
- Install the following ONOS features:
    - org.onosproject.pipelines.basic
    - org.onosproject.fwd
    - org.onosproject.openflow
    - org.onosproject.cpman
    - org.onosproject.metrics

- See more information on ONOS installation and design [here](https://wiki.onosproject.org/display/ONOS/ONOS).
- The Knowledge plane interacts with the ONOS SDN Controller [subsystems](https://github.com/PinaPhD/A-threshold-triggered-DQN-self-healing-framework/tree/main/Images/onos-subsystems.png) using RESTFul APIs from the Northbound Interface.


## Knowledge Plane Design
- On one of the VMs, download Anaconda and install the relevant Tensorflow and Keras dependencies in a new environment (_not the base_). 
- The knowledge plane hosts 4 modules namely: Observe, Orient, Decide, and Act modules. These modules interact with each other exchanging important network performance information derived from the ONOS SDN controller topology manager, statistics manager, and flow rule manager as shown in the [self-healing framework](https://github.com/PinaPhD/A-threshold-triggered-DQN-self-healing-framework/blob/main/Data/selfheal.png).
- Detailed descriptions of each module and associated source files:
    - Observe module ([Description](https://pinaphd.github.io/testbed/topic6/topic65/observe.html)) ([Source File](https://github.com/PinaPhD/A-threshold-triggered-DQN-self-healing-framework/blob/main/KnowledgePlane/OODA-MySQL/Observe.py))
    - Orient Module ([Description]()) ([Source File](https://github.com/PinaPhD/A-threshold-triggered-DQN-self-healing-framework/blob/main/KnowledgePlane/OODA-MySQL/Orient_MySQL.py))
    - Decide Module ([Description]()) ([Source File](https://github.com/PinaPhD/A-threshold-triggered-DQN-self-healing-framework/blob/main/KnowledgePlane/OODA-MySQL/Decide_MySQL.py))
    - Act Module ([Description]() ) ([Source File](https://github.com/PinaPhD/A-threshold-triggered-DQN-self-healing-framework/blob/main/KnowledgePlane/OODA-MySQL/Act_MySQL.py))
    
    
## Conclusion


## References

- More studies from us and cite our work: [Reference list](https://github.com/PinaPhD/A-threshold-triggered-DQN-self-healing-framework/blob/main/References.md)
