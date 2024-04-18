---
INSTALLATION GUIDE:
---

Installing OpenDayLight Oxygen on Ubuntu 22.04 LTS in the Azure Resource Group (RG-ORSTED-ESR1):
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


Link address to the OpenDayLight SDN Controller:
* https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.8.4/karaf-0.8.4.zip


OpenDayLight Features Installed:
* odl-l2switch-switch-ui
* odl-dlux-core
* odl-dluxapps-nodes
* odl-dluxapps-yangui
* odl-dluxapps-yangman
* odl-dluxapps-topology
* odl-restconf
* odl-mdsal-apidocs


Accessing the ODL GUI Interface:
* http://172.30.0.4:8181/index.html#/login

Resources:
* https://developer.cisco.com/codeexchange/github/repo/CiscoDevNet/opendaylight-setup/
* https://docs.opendaylight.org/en/stable-oxygen/
* https://john.soban.ski/install-opendaylight-ubuntu-lts-22-04.html
