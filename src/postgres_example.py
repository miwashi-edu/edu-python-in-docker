#!/usr/bin/env python3
# postgres_cli.py
# pip install psycopg[binary]

import psycopg

DB = dict(host="postgres", port=5432, dbname="iotdb", user="iot", password="iotpass")

DDL = """
DROP TABLE IF EXISTS "User";
CREATE TABLE "User" (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL
);
"""

HELP = """Commands:
  list
  create <name>
  read <id>
  update <id> <name>
  delete <id>
  help
  quit
"""

def init_db(conn):
    with conn.cursor() as cur:
        cur.execute(DDL)
    conn.commit()

def main():
    with psycopg.connect(**DB) as conn:
        init_db(conn)
        print("Initialized table User.")
        print(HELP)

        while True:
            line = input("> ").strip()
            if not line:
                continue

            parts = line.split()
            cmd = parts[0].lower()

            try:
                if cmd in ("quit", "exit"):
                    break

                if cmd == "help":
                    print(HELP)
                    continue

                with conn.cursor() as cur:
                    if cmd == "list":
                        cur.execute('SELECT id, name FROM "User" ORDER BY id;')
                        rows = cur.fetchall()
                        if not rows:
                            print("(empty)")
                        else:
                            for rid, name in rows:
                                print(f"{rid}: {name}")

                    elif cmd == "create":
                        if len(parts) < 2:
                            print("usage: create <name>")
                            continue
                        name = " ".join(parts[1:])
                        cur.execute('INSERT INTO "User"(name) VALUES (%s) RETURNING id;', (name,))
                        new_id = cur.fetchone()[0]
                        conn.commit()
                        print(f"created id={new_id}")

                    elif cmd == "read":
                        if len(parts) != 2 or not parts[1].isdigit():
                            print("usage: read <id>")
                            continue
                        uid = int(parts[1])
                        cur.execute('SELECT id, name FROM "User" WHERE id=%s;', (uid,))
                        row = cur.fetchone()
                        print("not found" if row is None else f"{row[0]}: {row[1]}")

                    elif cmd == "update":
                        if len(parts) < 3 or not parts[1].isdigit():
                            print("usage: update <id> <name>")
                            continue
                        uid = int(parts[1])
                        name = " ".join(parts[2:])
                        cur.execute('UPDATE "User" SET name=%s WHERE id=%s;', (name, uid))
                        conn.commit()
                        print("updated" if cur.rowcount else "not found")

                    elif cmd == "delete":
                        if len(parts) != 2 or not parts[1].isdigit():
                            print("usage: delete <id>")
                            continue
                        uid = int(parts[1])
                        cur.execute('DELETE FROM "User" WHERE id=%s;', (uid,))
                        conn.commit()
                        print("deleted" if cur.rowcount else "not found")

                    else:
                        print("unknown command. type 'help'")

            except Exception as e:
                conn.rollback()
                print(f"error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    main()
