#!/bin/bash

# Check if the URL argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <URL>"
    exit 1
fi

# URL argument passed to the script
url="$1"

# Run the Node.js script to fetch postUrls
node mainjs.js

# Read the postUrls from the file and pass them to the Python script along with the URL
python3 scrapper.py "$url"
