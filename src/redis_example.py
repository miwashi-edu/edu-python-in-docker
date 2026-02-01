# redis_kv_cli.py
import redis

r = redis.Redis(host="redis", port=6379, decode_responses=True)

# write loop
print("STORE MODE (type 'quit' to stop)")
while True:
    key = input("key> ")
    if key == "quit":
        break
    value = input("value> ")
    if value == "quit":
        break
    r.set(key, value)
    print("stored")

# read loop
print("\nRETRIEVE MODE (type 'quit' to stop)")
while True:
    key = input("key> ")
    if key == "quit":
        break
    value = r.get(key)
    print(value if value is not None else "not found")
