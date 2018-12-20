import json
import paho.mqtt.client as mqtt
import ssl
import serial
import time
import decimal

client = None


org="upgyih"
username = "use-token-auth"
password ="p_VZoI(0+ZDh4ZyYo8"
token="use-token-auth"
secret="p_VZoI(0+ZDh4ZyYo8"
deviceType="Gateway"
deviceID="broker-001"
topic = "iot-2/evt/status/fmt/json"
rootCert = "certs/messaging.pem"
clientID = "d:" + org + ":" + deviceType + ":" + deviceID
client = mqtt.Client(clientID)

print("Connecting to broker ",clientID)

client.username_pw_set(token, secret)
#client.tls_set(ca_certs=rootCert, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_SSLv23)
client.connect(org+".messaging.internetofthings.ibmcloud.com", 8883, 60)
client.loop()


print("loop starts")

client.subscribe(topic)
print("suscripto a ",topic)