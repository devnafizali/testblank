# #!/bin/bash

# # Open Google Chrome
# "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" --headless --disable-gpu --remote-debugging-port=9222 --disable-gpu http://127.0.0.1:9222/json/version &
# sleep 10

# # Use PowerShell to invoke the REST API endpoint and retrieve the JSON data
# data=$(powershell.exe -Command "(Invoke-WebRequest -Uri 'http://127.0.0.1:9222/json/version' | ConvertFrom-Json)")

# # Print the JSON data
# echo "$data"

# # Close Chrome using PowerShell
# powershell.exe -Command "Stop-Process -Name chrome -Force"



#!/bin/bash

# Open Google Chrome
# "C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Default" --headless --disable-gpu --remote-debugging-port=9222 --disable-gpu http://127.0.0.1:9222/json/version &

google-chrome --user-data-dir="Default" --headless --disable-gpu --remote-debugging-port=9222 --disable-gpu http://127.0.0.1:9222/json/version &

data=$(curl -s http://127.0.0.1:9222/json/version)

# Print the fetched data
echo "$data"


# Close Chrome using pkill
pkill chrome
# powershell.exe -Command "Stop-Process -Name chrome -Force"


