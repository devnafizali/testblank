# Start Chrome in headless mode
"C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" --headless --disable-gpu --remote-debugging-port=9222 --disable-gpu http://127.0.0.1:9222/json/version &

# google-chrome --user-data-dir="Default" --headless --disable-gpu --remote-debugging-port=9222 --disable-gpu http://127.0.0.1:9222/json/version &

# Wait for Chrome to start
sleep 2

# Use curl to fetch data from the specified URL
data=$(curl -s http://127.0.0.1:9222/json/version)

# Print the extracted webSocketDebuggerUrl
echo "$data"

# Close Chrome
# pkill chrome
# powershell.exe -Command "Stop-Process -Name chrome -Force"


