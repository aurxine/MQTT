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

sub_message = ""

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

def on_disconnect(client, userdata, rc):
   print("client disconnected ok")

def on_message(client, userdata, message):
    global sub_message
    
    # print("message received " ,str(message.payload.decode("utf-8")))
    # print("message topic=",message.topic)
    # print("message qos=",message.qos)
    # print("message retain flag=",message.retain)
    sub_message = str(message.payload.decode("utf-8"))

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


def cityTemperature(city):
    URL = BASE_URL + "q=" + city + "&appid=" + API_KEY
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

topic = "DMA/Fish_Farm/Padma_Shrimps"

client= mqtt.Client("8htn30u94tin40")                           #create client object
client.on_publish = on_publish                          #assign function to callback
client.on_disconnect = on_disconnect
client.connect(broker,port, keepalive= 1000)                                 #establish connection
client.on_message =  on_message
client.subscribe(topic=topic)
while True:
    # temp = temp_to_analog(cityTemperature(CITY))
    # msg_0 = "GID:" + GID + ", DID:" + DID0 + ", Analog: " + str(base_pH_0 + random.randint(-5, 5)) + " " + str(base_tds_0 + random.randint(-5, 5)) + " 0 " + str(temp)
    # msg_1 = "GID:" + GID + ", DID:" + DID1 + ", Analog: " + str(base_pH_1 + random.randint(-5, 5)) + " " + str(base_tds_1 + random.randint(-5, 5)) + " 0 " + str(temp)
    # print(msg_0)
    # ret = client.publish(topic=topic, qos=2, payload=msg_0)
    # print(ret)
    # time.sleep(3*60)
    # print(msg_1)
    # ret = client.publish(topic=topic, qos=2, payload=msg_1)
    # print(ret)
    # time.sleep(12*60)
    if len(sub_message) > 0:
        print(sub_message)
        if "GID:8020002203220000, DID:8020012202170002" in sub_message:
            list_sub_message = list(sub_message)
            list_sub_message[42] = '3'
            sub_message = ''.join(list_sub_message)
            print("to be published: ", sub_message)
            client.publish(topic=topic, payload=sub_message)
        sub_message = ""
    client.loop()
    