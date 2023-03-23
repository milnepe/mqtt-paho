#!/usr/bin/env python3

''' Anonymous MQTT subscriber client for testing message receipts
    Use with any of the publishing clients.

    The publishing client sends a sequence of messages with a value that
    increments from 1 to 1000 - the index to the Fibonacci series.

    Each time this client receives a message it calculates the next number in
    the Fibonacci series. When the value received equals 1000 messages, the
    Fibonacci sequence should be equal to F(1000) if all the messages have been
    received and in the original sequence.

    The ROCK 4SE broker is able to process bursts of 1000 messages in ~50ms
    equivalent to 20k messages/second without errors at QoS-0
    '''

import paho.mqtt.client as mqtt
from threading import Lock

broker = "rock-4se"
topic = "test"

# F(100) from https://mersennus.net/fibonacci/f1000.txt
F1000 = 3 * pow(5,3) * 7 * 11 * 41 * 101 * 151 * 251 * 401 * 2161 * 3001 * \
        4001 * 570601 * 9125201 * 112128001 * 1353439001 * 5738108801 * \
        28143378001 * 5465167948001 * 10496059430146001 * 84817574770589638001 \
        * 158414167964045700001 * 9372625568572722938847095612481183137496995522804466421273200001

a, b = 0, 1
testing = True
lock = Lock()


def fib_test(idx):
    # For each message received generate the next fib(n) - if the fib index
    # received in the message does not match the fib(n) then messages have
    # been lost
    global a, b, testing
    print(idx, b)
    a, b = b, a+b
    # Test the one thousanth message when 'a' should match F1000
    if idx == 1000:
        if a == F1000:
            print("All messages received!")
        else:
            print("Messages lost")
        testing = False


# The callback for when the client receives a CONNACK response from the broker.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic, qos=0)


# The callback for when a PUBLISH message is received from the broker.
def on_message(client, userdata, msg):
    i = int(msg.payload)
    with lock:
        fib_test(i)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect on default port 1883 (un-encrypted)
client.connect(broker, 1883)

while testing:
    client.loop()
else:
    print("Finsihed")
