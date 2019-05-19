# -*- coding: utf-8 -*-
import PyLora
import time
import paho.mqtt.client as mqtt

#Variables locales al archivo
ref="San Luis Norte"
broker="0"*3
nis_rqs="FFFFFFFFFE"
PyLora.init()
PyLora.set_frequency(434000000)
client=mqtt.Client(client_id='raspberry',clean_session=False)
client.connect("localhost",1883,60)




#Variables de control
NIS="1110000000"
nis_correcto=0
reservados={"FFFFFFFFFF","FFFFFFFFFE"}
disp="0123456789ABCDEF"
control_caract=1
envio_OK=0



while(1):
    PyLora.receive()   # put into receive mode
    while not PyLora.packet_available():
        # wait for a package
        time.sleep(0)
    rec = PyLora.receive_packet()
    print(str(rec))
    #Verifica que rec no esté vacio, para evitar errores de Types
    if rec is not None:
        rec_rec=rec[4:len(rec)]
        print(rec_rec) #Muestro el dato recibido
        print(len(rec_rec))


    if(rec_rec=="RQS NIS"):
        time.sleep(0.100)
        envio_OK=0
        print("vamo")
        envio_ok=0
        count=0
        while(envio_OK==0 and count<1):
            #Se debe definir un tiempo de espera por si falla el envio
            #para volver a reenviar el NIS
            
            #Envío del NIS al medidor
            print("Envía NIS")
            NIS=str(int(NIS)+1)
            PyLora.send_packet(NIS)
            
                   
            #Espero respuesta
            PyLora.receive()   # put into receive mode
            while not PyLora.packet_available():
                # wait for a package
                time.sleep(0)
            rec = PyLora.receive_packet()

            if rec is not None:
                rec_rec=rec[4:len(rec)]
                print(rec_rec)
                print(len(rec))
            
            if "OK-"+NIS==rec_rec:
                print("Evento terminado correctamente")
                envio_OK=1
            else:
                count=count+1
                
