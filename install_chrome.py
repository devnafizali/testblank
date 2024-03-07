import os
import requests
import subprocess
from tqdm import tqdm

def download_chrome(download_url):
    response = requests.get(download_url, stream=True)
    file_path = os.path.join(os.path.dirname(__file__), "google-chrome.deb")
    file_size = int(response.headers.get('content-length', 0))
    
    with open(file_path, "wb") as file, tqdm(
        desc="Downloading Google Chrome",
        total=file_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            bar.update(len(data))
            file.write(data)

    return file_path

def install_chrome(deb_file):
    os.chdir(os.path.dirname(__file__))
    subprocess.run(["ar", "x", deb_file])
    subprocess.run(["tar", "xvf", "data.tar.xz"])
def main():
    # Set the download URL
    chrome_download_url = "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"

    # Download Google Chrome
    deb_file = download_chrome(chrome_download_url)

    # Install Google Chrome
    install_chrome(deb_file)

if __name__ == "__main__":
    main()
