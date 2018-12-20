import json
import paho.mqtt.client as mqtt
import ssl
import serial
import time
import decimal


org="upgyih"
username = "use-token-auth"
password ="iYNZNyidX_*dBmTRSu"
token="use-token-auth"
#secret="iYNZNyidX_*dBmTRSu" #secret de broker-000
secret="O5AJNbh8gzd3uT2grG"
deviceType="Gateway"
deviceID="broker-001"
topic = "iot-2/evt/status/fmt/json"
rootCert = "certs/messaging.pem"
clientID = "d:" + org + ":" + deviceType + ":" + deviceID

client = mqtt.Client(clientID)

client.username_pw_set('use-token-auth', secret)
client.connect(org+'.messaging.internetofthings.ibmcloud.com', 1883, 60)

client.loop()

contador=0

while(1):
    l=''
    msg={}
    s = deviceID+" "+str(contador)  
    msg = json.JSONEncoder().encode(s)
    contador=contador+1
    print(msg)
    try:
         client.publish(topic, json.dumps(msg))
    except ConnectionException as e:
          print(e)
    print("published")
    time.sleep(4)


#payload = "ojala funque"
#client.publish('iot-2/evt/test/fmt/json', json.dumps(payload))

#client.disconnect()
