---
Implementing self-healing autonomous software-defined OT networks in offshore wind power plants
---

Autonomous software-defined OT networks in offshore Wind Power Plants (WPPs) enforce rigorous Service Level Agreements (SLAs) and Quality of Service (QoS) requirements to ensure reliable transmission of critical time-sensitive and best-effort data traffic. 
Flash events of benign traffic flows causes network congestion resulting in intermittent network service interruptions which are undesirable for the offshore WPP operators. 
This study proposes an externally adapted Deep Q-Networks (DQN) agent within the _"Observe-Orient-Decide-Act"_ Closed Control Loop (CCL) self-healing framework. 
This agent detects traffic anomalies, learns optimal paths, and places rules in the SDN controller to reroute traffic, thereby maximizing network throughput and minimizing end-to-end latency.




##### Setting up Ms-Azure Resource Group Proof-of-Concept Testbed


Data plane virtual machine (VM) setup on the Ms-Azure Resource Group:
- sudo apt-get update && sudo apt-get upgrade
- sudo apt install ubuntu-desktop -y
- sudo apt-get -y install xrdp
- sudo systemctl enable xrdp
- sudo adduser xrdp ssl-cert
- echo gnome-session > ~/.xsession
- sudo service xrdp restart
- sudo ufw allow 3389/tcp
- sudo passwd amwangi254

##### Installing Mininet on the Ubuntu Desktop (GUI) version:
- sudo apt install git python3-pip -y
- git clone https://github.com/mininet/mininet
- cd mininet
- sudo ./util/install.sh -a

Running the offshore WPP Network Topology [AS1 Network Topology](https://github.com/PinaPhD/JP3/blob/main/DataPlane/dataplane.py)
Running Wireshark:
```bash
sudo -E wireshark

##### Setting up the ONOS SDN Controller Cluster:
- sudo apt-get -y update && sudo apt-get -y upgrade
- sudo apt install git wget vim
- Append environment variable JAVA_HOME to ~/.bashrc
  
```bash
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export JRE_HOME=$JAVA_HOME/jre
export CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib
export PATH=$JAVA_HOME/bin:$PATH
