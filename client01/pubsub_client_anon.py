#!/usr/bin/env python3

import paho.mqtt.client as mqtt

server = "rock-4se"  # FQDN must match CN in server certificate
topic = "test"


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe(topic, qos=0)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload.decode("utf-8")))


client = mqtt.Client()
client.on_connect = on_connect
# client.on_message = on_message

# Connect on default port 1883 (un-encrypted)
client.connect(server)

client.loop_start()

for i in range(1, 1001):
    client.publish(topic, i, qos=0)

client.loop_stop()

print("Finsihed")