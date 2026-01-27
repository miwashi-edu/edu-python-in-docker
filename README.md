# edu-python-in-docker


## Instructions

### Prepare
```
cd ~
cd ws
git clone https://github.com/miwashi-edu/edu-python-in-docker.git
cd edu-python-in-docker
git checkout level-2
docker compose up -d
docker ps
```

### Check IP adreesses

```bash
docker inspect iotnet # read the json produced
```

### Login to client

#### Client 1

```bash
ssh -p 2223 dev@localhost   # password dev
cd ~/src
pip install paho-mqtt
python mqtt-listener.py
```

```bash
ssh -p 2224 dev@localhost   # password dev
cd ~/src
pip install paho-mqtt
python mqtt-listener.py
```

### Login to Broadcaster

```bash
ssh -p 2222 dev@localhost   # password dev
cd ~/src
pip install paho-mqtt
python mqtt-broadcaster.py
```

### Rebuilding machines

```bash
docker compose up -d --build
```

or

```bash
docker compose build --no-cache
docker compose up -d
```




