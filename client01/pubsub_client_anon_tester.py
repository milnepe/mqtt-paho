#!/usr/bin/env python3

import paho.mqtt.client as mqtt
from threading import Lock

server = "rock-4se"  # FQDN must match CN in server certificate
topic = "test"

#F(100) from https://mersennus.net/fibonacci/f1000.txt
F1000 = 3 * pow(5,3) * 7 * 11 * 41 * 101 * 151 * 251 * 401 * 2161 * 3001 * \
        4001 * 570601 * 9125201 * 112128001 * 1353439001 * 5738108801 * \
        28143378001 * 5465167948001 * 10496059430146001 * 84817574770589638001 \
        * 158414167964045700001 * 9372625568572722938847095612481183137496995522804466421273200001

a, b = 0, 1
testing = True
lock = Lock()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic, qos=0)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # For each message received generate the next fib(n) - if the fib index
    # received in the message does not match the fib(n) then messages have
    # been lost
    with lock:
        global a, b, testing
        i = int(msg.payload)
        print(i, b)
        a, b = b, a+b
        if i == 1000:
            if a == F1000:
                print("All messages received!")
            else:
                print("Messages lost")
            testing = False


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect on default port 1883 (un-encrypted)
client.connect(server, 1883)

while testing:
    client.loop()
else:
    print("Finsihed")
