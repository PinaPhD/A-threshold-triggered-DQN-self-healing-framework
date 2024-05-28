---
DDPG Resilience Model 
---
A secure self-healing module for software-defined industrial OT networks in extreme environments

---
Pre-requisites
---

Installation:
- sudo apt-get update && sudo apt-get upgrade
- sudo apt-get install mosquitto
- sudo apt-get install mosquitto-clients

---
IoT-to-ECP Node 
---

Start the mosquitto broker:
- sudo service mosquitto start

Test the broker:
 - mosquitto_pub -h localhost -t topic_name -m "Hello, MQTT!"  #To publish
 - mosquitto_sub -h localhost -t topic_name   #To subscribe
 
Check whether mosquitto is running:
 - sudo systemctl status mosquitto.service
 - sudo systemctl status mosquitto





