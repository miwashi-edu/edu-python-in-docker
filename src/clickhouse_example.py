#!/usr/bin/env python3
# clickhouse_temps.py
# pip install clickhouse-connect

import clickhouse_connect

ch = clickhouse_connect.get_client(host="clickhouse", port=8123)

# fresh start
ch.command("CREATE DATABASE IF NOT EXISTS iot")
ch.command("DROP TABLE IF EXISTS iot.temps")
ch.command("""
CREATE TABLE iot.temps (
  ts DateTime DEFAULT now(),
  temp Int32
)
ENGINE = MergeTree
ORDER BY ts
""")

print("Enter temperatures as integers. Type 'quit' to stop.\n")

rows = []
while True:
    s = input("temp> ").strip()
    if s.lower() == "quit":
        break
    try:
        t = int(s)
        rows.append((t,))   # one-column row
    except ValueError:
        print("please enter an integer or 'quit'")

if rows:
    ch.insert("iot.temps", rows, column_names=["temp"])
    print(f"\nInserted {len(rows)} rows.")
else:
    print("\nNo rows inserted.")

stats = ch.query("""
SELECT
  count() AS n,
  avg(temp) AS avg,
  min(temp) AS min,
  max(temp) AS max,
  varPop(temp) AS var_pop,
  stddevPop(temp) AS std_pop
FROM iot.temps
""").result_rows[0]

n, avg_, min_, max_, var_pop, std_pop = stats

if n == 0:
    print("No data to summarize.")
else:
    print("\nStats (population):")
    print(f"n     : {n}")
    print(f"avg   : {avg_}")
    print(f"min   : {min_}")
    print(f"max   : {max_}")
    print(f"var   : {var_pop}")
    print(f"stdev : {std_pop}")
