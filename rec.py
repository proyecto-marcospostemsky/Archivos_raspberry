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
    print(rec)
