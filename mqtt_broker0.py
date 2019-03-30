# -*- coding: utf-8 -*-

import PyLora
import json
import paho.mqtt.client as mqtt
import ssl
import time
import decimal

def rec_lora(timeout=3):
    flag="noMsg"
    time_out=0
    PyLora.receive()   # put into receive mode
    msg=None    
    while not PyLora.packet_available():
        # wait for a package
        flag="msg"
        time.sleep(0.25)
        time_out+=1
        if time_out>=int(timeout*4):
            flag="tmrout"
            break
    if(flag=="msg"):
        msg = PyLora.receive_packet()
    return(msg,flag)
    

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

print("Conectado MQTT")

client.loop()
PyLora.init()
PyLora.set_frequency(434000000)



contador=0
nis="0000000243"

#Agregar la lectura del archivo "mod_address.txt", donde se decidió que la información se recaba cada 15 días,
# es decir este programa debe leer cada nis, pedir su información con un total de tres intentos, y por último,
#esperar 15 días para volver a realizar esta tarea.






##
date=10
suma=200.0
flag=1
while(flag):
    enviar=nis+"INFO-"+nis
    print(enviar)
    PyLora.send_packet(enviar)

    (rec,flag_rec)=rec_lora(10)

    if flag_rec=="noMsg":
        print(flag_rec)
        
    if flag_rec=="tmrout":
        print("time out activado")
    
    if flag_rec=="msg":
        
        try:                       
            rec_rec=rec[4:len(rec)]
            print(rec)
            
            recdiv=rec.split(";")
            
            publicar={
            "nis":"b"+nis[0:3]+"m"+nis[3:10],
            "energia_kwh":float(recdiv[0]), #0
            "energia_wh":float(recdiv[1]),
            "tension_rms":float(recdiv[2]),
            "corriente_rms":float(recdiv[3]),
            "factor_potencia":float(recdiv[4]),
            "date": str(recdiv[7])+"-"+"0"*(2-len(str(recdiv[6])))+str(recdiv[6])+"-"+"0"*(2-len(str(recdiv[5])))+str(recdiv[5])
            }
            
            print(publicar)
        except IndexError or ValueError:
            print("mensaje incorrecto")
    ##    msg={}
    ##    msg = json.JSONEncoder().encode(publicar)
    ##    contador=contador+1
    ##    print(msg)
    ##    try:
    ##         client.publish(topic, json.dumps(publicar),qos=1)
    ##    except ConnectionException as e:
    ##          print(e)
    ##    print("published")
    flag=0

    #payload = "ojala funque"
    #client.publish('iot-2/evt/test/fmt/json', json.dumps(payload))

    #client.disconnect()
