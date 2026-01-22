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

### Login to Server

```bash
ssh -p 2222 dev@localhost   # server (iot-server), password dev
```

### Login to client

```bash
ssh -p 2223 dev@localhost   # client (iot-client), password dev
```

## Rebuilding machines

```bash
docker compose up -d --build
```

or

```bash
docker compose build --no-cache
docker compose up -d
```


## Generate new signatures if needed

> When you see  
> @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  
> @    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @  
> @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  

```bash
ssh-keygen -R "[localhost]:2222" # Add new key if needed 
ssh-keygen -R "[localhost]:2223" # Add new key if needed
```






