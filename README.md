# edu-python-in-docker


## Instructions

### Prepare
```
cd ~
cd ws
git clone https://github.com/miwashi-edu/edu-python-in-docker.git
cd edu-python-in-docker
git checkout level-1
docker compose up -d
docker ps
```

### Check IP adreesses

```bash
docker inspect iotnet # read the json produced
```


### Login to Server

```bash
ssh -p 2222 dev@localhost   # password dev, respond yes if prompted about signature
cd ~/src
python tcp-server.py
# or
python udp-server.py
```

### Login to client

```bash
ssh -p 2223 dev@localhost   # password dev, respond yes if prompted about signature
python tcp-client.py
# or
python udp-client.py
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




