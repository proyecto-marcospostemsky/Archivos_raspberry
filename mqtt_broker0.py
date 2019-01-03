import json
import paho.mqtt.client as mqtt
import ssl
import serial
import time
import decimal

nis="0000000003"
rec="430/350/245/40/52/"

recdiv=rec.split("/")




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

contador=0
##while(contador<2):
##    client.publish(topic, json.dumps(publicar))
##    contador=contador+1
##    time.sleep(1)
##
date=10
suma=200.0
while(contador<15):
    publicar={
    "nis":"b"+nis[0:3]+"m"+nis[3:10],
    "energia_kwh":float(recdiv[0])+suma,
    "energia_wh":float(recdiv[1]),
    "tension_rms":float(recdiv[2]),
    "corriente_rms":float(recdiv[3]),
    "factor_potencia":float(recdiv[4]),
    "date": "2018-10-"+str(date)
    }
    date=date+1
    suma=suma+50
    l=''
    msg={}
    s = deviceID+" "+str(contador)  
    msg = json.JSONEncoder().encode(publicar)
    contador=contador+1
    print(msg)
    try:
         client.publish(topic, json.dumps(publicar),qos=1)
    except ConnectionException as e:
          print(e)
    print("published")
    time.sleep(2)


#payload = "ojala funque"
#client.publish('iot-2/evt/test/fmt/json', json.dumps(payload))

#client.disconnect()
