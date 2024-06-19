# Secure self-healing software-defined industrial OT networks in extreme environments 
---
Installation Project Guide
---



##### Step 1: Infrastructure Layer Design
- Create a virtual machine on the Microsoft Azure Resource Group and assign it a virtual network and security group
- In the VM, install Ubuntu 22.04 x64 Gen2 Operating System and run the following commands:

  ```bash
 sudo apt-get -y update && sudo apt-get -y upgrade
 sudo apt-get -y install wireshark wget curl vim nano 
 git clone https://github.com/mininet/mininet 
 mininet/util/install.sh -w
  ```
  
