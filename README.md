---
A secure self-healing module for software-defined industrial OT networks in extreme environments 
---


Self-healing involves the communication network's ability to detect and remediate issues autonomously, reducing the reliance on manual interventions. This is achieved using ML algorithms and automation to predict, detect, and respond to operational issues. Self-healing can either be data-based or event-based. We anticipate that adopting a self-healing framework in the software-defined industrial OT networks will improve SLAs and uptime, allowing Network Engineers to focus on developing solutions that drive business value and facilitate digital transformation without spending a significant portion of their time on manual tasks. Implementing a self-healing framework needs a mind shift from reactive to proactive approaches.


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





