import paho.mqtt.client as mqtt
import time
import random
import requests
from bs4 import BeautifulSoup
import math



BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
CITY = "comilla"
API_KEY = "7a7adfc0a5635b1627c72eccab71a8e9"



GID =  "8020002201070001"
DID0 = "8020012201080000"
DID2 = "8020012201080002"
DID3 = "8020012201080003"
DID4 = "8020012201080004"

base_pH_0 = 800
base_pH_2 = 540
base_pH_3 = 554
base_pH_4 = 620

base_tds_0 = 12
base_tds_2 = 43
base_tds_3 = 175
base_tds_2 = 120

broker="broker.hivemq.com"
port=1883

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

def ConvertTemp(analog_val, calibration_val = 100000):
    R1 = calibration_val
    c1, c2, c3 = 1.009249522e-03, 2.378405444e-04, 2.019202697e-07
    R2 = R1 * (1023.0 / analog_val - 1.0)
    logR2 = math.log(R2)
    temperature = (1.0 / (c1 + c2 * logR2 + c3 * logR2 * logR2 * logR2))
    temperature = temperature - 273.15
    
    return temperature # degree celcius

def temp_to_analog(temp):
    min_diff = 100
    analog_val = 0
    for val in range(820, 950):
        # print(val)
        # print((abs(ConvertTemp(val) - temp)))
        if min_diff > (abs(ConvertTemp(val) - temp)):
            analog_val = val
            min_diff = (abs(ConvertTemp(val) - temp))
            # print(analog_val, min_diff)
            
    return analog_val

def on_disconnect(client, userdata, rc):
   print("client disconnected ok")
   
def cityTemperature(city):
    URL = BASE_URL + "q=" + city + "&appid=" + API_KEY
    # print(URL)
    response = requests.get(URL)
    # checking the status code of the request
    if response.status_code == 200:

        data = response.json()

        main = data['main']
        temperature = round(main['temp']-273, 2) #n celcius
        humidity = main['humidity']
        pressure = main['pressure']
        return temperature
        
        # weather report
        # report = data['weather']
        # print(f"{city:-^30}")
        # print("Temperature:", temperature)
        # print("Humidity:", humidity)
        # print("Pressure:", pressure)
        # print("Weather Report:",report[0]['description'])
    else:
        # showing the error message
        print("Error in the HTTP request")
        return 22
   

client= mqtt.Client("87trh48yt4h43uy438")                           #create client object
client.on_publish = on_publish                          #assign function to callback
client.on_disconnect = on_disconnect
client.connect(broker,port, keepalive= 1000)                                 #establish connection

topic = "DMA/Fish_Farm/CCDA"
while True:
    client.loop()
    temp = temp_to_analog(cityTemperature(CITY))
    msg_0 = "GID:" + GID + ", DID:" + DID0 + ", Analog: " + str(base_pH_0 + random.randint(-10, 10)) + " " + str(base_tds_0 + random.randint(-5, 5)) + " 0 " + str(temp)
    msg_2 = "GID:" + GID + ", DID:" + DID2 + ", Analog: " + str(base_pH_2 + random.randint(-10, 10)) + " " + str(base_tds_2 + random.randint(-5, 5)) + " 0 " + str(temp)
    msg_3 = "GID:" + GID + ", DID:" + DID3 + ", Analog: " + str(base_pH_2 + random.randint(-10, 10)) + " " + str(base_tds_2 + random.randint(-5, 5)) + " 0 " + str(temp)
    msg_4 = "GID:" + GID + ", DID:" + DID4 + ", Analog: " + str(base_pH_2 + random.randint(-10, 10)) + " " + str(base_tds_2 + random.randint(-5, 5)) + " 0 " + str(temp)
    
    print(msg_0)
    ret = client.publish(topic=topic, qos=2, payload=msg_0)
    print(ret)
    time.sleep(3*60)
    
    print(msg_2)
    ret = client.publish(topic=topic, qos=2, payload=msg_2)
    print(ret)
    time.sleep(1*60)
    
    print(msg_3)
    ret = client.publish(topic=topic, qos=2, payload=msg_3)
    print(ret)
    time.sleep(1*60)
    
    print(msg_4)
    ret = client.publish(topic=topic, qos=2, payload=msg_4)
    print(ret)
    time.sleep(10*60)
    
    