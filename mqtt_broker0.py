# -*- coding: utf-8 -*-

import PyLora
import json
import paho.mqtt.client as mqtt
import ssl
import time
import decimal


org="upgyih"
username = "use-token-auth"
password ="iYNZNyidX_*dBmTRSu"
token="use-token-auth"
secret="iYNZNyidX_*dBmTRSu" #secret de broker-000
deviceType="Gateway"
deviceID="broker-000"
topic = "iot-2/evt/status/fmt/json"
rootCert = None#"certs/certifi2.pem"
clientID = "d:" + org + ":" + deviceType + ":" + deviceID

client = mqtt.Client(clientID)

client.username_pw_set('use-token-auth', secret)
client.tls_set(ca_certs=rootCert, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_SSLv23)
client.connect(org+'.messaging.internetofthings.ibmcloud.com', 8883, 60)

client.loop()
PyLora.init()
PyLora.set_frequency(434000000)



contador=0
nis="0000000015"
##while(contador<2):
##    client.publish(topic, json.dumps(publicar))
##    contador=contador+1
##    time.sleep(1)
##
date=10
suma=200.0
flag=1
while(flag):
    PyLora.send_packet("INFO-"+nis)
    PyLora.receive()   # put into receive mode
    while not PyLora.packet_available():
        # wait for a package
        time.sleep(0)
    rec = PyLora.receive_packet()
    
  
    rec_rec=rec[4:len(rec)]
    print(rec_rec)
    
    recdiv=rec_rec.split(";")
    
    publicar={
    "nis":"b"+nis[0:3]+"m"+nis[3:10],
    "energia_kwh":float(recdiv[0]),
    "energia_wh":float(recdiv[1]),
    "tension_rms":float(recdiv[2]),
    "corriente_rms":float(recdiv[3]),
    "factor_potencia":float(recdiv[4]),
    "date": str(recdiv[7])+"-"+str(recdiv[6])+"-"+str(recdiv[5])
    }
    
    print(publicar)
##    msg={}
##    msg = json.JSONEncoder().encode(publicar)
##    contador=contador+1
##    print(msg)
    try:
         client.publish(topic, json.dumps(publicar),qos=1)
    except ConnectionException as e:
          print(e)
    print("published")
    flag=0

#payload = "ojala funque"
#client.publish('iot-2/evt/test/fmt/json', json.dumps(payload))

#client.disconnect()
