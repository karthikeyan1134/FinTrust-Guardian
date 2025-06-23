#!/bin/bash

# Start the Policy Gateway
echo "Starting Policy Gateway..."
cd backend
python app.py &

# Start the Data Vault
echo "Starting Data Vault..."
cd ../data-exchange
python server.py &

# Start the Compliance Dashboard
echo "Starting Compliance Dashboard..."
cd ../frontend
npm start &

# Wait for all services to start
wait

echo "All services are up and running!"