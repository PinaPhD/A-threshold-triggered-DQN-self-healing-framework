---
# INSTALLATION GUIDE:
---

# Installing OpenDayLight Oxygen on Ubuntu 22.04 LTS in the Azure Resource Group (RG-ORSTED-ESR1):
* sudo apt-get -y update && sudo apt-get -y upgrade
* sudo apt-get -y install unzip
* sudo apt-get install openjdk-8-jre
* sudo update-alternatives --config java
* java -version
* ls -l /etc/alternatives/java
* echo 'export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre' >> ~/.bashrc
* vim ~/.bashrc
* source ~/.bashrc
* echo $JAVA_HOME


* curl -O https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.8.4/karaf-0.8.4.zip
* unzip karaf-0.8.4.zip
* cd karaf-0.8.4/


# Link address to the OpenDayLight SDN Controller:
* https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.8.4/karaf-0.8.4.zip


# OpenDayLight Features Installed:
* odl-l2switch-switch-ui
* odl-dlux-core
* odl-dluxapps-nodes
* odl-dluxapps-yangui
* odl-dluxapps-yangman
* odl-dluxapps-topology
* odl-restconf
* odl-mdsal-apidocs

# Installing Ubuntu Desktop on the Ubuntu Azure VM
* sudo DEBIAN_FRONTEND=noneinteractive apt-get -y install xfce4
* sudo apt install xfce4-session
* sudo apt-get -y install xrdp
* sudo systemctl enable xrdp
* sudo adduser xrdp ssl-cert
* echo xfce4-session >~/.xsession
* sudo service xrdp restart
* sudo passwd amwangi 

--- Here the password used was (8998)

# Add an inbound security rules for RDP on Azure VM to allow traffic on port 3389 (Exposed to the Internet)


# Accessing the ODL GUI Interface:
* http://172.30.0.4:8181/index.html#/login

# Resources:
* https://developer.cisco.com/codeexchange/github/repo/CiscoDevNet/opendaylight-setup/
* https://docs.opendaylight.org/en/stable-oxygen/
* https://john.soban.ski/install-opendaylight-ubuntu-lts-22-04.html


# Installing Mininet on VM-Mininet in the Azure Resource Group (RG-ORSTED-ESR1):
* sudo apt-get -y update && sudo apt-get -y upgrade
* sudo apt-get -y install mininet
* sudo apt -y iperf3
* iperf3 -v



# Running a test mininet topology connected to the remote controller
* sudo mn --controller=remote,ip=172.30.0.5 --mac -i 10.1.2.0/24 --topo=tree,depth=3,fanout=4

# Running Iperf3 on Mininet to capture network traffic

# Installing a network monitoring tool to observe network performance metrics:
* sudo apt-get -y install --no-install-recommends ubuntu-desktop
* sudo apt-get -y install sflowtool
* sflowtool -p 6343
* sudo apt-get install influxdb
* sudo systemctl enable --now influxdb
* sudo apt-get install grafana
* sudo systemctl enable --now grafana-server

