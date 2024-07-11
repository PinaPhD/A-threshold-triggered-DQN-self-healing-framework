---
Implementing self-healing autonomous software-defined OT networks in offshore wind power plants
---

Autonomous software-defined OT networks in offshore Wind Power Plants (WPPs) enforce rigorous Service Level Agreements (SLAs) and Quality of Service (QoS) requirements to ensure reliable transmission of critical time-sensitive and best-effort data traffic. 
Flash events of benign traffic flows causes network congestion resulting in intermittent network service interruptions which are undesirable for the offshore WPP operators. 
This study proposes an externally adapted Deep Q-Networks (DQN) agent within the _"Observe-Orient-Decide-Act"_ Closed Control Loop (CCL) self-healing framework. 
This agent detects traffic anomalies, learns optimal paths, and places rules in the SDN controller to reroute traffic, thereby maximizing network throughput and minimizing end-to-end latency.




#### Setting up Ms-Azure Resource Group Proof-of-Concept Testbed


Virtual machine (VM) setup on the Ms-Azure Resource Group:
```bash
sudo apt-get update && sudo apt-get upgrade
sudo apt install ubuntu-desktop -y
sudo apt-get -y install xrdp
sudo systemctl enable xrdp
sudo adduser xrdp ssl-cert
echo gnome-session > ~/.xsession
sudo service xrdp restart
sudo ufw allow 3389/tcp
sudo passwd amwangi254
```

#### Installing Mininet on the Ubuntu Desktop (GUI) version:

```bash
sudo apt install git python3-pip -y
git clone https://github.com/mininet/mininet
cd mininet
sudo ./util/install.sh -a
```

Running the offshore WPP Network Topology [AS1 Network Topology](https://github.com/PinaPhD/JP3/blob/main/DataPlane/dataplane.py)

In the Mininet CLI prompt, using xterm instantiate the data transfers between all the communicating nodes (IIoT sensors, Merging Units, vIEDs, ECP units, and actuators)
```bash
xterm <host_name> <host_name> <host_name> ...
```

Running Wireshark:

```bash
sudo -E wireshark
```

#### Setting up the ONOS SDN Controller Cluster:

```bash
sudo apt-get -y update && sudo apt-get -y upgrade
sudo apt install git wget vim
```

Append environment variable JAVA_HOME to ~/.bashrc 
```bash
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export JRE_HOME=$JAVA_HOME/jre
export CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib
export PATH=$JAVA_HOME/bin:$PATH
```

Installing ONOS Ver2.0.0 (_Loon_)

Download the onos binary file:  `sudo wget -c https://repo1.maven.org/maven2/org/onosproject/onos-releases/2.0.0/onos-2.0.0.tar.gz`

```bash
tar zxvf onos-2.0.0.tar.gz
sudo mkdir /opt/onos 
sudo cp -r onos-2.0.0/* /opt/onos
```

Run onos services 
```bash
cd /opt/onos/bin
sudo /opt/onos/bin/onos-service start
```

Open another terminal and add configuration to ~/.ssh/config
```bash
mkdir ~/.ssh
touch ~/.ssh/config
vim ~/.ssh/config
```

Paste this in the `~/.ssh/config` file
```bash
HostKeyAlgorithms +ssh-rsa
PubkeyAcceptedKeyTypes +ssh-rsa
```

Connect to onos cli and activate application
```bash
cd /opt/onos/bin
/opt/onos/bin/onos -l onos
password: rocks
```

On the ONOS SDN Controller CLI activate the following applications:
```bash
onos@root$ app activate org.onosproject.pipelines.basic
onos@root$ app activate org.onosproject.fwd
onos@root$ app activate org.onosproject.openflow
```

Login GUI
Open browser and type
localhost:8181/onos/ui

username: onos
password: rocks


---
Reference Section
---

#### See more studies from us and cite our work:

1. Mwangi, A., Sundsgaard, K., Vilaplana, J. A. L., Vilerá, K. V., & Yang, G. (2023, June). A system-based framework for optimal sensor placement in smart grids. In 2023 IEEE Belgrade PowerTech (pp. 1-6). IEEE.
```{bibliography}
@inproceedings{mwangi2023system,
  title={A system-based framework for optimal sensor placement in smart grids},
  author={Mwangi, Agrippina and Sundsgaard, Konrad and Vilaplana, Jose Angel Leiva and Viler{\'a}, Kaio Vin{\'\i}cius and Yang, Guangya},
  booktitle={2023 IEEE Belgrade PowerTech},
  pages={1--6},
  year={2023},
  organization={IEEE}
}
```

2. Mwangi, A., Sahay, R., Fumagalli, E., Gryning, M., & Gibescu, M. (2024). Towards a Software-Defined Industrial IoT-Edge Network for Next-Generation Offshore Wind Farms: State of the Art, Resilience, and Self-X Network and Service Management. Energies, 17(12), 2897.
```{bibliography}
@article{mwangi2024towards,
  title={Towards a Software-Defined Industrial IoT-Edge Network for Next-Generation Offshore Wind Farms: State of the Art, Resilience, and Self-X Network and Service Management},
  author={Mwangi, Agrippina and Sahay, Rishikesh and Fumagalli, Elena and Gryning, Mikkel and Gibescu, Madeleine},
  journal={Energies},
  volume={17},
  number={12},
  pages={2897},
  year={2024},
  publisher={MDPI}
}
```

3. Mwangi, A., Fumagalli, E., Gryning, M., & Gibescu, M. (2023, October). Building Resilience for SDN-Enabled IoT Networks in Offshore Renewable Energy Supply. In 2023 IEEE 9th World Forum on Internet of Things (WF-IoT) (pp. 1-2). IEEE.
```{bibliography}
@inproceedings{mwangi2023building,
  title={Building Resilience for SDN-Enabled IoT Networks in Offshore Renewable Energy Supply},
  author={Mwangi, Agrippina and Fumagalli, Elena and Gryning, Mikkel and Gibescu, Madeleine},
  booktitle={2023 IEEE 9th World Forum on Internet of Things (WF-IoT)},
  pages={1--2},
  year={2023},
  organization={IEEE}
}
```
