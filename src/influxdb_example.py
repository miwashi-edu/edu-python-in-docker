from influxdb_client import InfluxDBClient

# must be created via UI or API first
URL = "http://influxdb:8086"
TOKEN = "PUT_TOKEN_HERE"
ORG = "PUT_ORG_HERE"

with InfluxDBClient(url=URL, token=TOKEN, org=ORG) as client:
    health = client.health()
    print("influxdb:", health.status)
