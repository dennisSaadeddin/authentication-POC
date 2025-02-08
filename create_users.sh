#!/bin/bash

echo "Creating users..."
echo "----------------"

echo -e "\n1. Creating John Doe..."
curl -X POST "http://localhost:8000/api/signup" \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "password": "password123"}' | python3 -m json.tool

echo -e "\n2. Creating Alice Smith..."
curl -X POST "http://localhost:8000/api/signup" \
  -H "Content-Type: application/json" \
  -d '{"username": "alice_smith", "password": "securepass456"}' | python3 -m json.tool

echo -e "\n3. Creating Bob Wilson..."
curl -X POST "http://localhost:8000/api/signup" \
  -H "Content-Type: application/json" \
  -d '{"username": "bob_wilson", "password": "pass789!"}' | python3 -m json.tool

echo -e "\n4. Creating Emma Brown..."
curl -X POST "http://localhost:8000/api/signup" \
  -H "Content-Type: application/json" \
  -d '{"username": "emma_brown", "password": "emma2024"}' | python3 -m json.tool

echo -e "\n5. Creating Mike Jones..."
curl -X POST "http://localhost:8000/api/signup" \
  -H "Content-Type: application/json" \
  -d '{"username": "mike_jones", "password": "mikepass!"}' | python3 -m json.tool

echo -e "\nUser creation completed!" 