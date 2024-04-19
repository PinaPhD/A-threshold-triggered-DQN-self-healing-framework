Installing ONOS SDN Controller

* Start the Azure VM-SDNC on the resource group (RG-ORSTED-ESR1)
* Connect via Bastion or RDP
* sudo apt-get -y update && sudo apt-get -y upgrade
* sudo apt install git wget vim

#Install mininet 2.3.1b4
$ git clone https://github.com/mininet/mininet.git
$ cd mininet/util
$ git checkout 2.3.1b4
$ ./install.sh -a

Install openjdk-8-jdk
$ sudo apt install openjdk-8-jdk

Append environment variable JAVA_HOME to ~/.bashrc

export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export JRE_HOME=$JAVA_HOME/jre
export CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib
export PATH=$JAVA_HOME/bin:$PATH

$ source ~/.bashrc

Install onos 2.0.0
Download onos binary file:
$ sudo wget -c https://repo1.maven.org/maven2/org/on...
$ tar zxvf onos-2.0.0.tar.gz

Copy files in folder to /opt/onos
$ sudo mkdir /opt/onos 
$ sudo cp -r onos-2.0.0/* /opt/onos

Run onos services 
$ cd /opt/onos/bin
$ sudo /opt/onos/bin/onos-service start

Open another terminal
Add configuration to ~/.ssh/config
$ mkdir ~/.ssh
$ touch ~/.ssh/config

HostKeyAlgorithms +ssh-rsa
PubkeyAcceptedKeyTypes +ssh-rsa

Connect to onos cli and activate application
$ /opt/onos/bin/onos -l onos
password: rocks

onos@root$ app activate org.onosproject.pipelines.basic
onos@root$ app activate org.onosproject.fwd
onos@root$ app activate org.onosproject.openflow

Login GUI
Open browser and type
localhost:8181/onos/ui

username: onos
password: rocks

Run Mininet And PingAll
$ sudo mn --controller remote,ip='your-ip' --switch ovs,protocols=OpenFlow13
mininet $ pingall

If no host icon present on onos gui, press 'h'
