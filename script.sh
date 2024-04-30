# #!/bin/bash

# # Check if the URL argument is provided
# if [ "$#" -ne 1 ]; then
#     echo "Usage: $0 <URL>"
#     exit 1
# fi
# # URL argument passed to the script
# url="$1"
# # Start Chrome in headless mode
# "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" --headless --disable-gpu --remote-debugging-port=9222 --disable-gpu http://127.0.0.1:9222/json/version &

# # google-chrome --user-data-dir="Default" --headless --disable-gpu --remote-debugging-port=9222 --disable-gpu http://127.0.0.1:9222/json/version &

# # Wait for Chrome to start
# sleep 2

# # Use curl to fetch data from the specified URL
# data=$(curl -s http://127.0.0.1:9222/json/version)

# name=$(echo "$url" | awk -F'/' '{print $NF}')
# python3 get_links.py "$name" "$data"

#!/bin/bash

# Check if the URL argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <URL>"
    exit 1
fi

# URL argument passed to the script
url="$1"

# Start Chrome in headless mode (assuming Chrome is installed)
google-chrome --user-data-dir="Default" --headless --disable-gpu --remote-debugging-port=9222 --disable-gpu http://127.0.0.1:9222/json/version &

# Wait for Chrome to start
sleep 2

# Use curl to fetch data from the specified URL
data=$(curl -s http://127.0.0.1:9222/json/version)

name=$(echo "$url" | awk -F'/' '{print $NF}')
python3 get_links.py "$name" "$data"
python3 scrapper.py "$url"
pkill chrome
