#!/bin/bash

# Pull the latest MongoDB image
docker pull mongodb/mongodb-community-server:latest

# Start the MongoDB container
docker-compose up -d

# Wait for MongoDB to initialize
sleep 10

# Connect to the MongoDB container and set up the database and collections
sudo docker exec -it mongodb_container mongosh "mongodb+srv://dcou45093:ejSMSqWDSAlMLDTL@cluster0.kzthwzt.mongodb.net/" '
use Galaxies;

db.createCollection("Stars");

db.Stars.insertMany([
  { name: "Sun", type: "G-type", age: 4600000000, distance_from_earth: 0 },
  { name: "Sirius", type: "A-type", age: 300000000, distance_from_earth: 8.6 },
  { name: "Alpha Centauri", type: "G-type", age: 5500000000, distance_from_earth: 4.37 },
  { name: "Betelgeuse", type: "M-type", age: 8000000, distance_from_earth: 642.5 },
  { name: "Rigel", type: "B-type", age: 8000000, distance_from_earth: 863 }
]);

db.createCollection("Planets");

db.Planets.insertMany([
  { name: "Mercury", type: "Terrestrial", number_of_moons: 0, distance_from_sun: 57.91 },
  { name: "Venus", type: "Terrestrial", number_of_moons: 0, distance_from_sun: 108.2 },
  { name: "Earth", type: "Terrestrial", number_of_moons: 1, distance_from_sun: 149.6 },
  { name: "Mars", type: "Terrestrial", number_of_moons: 2, distance_from_sun: 227.9 },
  { name: "Jupiter", type: "Gas Giant", number_of_moons: 79, distance_from_sun: 778.5 }
]);

db.Stars.createIndex({ name: 1 });
db.Planets.createIndex({ name: 1 });

db.adminCommand({ listDatabases: 1 });

use admin;
db.runCommand({ fsync: 1 });
'
