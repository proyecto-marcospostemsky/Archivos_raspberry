# -*- coding: utf-8 -*-
import PyLora
import time

PyLora.init()
PyLora.set_frequency(434000000)

while True:
    PyLora.receive()   # put into receive mode
    while not PyLora.packet_available():
        # wait for a package
        time.sleep(0)
    rec = PyLora.receive_packet()
    print(str(rec))
    print(rec)
    print(len(rec))
    i=0
    rec_str=""
    for valor in rec:
        valor=chr(valor)
        print(valor)
        rec_str=rec_str+valor
        print(rec_str)
        
    print(rec_str)
    
