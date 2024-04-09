#!/bin/bash

# Check if the URL argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <URL>"
    exit 1
fi
# URL argument passed to the script
url="$1"

# Extract the last part or name from the URL using awk or sed
# Here, we use awk to extract the last field separated by '/'
name=$(echo "$url" | awk -F'/' '{print $NF}')

# Run the Node.js script with the extracted name as an argument
node mainjs.js "$name"

# Read the postUrls from the file and pass them to the Python script along with the URL
python3 scrapper.py "$url"
