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





