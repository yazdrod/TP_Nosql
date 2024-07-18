# EXERCICE 2 REPLICATION script



import os
import subprocess
import time
from pymongo import MongoClient

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {command}")
        print(result.stderr)
    return result.stdout

def create_directories():
    os.makedirs('db1', exist_ok=True)
    os.makedirs('db2', exist_ok=True)
    os.makedirs('db3', exist_ok=True)

def start_mongod_instances():
    commands = [
        'mongod --replSet rs0 --port 27017 --dbpath ./db1 --bind_ip localhost --fork --logpath ./db1/mongod.log',
        'mongod --replSet rs0 --port 27018 --dbpath ./db2 --bind_ip localhost --fork --logpath ./db2/mongod.log',
        'mongod --replSet rs0 --port 27019 --dbpath ./db3 --bind_ip localhost --fork --logpath ./db3/mongod.log'
    ]
    for command in commands:
        print(f"Running command: {command}")
        run_command(command)
        time.sleep(5)  # Give some time for the server to start

def initialize_replica_set():
    client = MongoClient('localhost', 27017)
    config = {
        "_id": "rs0",
        "members": [
            {"_id": 0, "host": "localhost:27017"},
            {"_id": 1, "host": "localhost:27018"},
            {"_id": 2, "host": "localhost:27019"}
        ]
    }
    client.admin.command("replSetInitiate", config)
    print("Replica set initiated.")
    time.sleep(10)  # Give some time for the replica set to initialize

def verify_replica_set():
    client = MongoClient('localhost', 27017)
    status = client.admin.command("replSetGetStatus")
    print("Replica set status:")
    print(status)

def main():
    create_directories()
    start_mongod_instances()
    initialize_replica_set()
    verify_replica_set()

if __name__ == "__main__":
    main()
