from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "bolt://neo4j:7687",
    auth=("neo4j", "neo4jpass"),
)

with driver.session() as session:
    result = session.run("RETURN 1 AS x").single()
    print("neo4j:", result["x"])

driver.close()
