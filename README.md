---
Implementing self-healing autonomous software-defined OT networks in offshore wind power plants
---


![Self healing framework](https://github.com/PinaPhD/A-threshold-triggered-DQN-self-healing-framework/blob/main/Data/selfheal.png)


###### Executive Summary

Flash events of benign traffic flows and switch thermal instability are key stochastic disruptions causing intermittent network service interruptions in software-defined Industrial Internet of Things (IIoT-Edge) networks for offshore wind power plants (WPPs). 
These stochastic disruptions violate the service level agreements and quality of service requirements enforced to ensure high availability and high performance; for reliable transmission of critical, time-sensitive and best-effort data traffic. 
To mitigate these stochastic disruptions, this paper implements a threshold-triggered Deep Q-Network (DQN) self-healing framework that detects, analyzes, repairs, and adapts network behavior and resources in response to these stochastic disruptions.  
On a Microsoft Azure (Ms-Azure) proof-of-concept testbed, the DQN self-healing framework was trained and tested in software-defined IIoT-Edge networks designed for triple WPP cluster application scenario. 
The testbed comprised Mininet-emulated super spine-leaf switch network topologies at the data plane, ONOS-based controller clusters at the control plane, and the threshold-triggered DQN self-healing agent in the knowledge plane.
Simulation results from this testbed demonstrated that this threshold-triggered DQN self-healing agent outperformed the baseline super spine-leaf switch network algorithms by 53.84% for specific test case scenarios representing varied network states. 
Further, it was observed that the DQN self-healing agent maintained switch temperatures within the nominal operating range by activating select external rack fans. 
These findings highlight the potential of learning algorithms in building the resilience and autonomy of such critical industrial operational technology networks. 


---
A threshold-triggered Deep Q-Network self-healing framework
---


