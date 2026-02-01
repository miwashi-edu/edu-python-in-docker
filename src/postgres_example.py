import psycopg

with psycopg.connect(
    host="postgres",
    port=5432,
    dbname="iotdb",
    user="iot",
    password="iotpass",
) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT 1;")
        print("postgres:", cur.fetchone()[0])
