#!/usr/bin/env python3

''' MQTT publishing client for testing TLS encrypted message receipts with
    client certificates. The certficate CN is used to identify the client.

    Use with the fib tester client.

    This client sends a sequence of messages with a value that increments from
    1 to 1000 - the index to the Fibonacci series.

    A broker root CA certificate is required as well as valid certificate and
    key for the client.

    The ROCK 4SE broker is able to process bursts of 1000 messages in ~110ms
    equivalent to 9k messages/second without errors at QoS-0 with TLS and
    client certficates.
    '''

import paho.mqtt.client as mqtt

broker = "rock-4se"  # FQDN must match CN in broker certificate
topic = "test"


# The callback for when the client receives a CONNACK response from the broker.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe(topic, qos=0)


# The callback for when a PUBLISH message is received from the broker.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload.decode("utf-8")))


client = mqtt.Client()
client.on_connect = on_connect
# client.on_message = on_message

# Connect using TLS and client certficates on port 8884 (encrypted)
client.tls_set(ca_certs="/etc/ssl/certs/Highly_Trusted_CA.crt",
               certfile="certs/client01.crt", keyfile="certs/client01.key")
client.connect(broker, 8884)

client.loop_start()

# Publish a burst of messages very quickly
for i in range(1, 1001):
    client.publish(topic, i, qos=0)

client.loop_stop()

print("Finsihed")
