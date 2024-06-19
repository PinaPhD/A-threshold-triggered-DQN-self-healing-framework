# Secure self-healing software-defined industrial OT networks in extreme environments 
---
Installation Project Guide
---



##### Step 1: Infrastructure Layer Design
- Create a Virtual Machine (VM) on the Microsoft Azure Resource Group and assign it a virtual network and security group
- Connect to the VM via Bastion or a Remote Desktop (RDP) granted you have a public IP address or are running a VPN agent
- In the VM, install Ubuntu 22.04 x64 Gen2 Operating System and run the following commands:

``` bash
sudo apt-get -y update && sudo apt-get -y upgrade
sudo apt-get -y install wireshark wget curl vim nano git
git clone https://github.com/mininet/mininet.git
cd mininet/util
git checkout 2.3.1b4
./install.sh -a
```
  
