#! /usr/bin/python
# -*- coding: utf-8 -*-

import PyLora
import json
import paho.mqtt.client as mqtt
import ssl
import time
import decimal
from datetime import datetime

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
    

org="g4o2on"
username = "use-token-auth"
password ="1793.Marcos"
token="use-token-auth"
secret="1793.Marcos" #secret de broker-000
deviceType="Gateway"
deviceID="Broker-0"
topic = "iot-2/evt/status/fmt/json"
rootCert = None#"/home/pi/Medidor_Energia/certs/certifi2.pem"
clientID = "d:" + org + ":" + deviceType + ":" + deviceID

client = mqtt.Client(clientID)

client.username_pw_set('use-token-auth', secret)
client.tls_set(ca_certs=rootCert, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_SSLv23)
client.connect(org+'.messaging.internetofthings.ibmcloud.com', 8883, 60)

print("Conectado MQTT")

client.loop()
PyLora.init()
PyLora.reset()
PyLora.init()
PyLora.set_frequency(434000000)



contador=0


#Agregar la lectura del archivo "mod_address.log", donde se decidió que la información se recaba cada 15 días,
# es decir este programa debe leer cada nis, pedir su información con un total de tres intentos, y por último,

##
date=10
suma=200.0

while(1):
    #Lectura de todos los nis registrados para el broker
    nis_file=open("/home/pi/Medidor_Energia/mod_address.log","r")
    all_nis=nis_file.readlines()
    nis_file.close()

    cant_nis=len(all_nis)
#Lectura del ultimo nis del cual se recaban los datos
    last_file=open("/home/pi/Medidor_Energia/last_NIS.log","r")
    ult_nis=last_file.readlines()
    last_file.close()
    ult_nis=ult_nis[0].split("=")
    ult_nis=int(ult_nis[1])


    nis=all_nis[ult_nis].split("-")
    nis=nis[0]
    print("NIS medidor actual: "+nis)


    #Dependiendo el valor de "flag", el programa seguirá intentando conseguir la información o no.
    flag=1
    count=0 #Se permitirá solo 3 intentos debido a cualquier error
    while(flag==1 and count<3):
        print("Numero de intento:"+str(count))
        fecha=datetime.now();
        anio=str(fecha.year)
        enviar=nis+"INFO-"+nis+"-"+str(fecha.day)+"-"+str(fecha.month)+"-"+anio[2:4]+"-"
        print("Envia mensaje a nodo: "+enviar)
        PyLora.send_packet(enviar)
        
        
        (rec,flag_rec)=rec_lora(10)

        if flag_rec=="noMsg":
            print(flag_rec)
            count=count+1
            
        if flag_rec=="tmrout":
            print("time out activado")
            count=count+1
        
        if flag_rec=="msg":
            
            try:                       
                rec_rec=rec[4:len(rec)]
                print("Recepcion desde nodo:" + rec_rec)
                
                recdiv=rec_rec.split(";")
                #Comprueba que el formado recibido es el correcto
                #Si no lo fuese, se vuelve a pedir.
                if(len(recdiv)==9 and recdiv[5]==anio and recdiv[6]==str(fecha.month) and recdiv[7]==str(fecha.day)): 
                    publicar={
                    "nis":"b"+nis[0:3]+"m"+nis[3:10],
                    "energia_kwh": float(recdiv[0]), #0
                    "energia_wh":float(recdiv[1]),
                    "tension_rms":float(recdiv[2]),
                    "corriente_rms":float(recdiv[3]),
                    "factor_potencia":float(recdiv[4]),
                    "date": str(recdiv[5])+"-"+"0"*(2-len(str(recdiv[6])))+str(recdiv[6])+"-"+"0"*(2-len(str(recdiv[7])))+str(recdiv[7])
                    }
                    
                    #crea un objeto para luego publicarlo a IBM cloud
                    msg={}
                    msg = json.JSONEncoder().encode(publicar)
                    flag=0
                    
                    try:
                        client.publish(topic, json.dumps(publicar),qos=1)
                        print("Mensaje a publicar en IBM Cloud: ")
                        print(publicar)
                        flag=0
                    except ConnectionException as e:
                        print(e)
                        count=count+1
                

            except:
                print("Mensaje incorrecto")
                count=count+1 

    print("="*80)

    #Control para grabar el último nis registrado por línea de documento, no por por numeración
    if(ult_nis+1!=cant_nis):
        #Se guarda el nis siguiente a leer
        last_file=open("/home/pi/Medidor_Energia/last_NIS.log","w")
        ult_nis=last_file.write("num_send="+str(ult_nis+1))
        last_file.close()
    elif(ult_nis+1==cant_nis): 
        #Se guarda el nis siguiente a leer
        last_file=open("/home/pi/Medidor_Energia/last_NIS.log","w")
        ult_nis=last_file.write("num_send=0")
        last_file.close()
        break

#Una vez terminada la adqusición de información, se desconecta el broker de la plataforma
client.disconnect()

