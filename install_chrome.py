import requests
import zipfile
import io
import os

# URL of the ZIP file
zip_url = "https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-41/stable-headless-chromium-amazonlinux-2017-03.zip"

# Download the ZIP file
response = requests.get(zip_url)
if response.status_code == 200:
    # Create a BytesIO object from the content
    zip_content = io.BytesIO(response.content)

    # Extract the contents of the ZIP file to the current directory
    with zipfile.ZipFile(zip_content, 'r') as zip_ref:
        zip_ref.extractall(os.getcwd())
    print("Installation successful!")
else:
    print(f"Failed to download ZIP file. Status code: {response.status_code}")
