import json
import paho.mqtt.client as mqtt
import ssl
import serial
import time
import decimal

client = None


org="upgyih"
username = "use-token-auth"
password ="iYNZNyidX_*dBmTRSu"
token="use-token-auth"
secret="iYNZNyidX_*dBmTRSu"
deviceType="Gateway"
deviceID="broker-000"
topic = "iot-2/evt/status/fmt/json"
rootCert = "certs/messaging.pem"
clientID = "d:" + org + ":" + deviceType + ":" + deviceID
client = mqtt.Client(clientID)

print("Connecting to broker ",clientID)

client.username_pw_set(token, secret)
#client.tls_set(ca_certs=rootCert, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_SSLv23)
client.connect(org+".messaging.internetofthings.ibmcloud.com", 8883, 60)
client.loop()

contador=0
print("loop starts")

while True:
    l=''
    msg={}
    s = "Hola soy Marcos"+" "+str(contador)  
    msg = json.JSONEncoder().encode(s)
    contador=contador+1
    print(msg)
    try:
         client.publish(topic, json.dumps(msg))
    except ConnectionException as e:
          print(e)
    print("published")
    time.sleep(0.01)
    pass
client.disconnect()
