#!/usr/bin/env python3
# pip install influxdb-client

from datetime import datetime, timezone
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

URL="http://influxdb:8086"
TOKEN="YPvilNzwob8ejJm394rCnr7qk-I0LujUb9ZbkbEXPOoEEa0ALEyMR1dmwhpqz7aIZnTESGLV7caL06PkvClPIQ=="
ORG="iotorg"
BUCKET="temps"

client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()

print("Enter temperatures. Commands: stats | quit")

while True:
    s = input("> ").strip().lower()
    if s == "quit":
        break

    if s == "stats":
        q = f"""
        from(bucket: "{BUCKET}")
          |> range(start: -1m)
          |> filter(fn: (r) => r._measurement == "temperature")
          |> aggregateWindow(every: 1m, fn: mean)
        """
        tables = query_api.query(q)
        if not tables:
            print("no data (last 1 min)")
        else:
            for rec in tables[0].records:
                print("avg (1m):", rec.get_value())
        continue

    try:
        t = int(s)
        p = (
            Point("temperature")
            .field("value", t)
            .time(datetime.now(tz=timezone.utc))
        )
        write_api.write(bucket=BUCKET, record=p)
        print("written")
    except ValueError:
        print("enter integer, stats, or quit")

client.close()
