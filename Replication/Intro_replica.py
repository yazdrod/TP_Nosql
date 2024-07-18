import os
import time
from pymongo import MongoClient, errors

def start_mongod_instances():
    # Create directories for data files
    os.makedirs('data/db1', exist_ok=True)
    os.makedirs('data/db2', exist_ok=True)
    os.makedirs('data/db3', exist_ok=True)

    # Commands to start mongod instances
    commands = [
        'mongod --replSet rs0 --port 27017 --dbpath ./data/db1 --bind_ip localhost',
        'mongod --replSet rs0 --port 27018 --dbpath ./data/db2 --bind_ip localhost',
        'mongod --replSet rs0 --port 27019 --dbpath ./data/db3 --bind_ip localhost'
    ]

    for command in commands:
        os.system(f'{command} &')
        time.sleep(5)  # Wait a bit for the server to start

def initialize_replica_set():
    # Connect to the first mongod instance
    client = MongoClient('localhost', 27017)
    db = client.admin

    # Initiate the replica set
    rs_config = {
        "_id": "rs0",
        "members": [
            {"_id": 0, "host": "localhost:27017"},
            {"_id": 1, "host": "localhost:27018"},
            {"_id": 2, "host": "localhost:27019"}
        ]
    }

    try:
        db.command("replSetInitiate", rs_config)
        print("Replica set initiated.")
    except errors.OperationFailure as e:
        print(f"Error initiating replica set: {e}")

    time.sleep(10)  # Wait a bit for the replica set to initialize

def create_database_and_insert_data():
    client = MongoClient('localhost', 27017)
    db = client.GameOfThrones
    characters = db.characters

    characters.insert_many([
        {"name": "Jon Snow", "age": 25, "house": "Stark"},
        {"name": "Daenerys Targaryen", "age": 23, "house": "Targaryen"},
        {"name": "Tyrion Lannister", "age": 30, "house": "Lannister"}
    ])
    print("Data inserted into primary node.")

def verify_replication():
    secondary_ports = [27018, 27019]

    for port in secondary_ports:
        client = MongoClient('localhost', port)
        db = client.GameOfThrones
        characters = db.characters

        try:
            data = list(characters.find())
            print(f"Data from secondary node (port {port}):")
            for doc in data:
                print(doc)
        except errors.OperationFailure as e:
            print(f"Error reading from secondary node (port {port}): {e}")

def main():
    start_mongod_instances()
    initialize_replica_set()
    create_database_and_insert_data()
    verify_replication()

if __name__ == "__main__":
    main()
