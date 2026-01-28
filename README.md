# edu-python-in-docker


## Instructions

### Prepare
```
cd ~
cd ws
git clone https://github.com/miwashi-edu/edu-python-in-docker.git
cd edu-python-in-docker
docker compose up -d
docker ps
```

### Terminal one

```
ssh -p 2222 dev@localhost
cd src
pip install aiocoap paho-mqtt
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
python chatter.py
```

### Terminal two

```
ssh -p 2223 dev@localhost
cd src
pip install aiocoap paho-mqtt
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
python chatter.py
```

### Terminal three

```
ssh -p 2224 dev@localhost
cd src
pip install aiocoap paho-mqtt
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
python chatter.py
```

### Refactor for understanding

#### Target file structure

```
chatter/
  __init__.py
  __main__.py
  cli.py
  net.py
  mqtt_presence.py
  coap_node.py
  loop.py
```

#### Suggested SoC

1. __main__.py – entrypoint (python -m chatter)
2. cli.py – argparse config (all flags)
3. net.py – get_my_ip() + small helpers
4. mqtt_presence.py – connect/subscribe/publish presence + update registry
5. coap_node.py – CoAP server resource + client context creation
6. loop.py – periodic “see you” loop + shared registry/lock

#### Suggested run command

```bash
python -m chatter --mqtt-host mqtt --topic iot/presence --interval 5
```

#### Suggested poetry toml

```toml
[project]
name = "chatter"
version = "0.1.0"
dependencies = ["aiocoap", "paho-mqtt"]

[project.scripts]
chatter = "chatter.__main__:main"
```

#### Installation with pip and toml

```bash
pip install -e .
chatter --mqtt-host mqtt --interval 5
```

#### Suggested \_\_main\_\_.py

```python
# chatter/__main__.py

import asyncio
import socket

from .cli import parse_args
from .net import get_my_ip
from .mqtt_presence import start_mqtt
from .coap_node import start_coap_server
from .loop import chatter_loop


def main():
    args = parse_args()

    my_ip = get_my_ip()
    hostname = socket.gethostname()
    print(f"[SYS] hostname={hostname} ip={my_ip}")

    known_ips = set()
    known_lock = asyncio.Lock()

    async def runner():
        # CoAP server
        await start_coap_server(
            bind_host=args.coap_bind_host,
            bind_port=args.coap_port,
        )
        print(f"[COAP] listening on {args.coap_bind_host}:{args.coap_port}")

        # MQTT discovery
        loop = asyncio.get_running_loop()
        mqtt_client = start_mqtt(
            loop=loop,
            args=args,
            my_ip=my_ip,
            known_ips=known_ips,
            known_lock=known_lock,
        )

        # Periodic chatter
        chatter_task = asyncio.create_task(
            chatter_loop(
                my_ip=my_ip,
                known_ips=known_ips,
                known_lock=known_lock,
                interval=args.interval,
                coap_port=args.coap_port,
            )
        )

        try:
            await chatter_task
        finally:
            mqtt_client.loop_stop()
            mqtt_client.disconnect()

    asyncio.run(runner())


if __name__ == "__main__":
    main()
```











