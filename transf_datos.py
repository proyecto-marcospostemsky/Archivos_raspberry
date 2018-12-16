# -*- coding: utf-8 -*-
import PyLora
import time
import paho.mqtt.client as mqtt

while True:
    PyLora.send_packet("RQS info|"+NIS);
    
