#!/usr/bin/env python3
# mongodb_cli.py
# pip install pymongo

import json
from pymongo import MongoClient

client = MongoClient(
    "mongodb://root:rootpass@mongodb:27017",
    serverSelectionTimeoutMS=5000,
)

db = client.iotdb
col = db.users

# clean start
col.delete_many({})
col.create_index("id", unique=True)

HELP = """Commands:
  add <json>
  list
  read <id>
  update <id> <json>
  delete <id>
  help
  quit
"""

print("Initialized MongoDB users collection.")
print(HELP)

while True:
    line = input("> ").strip()
    if not line:
        continue

    parts = line.split(maxsplit=2)
    cmd = parts[0].lower()

    try:
        if cmd in ("quit", "exit"):
            break

        if cmd == "help":
            print(HELP)
            continue

        if cmd == "add":
            if len(parts) != 2:
                print('usage: add {"id":"1","name":"Mikael"}')
                continue
            doc = json.loads(parts[1])
            col.insert_one(doc)
            print("added")

        elif cmd == "list":
            docs = list(col.find({}, {"_id": 0}))
            if not docs:
                print("(empty)")
            else:
                for d in docs:
                    print(d)

        elif cmd == "read":
            if len(parts) != 2:
                print("usage: read <id>")
                continue
            doc = col.find_one({"id": parts[1]}, {"_id": 0})
            print("not found" if doc is None else doc)

        elif cmd == "update":
            if len(parts) != 3:
                print('usage: update <id> {"name":"Anna"}')
                continue
            updates = json.loads(parts[2])
            res = col.update_one({"id": parts[1]}, {"$set": updates})
            print("updated" if res.matched_count else "not found")

        elif cmd == "delete":
            if len(parts) != 2:
                print("usage: delete <id>")
                continue
            res = col.delete_one({"id": parts[1]})
            print("deleted" if res.deleted_count else "not found")

        else:
            print("unknown command. type 'help'")

    except Exception as e:
        print(f"error: {type(e).__name__}: {e}")
