
# URL argument passed to the script
url="$1"
ptc=5
phc=5
vnc=5
if [ $# -gt 1 ]; then
    ptc="$2"
fi
if [ $# -gt 2 ]; then
    phc="$3"
fi
if [ $# -gt 3 ]; then
    vnc="$4"
fi


# Start Chrome in headless mode (assuming Chrome is installed)
google-chrome --profile-directory="Default" --headless --disable-gpu --remote-debugging-port=9222 --disable-gpu http://127.0.0.1:9222/json/version &

# Wait for Chrome to start
sleep 2

# Use curl to fetch data from the specified URL
data=$(curl -s http://127.0.0.1:9222/json/version)

name=$(echo "$url" | awk -F'/' '{print $NF}')
python get_links.py "$name" "$data" $ptc
pkill chrome
python scrapper.py "$url" --phc "$phc" --vnc "$vnc"
