#!/bin/bash

echo "Setting up 'Ask Your Data' environment"

# Step 1: Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Step 2: Upgrade pip
pip install --upgrade pip

# Step 3: Install project dependencies
pip install -r requirements.txt

# Step 4: Launch the Streamlit app
streamlit run chat_assistant.py  # Change this if your filename is different

echo "Done! Your app is now running."
