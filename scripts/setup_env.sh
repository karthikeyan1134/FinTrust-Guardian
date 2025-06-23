#!/bin/bash

# This script sets up the development environment for FinTrust Guardian.

# Update package list and install Python and Node.js
sudo apt update
sudo apt install -y python3 python3-pip nodejs npm

# Install Python dependencies
pip3 install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install

# Go back to the root directory
cd ..

echo "Development environment setup complete!"