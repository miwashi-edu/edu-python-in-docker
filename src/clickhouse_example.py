import clickhouse_connect

client = clickhouse_connect.get_client(
    host="clickhouse",
    port=8123,
)

result = client.query("SELECT 1").result_rows[0][0]
print("clickhouse:", result)
