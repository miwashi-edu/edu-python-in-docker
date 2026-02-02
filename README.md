# edu-python-in-docker


## Instructions

### Prepare

```bash
cd ~
cd ws
git clone https://github.com/miwashi-edu/edu-python-in-docker.git
cd edu-python-in-docker
docker compose down # If up from before.
docker compose up -d
docker ps
```
### Redis

> Redis is an in-memory key-value database optimized for extremely fast 
> reads/writes, often used for caching, queues, and ephemeral state.

```bash
ssh -p 2222 dev@localhost
cd src
pip install redis
python redis_example.py
```

### PostgreSQL

> **PostgreSQL** is a **relational (row-based) database** focused on **transactions, 
> consistency, and complex queries** using SQL.


```bash
ssh -p 2222 dev@localhost
cd src
pip install psycopg[binary]
python postgres_example.py
```

### Graph Database

> A graph database stores data as nodes and relationships, 
> optimized for traversing connections rather than scanning tables.

#### Example (graph search, Neo4j / Cypher):
```neo4j
MATCH (a:User)-[:KNOWS]->(b:User)-[:KNOWS]->(c:User)
WHERE a.name = "Mikael"
RETURN c.name;
```
→ “Find friends-of-friends of Mikael.”

```bash
ssh -p 2222 dev@localhost
cd src
pip install neo4j
python neo4j_example.py
```

### Document Database

> MongoDB is a document-oriented database that stores schema-flexible 
> JSON-like documents, optimized for easy data modeling and horizontal scaling.

```bash
ssh -p 2222 dev@localhost
cd src
pip install pymongo
python mongodb_example.py
```

### Column Database

> ClickHouse is a columnar analytics database optimized for fast 
> aggregations and scans over massive datasets, not transactional CRUD.

```bash
ssh -p 2222 dev@localhost
cd src
pip install clickhouse-connect
python clickhouse_example.py
```

### Time Series Database

> **InfluxDB** is a **time-series database** where **users and tokens are 
> created via the web UI (`http://localhost:8086`)**, and **time-series data can be 
> explored and visualized there** (queries, charts, dashboards).
> Script cant be used before visiting: `http://localhost:8086`


```bash
ssh -p 2222 dev@localhost
cd src
pip install influxdb-client
python influxdb_example.py
```
Surf to http://localhost:8086 and add a user

### Use shebang

```bash
# Works if you have a shebang (#!/usr/bin/env python3)
chmod + x redis_example.py
./redis_example.py # As working directory isn't in path we need to tell here with ./
```







