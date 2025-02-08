#!/bin/bash

echo "Creating test users..."
echo "--------------------"

echo -e "\n1. Creating Test User 1..."
curl -X POST "http://localhost:8000/api/signup" \
  -H "Content-Type: application/json" \
  -d '{"username": "test_user1", "password": "test123"}' | python3 -m json.tool

echo -e "\n2. Creating Test User 2..."
curl -X POST "http://localhost:8000/api/signup" \
  -H "Content-Type: application/json" \
  -d '{"username": "test_user2", "password": "test456"}' | python3 -m json.tool

echo -e "\n3. Creating Test User 3..."
curl -X POST "http://localhost:8000/api/signup" \
  -H "Content-Type: application/json" \
  -d '{"username": "test_user3", "password": "test789"}' | python3 -m json.tool

echo -e "\nTest user creation completed!" 