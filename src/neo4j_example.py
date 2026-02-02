#!/usr/bin/env python3
# neo4j_cli.py
# pip install neo4j

from neo4j import GraphDatabase

URI = "bolt://neo4j:7687"
AUTH = ("neo4j", "neo4jpass")

HELP = """Commands:
  list
  create <name>
  read <user_id>
  update <user_id> <name>
  delete <user_id>
  help
  quit
"""

def main():
    driver = GraphDatabase.driver(URI, auth=AUTH)

    with driver.session() as session:
        # clean start (optional)
        session.run("MATCH (n:User) DETACH DELETE n")

        # stable id + uniqueness
        session.run(
            "CREATE CONSTRAINT user_id_unique IF NOT EXISTS "
            "FOR (u:User) REQUIRE u.user_id IS UNIQUE"
        )

        print("Initialized User nodes (user_id is UUID).")
        print(HELP)

        while True:
            line = input("> ").strip()
            if not line:
                continue

            parts = line.split()
            cmd = parts[0].lower()

            if cmd in ("quit", "exit"):
                break
            if cmd == "help":
                print(HELP)
                continue

            try:
                if cmd == "list":
                    rows = session.run(
                        "MATCH (u:User) "
                        "RETURN u.user_id AS user_id, u.name AS name "
                        "ORDER BY u.user_id"
                    ).data()
                    if not rows:
                        print("(empty)")
                    else:
                        for r in rows:
                            print(f"{r['user_id']}: {r['name']}")

                elif cmd == "create":
                    if len(parts) < 2:
                        print("usage: create <name>")
                        continue
                    name = " ".join(parts[1:])
                    r = session.run(
                        "CREATE (u:User {user_id: randomUUID(), name: $name}) "
                        "RETURN u.user_id AS user_id",
                        name=name,
                    ).single()
                    print(f"created user_id={r['user_id']}")

                elif cmd == "read":
                    if len(parts) != 2:
                        print("usage: read <user_id>")
                        continue
                    user_id = parts[1]
                    r = session.run(
                        "MATCH (u:User {user_id: $user_id}) "
                        "RETURN u.user_id AS user_id, u.name AS name",
                        user_id=user_id,
                    ).single()
                    print("not found" if r is None else f"{r['user_id']}: {r['name']}")

                elif cmd == "update":
                    if len(parts) < 3:
                        print("usage: update <user_id> <name>")
                        continue
                    user_id = parts[1]
                    name = " ".join(parts[2:])
                    r = session.run(
                        "MATCH (u:User {user_id: $user_id}) "
                        "SET u.name = $name "
                        "RETURN count(u) AS c",
                        user_id=user_id,
                        name=name,
                    ).single()
                    print("updated" if r["c"] else "not found")

                elif cmd == "delete":
                    if len(parts) != 2:
                        print("usage: delete <user_id>")
                        continue
                    user_id = parts[1]
                    r = session.run(
                        "MATCH (u:User {user_id: $user_id}) "
                        "DELETE u "
                        "RETURN count(u) AS c",
                        user_id=user_id,
                    ).single()
                    print("deleted" if r["c"] else "not found")

                else:
                    print("unknown command. type 'help'")

            except Exception as e:
                print(f"error: {type(e).__name__}: {e}")

    driver.close()

if __name__ == "__main__":
    main()