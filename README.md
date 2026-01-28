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











