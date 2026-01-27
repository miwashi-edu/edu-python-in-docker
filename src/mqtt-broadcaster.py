#!/usr/bin/env python3
import sys
import time
import paho.mqtt.client as mqtt

BROKER_HOST = "192.168.2.100"
BROKER_PORT = 1883
TOPIC = "chat/demo"
CLIENT_ID = f"broadcaster-{int(time.time())}"

def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print(f"[mqtt-broadcaster] connected to {BROKER_HOST}:{BROKER_PORT}")
    else:
        print(f"[mqtt-broadcaster] connect failed rc={reason_code}")

def main():
    client = mqtt.Client(client_id=CLIENT_ID, protocol=mqtt.MQTTv311)
    client.on_connect = on_connect

    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_start()

    print(f"[mqtt-broadcaster] publishing to topic '{TOPIC}'")
    print("[mqtt-broadcaster] type messages; 'quit' to exit; Ctrl-C to exit")

    try:
        while True:
            try:
                line = input("> ")
            except EOFError:
                break

            if line.strip().lower() == "quit":
                break

            payload = line
            info = client.publish(TOPIC, payload=payload, qos=0, retain=False)
            info.wait_for_publish()
    except KeyboardInterrupt:
        pass
    finally:
        print("\n[mqtt-broadcaster] bye")
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
