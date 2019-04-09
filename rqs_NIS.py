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


#Comienza por pedir el ingreso del NIS al usuario, verificando la disponibilidad del mismo.

print("Para grabar el identificador NIS en el dispositivo siga los siguientes pasos: \n")
print("   1. Ingrese el NIS que se desee grabar entre comillas (\"NIS\"). \n")
print("   2. Energice el medidor y espere el mensaje de confirmación. \n")

#Variables de control
NIS="F"
nis_correcto=0
reservados={"FFFFFFFFFF","FFFFFFFFFE"}
disp="0123456789ABCDEF"
control_caract=1
envio_OK=0

#Loop para corroborar que el NIS que ingresa el usuario es válido.
while(len(NIS)!=10 or nis_correcto==0):
    nis_correcto=1
    try:
        NIS= str(input("Ingrese el nuevo valor de NIS: "))
    except:
        print("\nEl NIS ingresado contiene caracteres prohibidos")        
    if(len(NIS)!=10):
        print("\nEl identificador NIS no tiene el largo correcto\n")
        nis_correcto=0
    else:

        
        for carac in NIS:           #Verifica que los caracteres sean correctos
            if disp.find(carac)==-1:
                print("\nSolo se permiten los caracter (0 al 9) y (A a F).\n")
                nis_correcto=0
                break

        #Se abre el archivo donde se encuentran los NIS, para verificar que no esté en uso.
        nis_file=open("mod_address.log","r") #abro archivo con los nis
        lines=nis_file.read() #Lee todas las lineas del archivo
        nis_file.close()
        if nis_correcto==1 and lines.find(NIS)!= -1:
            print("\nEl NIS ingresado ya se encuentra en uso, por favor de verificarlo.\n")
            nis_correcto=0

        #Verificación de que el NIS no sea uno de los reservados
        elif NIS in reservados and nis_correcto==1:
            print("\nEl NIS ingresado se encuentra reservado.\n")
            nis_correcto=0

        #Si hasta este punto de control el NIS ha sido correcto, se pide una refencia 
        #con la cual guardar la información, luego de grabar en el medidor.
        elif nis_correcto==1:
            ref_ok=0
            while(ref_ok==0):
                try:
                    referencia=str(input("\nNIS disponible. Escriba una referencia, entre comillas (\"ref\"): "))
                    ref_ok=1
                except:
                    print("\nReferencia contiene caracteres prohibidos. Recuerde las comillas.")

print("\n Energice el medidor y espere el mensaje de confirmación.")



#Se comienza por grabar el NIS del nuevo dispositivo.
print("recibiendo")
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
        print(rec) #Muestro el dato recibido
        print(len(rec))


if(rec=="RQS NIS"):
    time.sleep(0.05)
    envio_OK=0

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
            print("Evento terminado correctamente")
            envio_OK=1


#Si se confirma que el medidor recibio el valor configurado, se guarda el NIS en el archivo "mod_address.log"           
if(envio_OK==1):
    nis_file=open("mod_address.log","r+")
    lines=nis_file.read() #Lee todas las lineas del archivo
    nis_file.writelines("\n"+NIS+"-"+referencia) #Guardo nuevo NIS en archivo
    nis_file.close()



