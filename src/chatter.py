#!/usr/bin/env python3
"""
chatter.py

Each instance:
1) Publishes its own IP on MQTT topic (presence).
2) Subscribes to the same topic and learns other devices' IPs.
3) Runs a CoAP server endpoint (/see) to receive messages.
4) Every N seconds, CoAP-POSTs to every known device:
   "I see you from: <my_ip>"

Deps:
  pip install paho-mqtt aiocoap
"""

import argparse
import asyncio
import json
import socket
import time
from typing import Set

import paho.mqtt.client as mqtt
from aiocoap import resource, Context, Message
from aiocoap.numbers.codes import Code


def get_my_ip() -> str:
    """
    Best-effort local IPv4 discovery inside Docker.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't need to be reachable; no packets are actually sent
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()


class SeeResource(resource.Resource):
    async def render_post(self, request):
        payload = request.payload.decode("utf-8", errors="replace")
        peer = request.remote.hostinfo  # e.g. "192.168.2.11:5683"
        print(f"[COAP] from {peer}: {payload.strip()}")
        return Message(code=Code.CHANGED, payload=b"ok\n")


async def coap_server(bind_host: str, bind_port: int):
    root = resource.Site()
    root.add_resource(["see"], SeeResource())
    await Context.create_server_context(root, bind=(bind_host, bind_port))


async def coap_broadcast_loop(
    my_ip: str,
    known_ips: Set[str],
    known_lock: asyncio.Lock,
    interval_s: float,
    coap_port: int,
):
    client = await Context.create_client_context()
    await asyncio.sleep(0.5)  # let transports settle

    while True:
        async with known_lock:
            targets = sorted(ip for ip in known_ips if ip and ip != my_ip)

        for ip in targets:
            uri = f"coap://{ip}:{coap_port}/see"
            payload = f"I see you from: {my_ip}\n".encode("utf-8")
            req = Message(code=Code.POST, uri=uri, payload=payload)
            try:
                resp = await client.request(req).response
                # optional: print success
                # print(f"[COAP] -> {ip}: {resp.code}")
            except Exception as e:
                print(f"[COAP] -> {ip} failed: {e}")

        await asyncio.sleep(interval_s)


def make_mqtt(loop: asyncio.AbstractEventLoop, known_ips: Set[str], known_lock: asyncio.Lock, args, my_ip: str):
    client = mqtt.Client(client_id=args.mqtt_client_id or f"chatter-{socket.gethostname()}-{my_ip}", clean_session=True)

    if args.mqtt_username:
        client.username_pw_set(args.mqtt_username, args.mqtt_password or "")

    def on_connect(c, userdata, flags, rc, properties=None):
        if rc != 0:
            print(f"[MQTT] connect failed rc={rc}")
            return
        print(f"[MQTT] connected to {args.mqtt_host}:{args.mqtt_port}")
        c.subscribe(args.topic, qos=1)

        # publish presence (retain so new joiners immediately learn you)
        presence = {
            "ip": my_ip,
            "host": socket.gethostname(),
            "ts": int(time.time()),
        }
        c.publish(args.topic, json.dumps(presence), qos=1, retain=True)

    def on_message(c, userdata, msg):
        try:
            data = json.loads(msg.payload.decode("utf-8", errors="strict"))
            ip = data.get("ip")
            if not ip or ip == my_ip:
                return

            async def add_ip():
                async with known_lock:
                    if ip not in known_ips:
                        known_ips.add(ip)
                        print(f"[MQTT] learned device ip={ip} (host={data.get('host')})")

            loop.call_soon_threadsafe(lambda: asyncio.create_task(add_ip()))
        except Exception as e:
            print(f"[MQTT] bad message: {e}")

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(args.mqtt_host, args.mqtt_port, keepalive=30)
    client.loop_start()
    return client


async def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mqtt-host", default="mqtt", help="MQTT broker host (compose sets hostname 'mqtt')")
    p.add_argument("--mqtt-port", type=int, default=1883)
    p.add_argument("--mqtt-username", default="")
    p.add_argument("--mqtt-password", default="")
    p.add_argument("--mqtt-client-id", default="")
    p.add_argument("--topic", default="iot/presence")
    p.add_argument("--coap-bind-host", default="0.0.0.0")
    p.add_argument("--coap-port", type=int, default=5683)
    p.add_argument("--interval", type=float, default=5.0)
    args = p.parse_args()

    my_ip = get_my_ip()
    print(f"[SYS] my_ip={my_ip} hostname={socket.gethostname()}")

    known_ips: Set[str] = set()
    known_lock = asyncio.Lock()

    # CoAP server
    await coap_server(args.coap_bind_host, args.coap_port)
    print(f"[COAP] server listening on {args.coap_bind_host}:{args.coap_port} (/see)")

    # MQTT presence + discovery
    loop = asyncio.get_running_loop()
    mqtt_client = make_mqtt(loop, known_ips, known_lock, args, my_ip)

    # Periodic CoAP chatter to everyone we know
    chatter_task = asyncio.create_task(
        coap_broadcast_loop(my_ip, known_ips, known_lock, args.interval, args.coap_port)
    )

    try:
        await chatter_task
    finally:
        try:
            mqtt_client.loop_stop()
            mqtt_client.disconnect()
        except Exception:
            pass


if __name__ == "__main__":
    asyncio.run(main())
