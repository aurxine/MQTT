import paho.mqtt.client as mqtt
import time
import random
import requests
from bs4 import BeautifulSoup
import math



BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
CITY = "Gopalganj"
API_KEY = "7a7adfc0a5635b1627c72eccab71a8e9"




GID =  "8020002201100000"
DID0 = "8021012201100000"
DID1 = "8021012201100001"

base_pH_0 = 550
base_pH_1 = 550

base_tds_0 = 91
base_tds_1 = 100

broker="broker.hivemq.com"
port=1883

# def on_publish(client,userdata,result):             #create function for callback
#     print("data published \n")
#     pass

def on_disconnect(client, userdata, rc):
   print("client disconnected ok")

client= mqtt.Client("8htn3094u30u94tin40")                           #create client object
# client.on_publish = on_publish                          #assign function to callback
client.on_disconnect = on_disconnect
client.connect(broker,port, keepalive= 1000)                                 #establish connection

topic = "DMA/Fish_Farm/Padma_Shrimps/8020022201310000"
while True:
    msg = "ON"
    ret = client.publish(topic=topic, payload= msg,qos=2)
    print(ret)
    time.sleep(5)
    msg = "OFF"
    ret = client.publish(topic=topic, payload= msg,qos=2)
    print(ret)
    time.sleep(5)
    client.loop()
    