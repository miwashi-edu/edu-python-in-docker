#!/usr/bin/env python3
import time
import paho.mqtt.client as mqtt

BROKER_HOST = "192.168.2.100"
BROKER_PORT = 1883
TOPIC = "chat/demo"
CLIENT_ID = f"listener-{int(time.time())}"

def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print(f"[mqtt-listener] connected to {BROKER_HOST}:{BROKER_PORT}")
        client.subscribe(TOPIC, qos=0)
        print(f"[mqtt-listener] subscribed to '{TOPIC}' (Ctrl-C to exit)")
    else:
        print(f"[mqtt-listener] connect failed rc={reason_code}")

def on_message(client, userdata, msg):
    text = msg.payload.decode("utf-8", errors="replace")
    print(f"[mqtt-listener] {msg.topic}: {text}")

def main():
    client = mqtt.Client(client_id=CLIENT_ID, protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n[mqtt-listener] bye")
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()
