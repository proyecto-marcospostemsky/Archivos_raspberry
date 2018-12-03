# -*- coding: utf-8 -*-
import PyLora
import time
import paho.mqtt.client as mqtt

#Variables locales al archivo
ref="San Luis Norte"
broker="000"

PyLora.init()
PyLora.set_frequency(434000000)
client=mqtt.Client(client_id='raspberry',clean_session=False)
client.connect("localhost",1883,60)
while True:
    
    PyLora.receive()   # put into receive mode
    while not PyLora.packet_available():
        # wait for a package
        time.sleep(0)
    rec = PyLora.receive_packet()
    rec_rec=rec[4:len(rec)]
    print(rec_rec)
##    rec_rec=input()
    if(rec_rec=="RQS NIS"):
        #Abre archivo, y lee cada una de las líneas
        
        file_direcciones=open("mod_address.txt","r+")
        lista_NIS=file_direcciones.readlines()
        #El archivo se encuentra vacio?
        if len(lista_NIS)<2:
            grabar_archivo=broker+"0"*7+"-San Luis Norte"
            file_direcciones.write(grabar_archivo)
            NIS=grabar_archivo[0:10]
        else:
    ##        Toma ultimo NIS del archivo de texto, y se le
    ##        suma uno (al num de modulo) el num de broker se mantiene
            ult_linea=str(lista_NIS[len(lista_NIS)-1])
            div_ult_linea=ult_linea.split("-")
            num=int(div_ult_linea[0][3:10])+1
            NIS=broker+"0"*(7-len(str(num)))+str(num)
            file_direcciones.writelines("\n"+NIS+"-"+ref)
            
        #Guardo archivo con NIS  
        file_direcciones.close()
        
        envio_OK=0
        while(envio_OK==0):
            #Se debe definir un tiempo de espera por si falla el envio
            #para volver a reenviar el NIS
            
            #Envío del NIS al medidor
            PyLora.send_packet("0123456789")
                      
            
            #Espero respuesta
            PyLora.receive()   # put into receive mode
            while not PyLora.packet_available():
                # wait for a package
                time.sleep(0)
            rec = PyLora.receive_packet()
            rec_rec=rec[4:len(rec)]
            
            envio_OK=1
            
            if "OK-"+NIS==rec_rec:
                print("Evento terminado correctamente")
                envio_OK=1
            else:
                print("Envío incorrecto")



    #separo la información que envía el dispositivo
    #topic_m=str(msg_div[0])
    #dato=str(msg_div[1])

    #utilizando mqtt lo publico con mosquitto
    #client.publish(topic=topic_m,payload=dato)

