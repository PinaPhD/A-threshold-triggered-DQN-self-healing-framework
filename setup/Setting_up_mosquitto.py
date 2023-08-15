#Installation
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install mosquitto
sudo apt-get install mosquitto-clients

#Start the mosquitto broker
sudo service mosquitto start

#Test the broker
mosquitto_pub -h localhost -t topic_name -m "Hello, MQTT!"  #To publish
mosquitto_sub -h localhost -t topic_name   #To subscribe
 
#Check whether mosquitto is running
sudo systemctl status mosquitto.service
sudo systemctl status mosquitto




