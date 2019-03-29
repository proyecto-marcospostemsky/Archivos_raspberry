# -*- coding: utf-8 -*-
import PyLora
import time
import paho.mqtt.client as mqtt

#Variables locales al archivo
ref="San Luis Norte"
broker="0"*3
PyLora.init()
PyLora.set_frequency(434000000)
client=mqtt.Client(client_id='raspberry',clean_session=False)
client.connect("localhost",1883,60)

print("Para grabar el identificador NIS en el dispositivo siga los siguientes pasos: \n")
print(" 1. Ingrese el NIS que se desee grabar. \n")
print(" 2. Energice el medidor y espere el mensaje de confirmación. \n")

    PyLora.receive()   # put into receive mode
    while not PyLora.packet_available():
        # wait for a package
        time.sleep(0)
    rec = PyLora.receive_packet()
    print(rec)
    #Verifica que rec no esté vacio, para evitar errores de Types
    if rec is not None:
        rec_rec=rec[4:len(rec)]
        print(rec) #Muestro el dato recibido
        print(len(rec))
    if(rec=="RQS NIS"):
        #Abre archivo, y lee cada una de las líneas
        
        file_direcciones=open("mod_address.txt","r+")
        lista_NIS=file_direcciones.readlines()
        #El archivo se encuentra vacio?
        if len(lista_NIS)<1:
            grabar_archivo=broker+"0"*7+"-San Luis Norte"
            file_direcciones.write(grabar_archivo)
            NIS=grabar_archivo[0:10]
        else:
    ##        Toma ultimo NIS del archivo de texto, y se le
    ##        suma uno (al num de modulo) el num de broker se
            ult_linea=str(lista_NIS[len(lista_NIS)-1])
            div_ult_linea=ult_linea.split("-")
            num=int(div_ult_linea[0][3:10])+1
            NIS=broker+"0"*(7-len(str(num)))+str(num)
            file_direcciones.writelines("\n"+NIS+"-"+ref)
            
        #Guardo archivo con NIS  
        file_direcciones.close()

        time.sleep(0.05)
        envio_OK=0
##        print(NIS)
        #PyLora.send_packet(NIS)
    

        
        while(envio_OK==0):
            #Se debe definir un tiempo de espera por si falla el envio
            #para volver a reenviar el NIS
            
            #Envío del NIS al medidor
            PyLora.send_packet("FFFFFFFFFF"+NIS)
                      
            
            #Espero respuesta
            PyLora.receive()   # put into receive mode
            while not PyLora.packet_available():
                # wait for a package
                time.sleep(0)
            rec = PyLora.receive_packet()

            if rec is not None:
                rec_rec=rec[4:len(rec)]
                print(rec)
                print(len(rec))
            
            if "OK-"+NIS==rec:
##                print("Evento terminado correctamente")
                envio_OK=1
            



    #separo la información que envía el dispositivo
    #topic_m=str(msg_div[0])
    #dato=str(msg_div[1])

    #utilizando mqtt lo publico con mosquitto
    #client.publish(topic=topic_m,payload=dato)

