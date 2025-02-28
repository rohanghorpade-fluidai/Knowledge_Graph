from neo4j import GraphDatabase
import re

# Connection details
NEO4J_URI = "neo4j+s://f8c17793.databases.neo4j.io"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "3AM3ZDi7VREjZU6G2fzuyjyg5UFcXNI1cYuPpGvEX7Y"

# Load tuples from a file
def load_tuples(file_path='final_output.txt'):
    with open(file_path, 'r') as file:
        content = file.read().strip()
        if content.startswith('[') and content.endswith(']'):
            content = content[1:-1]
        tuples = [eval(t) for t in re.findall(r'\(([^)]+)\)', content)]
    return tuples

# Data to insert
tuples = load_tuples()

# Function to dynamically insert data into Neo4j
def insert_data(tx, entity1, label1, relation, entity2, label2, properties1, properties2, rel_properties):
    relation = relation.replace(" ", "_")  # Convert spaces to underscores
    query = f"""
    MERGE (a:{label1} {{name: $entity1}})
    SET a += $properties1
    MERGE (b:{label2} {{name: $entity2}})
    SET b += $properties2
    MERGE (a)-[r:{relation}]->(b)
    SET r += $rel_properties
    """
    tx.run(query,
           entity1=entity1,
           entity2=entity2,
           properties1=properties1,
           properties2=properties2,
           rel_properties=rel_properties)

# Connect to Neo4j and insert data
def main():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as session:
        for entity1, label1, relation, entity2, label2 in tuples:
            # Dynamically build properties based on the relation type
            properties1 = {"source": "PDF Document", "timestamp": "2024-12-01"}
            properties2 = {"source": "PDF Document", "timestamp": "2024-12-01"}
            rel_properties = {"extracted_by": "AI Model v1.2", "confidence": 0.95}

            # Add the dynamic property based on the relation
            if label2 in ["AMOUNT", "PERCENTAGE", "CAPACITY", "ENERGY", "FUNDING"]:
                properties1[relation] = entity2
            else:
                rel_properties[relation] = entity2

            session.execute_write(insert_data,
                                  entity1, label1,
                                  relation,
                                  entity2, label2,
                                  properties1, properties2,
                                  rel_properties)
    driver.close()
    print("Data inserted successfully!")

if __name__ == "__main__":
    main()
