---
Implementing self-healing autonomous software-defined OT networks in offshore wind power plants
---

Autonomous software-defined OT networks in offshore Wind Power Plants (WPPs) enforce rigorous Service Level Agreements (SLAs) and Quality of Service (QoS) requirements to ensure reliable transmission of critical time-sensitive and best-effort data traffic. 
Flash events of benign traffic flows causes network congestion resulting in intermittent network service interruptions which are undesirable for the offshore WPP operators. 
This study proposes an externally adapted Deep Q-Networks (DQN) agent within the \textit{``Observe-Orient-Decide-Act"} Closed Control Loop (CCL) self-healing framework. 
This agent detects traffic anomalies, learns optimal paths, and places rules in the SDN controller to reroute traffic, thereby maximizing network throughput and minimizing end-to-end latency.



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





