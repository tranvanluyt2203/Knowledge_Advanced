from neo4j import GraphDatabase
import os
import time

# Thông tin kết nối Neo4j
uri = "neo4j+s://ffdfad2c.databases.neo4j.io"               # Địa chỉ database
username = "neo4j"                                          # Username
password = "niQisz0U5weBUMit5DuSDTxMXmDsU91qykqIEOJTA4o"    # Password

# Create Neo4j driver
def delete_old_graph(tx):
    query = """
    MATCH (n)
    DETACH DELETE n
    """
    tx.run(query)

def execute_cypher_block(tx, block):
    tx.run(block)

def split_into_blocks(file_content):
    # Split the content using two consecutive newlines as the delimiter
    blocks = file_content.split('\n\n')
    # Remove any leading/trailing whitespace from each block and filter out empty blocks
    blocks = [block.strip() for block in blocks if block.strip()]
    return blocks

folder_path = r".\cypher_query"
print(f"Number of files in folder: {len(os.listdir(folder_path))}")

for index, file_name in enumerate(os.listdir(folder_path)):
    file_path = os.path.join(folder_path, file_name)
    print(f"Processing file: {file_path}")
    
    driver = GraphDatabase.driver(uri, auth=(username, password), max_connection_lifetime=600)

    # Open session and process the graph creation
    with driver.session() as session:
        # if index == 0:
        #     session.execute_write(delete_old_graph)  # Delete old graph if needed

        # Load the file and split into blocks
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
            cypher_blocks = split_into_blocks(file_content)
        
        # Execute each Cypher block separately
        for block in cypher_blocks:
            print(f"Executing block:\n{block}\n")
            try:
                session.execute_write(execute_cypher_block, block)
            except Exception as e:
                print(f"Error executing block: {e}")

    # Close the driver connection
    driver.close()
