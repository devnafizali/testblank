import asyncio
import re
import argparse
import importlib
import subprocess
import time
from posts_url_list import fetch_post_urls
from urllib.parse import urlparse

library_names = ['pyppeteer', 'pyppeteer_stealth', 'requests', 'datefinder', 'datetime', 'json', 'tqdm']
for library_name in library_names:
    try:
        importlib.import_module(library_name)
    except ImportError:
        print(f"{library_name} is not installed. Installing...")
        subprocess.check_call(['pip', 'install', library_name])
        print(f"{library_name} has been successfully installed.")
from pyppeteer import launch
import json
from get_page_infos import getPageInfos
from get_page_posts import getPagePosts
from get_page_pv import getPagePV
# from install_chrome import dechrome

# dechrome()
# Set up argument parser
parser = argparse.ArgumentParser(description='Facebook Scraper')
parser.add_argument('url', type=str, help='Facebook page URL')
parser.add_argument('--ptc', type=int, default=5, help='Post count')
parser.add_argument('--phc', type=int, default=5, help='Photo number')
parser.add_argument('--vnc', type=int, default=5, help='Video number')
parser.add_argument('--wtp', type=int, default=20, help='Waiting time for photo')

# Parse command-line arguments
args = parser.parse_args()
def get_last_part_of_url(url):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    last_part = path_parts[-1]
    return last_part
# Assign values from command-line arguments
fbPageId = get_last_part_of_url(args.url)
fbPageUrl = "https://fb.com/"+fbPageId
post_count = args.ptc
photo_number = args.phc
video_number = args.vnc
waiting_time_for_photo = args.wtp
vscroll_count = video_number // 5
# Set up Pyppeteer
async def setup_browser():
    # result = subprocess.run(['which', 'google-chrome'], capture_output=True, text=True, check=True)
    # chrome_path = result.stdout.strip()
    # print(chrome_path)
    browser = await launch({
        'headless': True,
        'args': ['--start-maximized', '--no-sandbox'],
        'defaultViewport': {'width':1280,'height':800},
        # 'executablePath':"C:/Program Files/Google/Chrome/Application/chrome.exe",
        'executablePath': "/usr/bin/google-chrome",
        'timeout': 60000  # Set navigation timeout here
    })
    return browser
  
async def main():
    start_time = time.time()
    # post_urls = await fetch_post_urls(fbPageId)
    # print(post_urls)
    post_urls = []
    with open("postUrls.txt", 'r') as file:
        post_urls = file.read().splitlines()
    # Set up browser
    browser = await setup_browser()
    # Create a new page
    page = await browser.newPage()
    # Placeholder for PG
    PG = {'Page': {}}
        # Command Epoch Timespan
    PG["Page"]["scrape_epoch_timestamp"] = int(time.time())
    # Facebook page URL
    # Navigate to the specified URL
    print("Getting page Meta Data...", fbPageUrl)
    await page.goto(fbPageUrl + "/about_profile_transparency")

    # Remove the first Facebook popup
    try:
      await page.waitForSelector(".x92rtbv.x10l6tqk.x1tk7jg1.x1vjfegm")
      await page.click(".x92rtbv.x10l6tqk.x1tk7jg1.x1vjfegm")
       # Wait for the element to load
      await page.waitForSelector(
        ".x9f619.x1n2onr6.x1ja2u2z.x78zum5.xdt5ytf.x193iq5w.xeuugli.x1r8uery.x1iyjqo2.xs83m0k.xamitd3.xsyo7zv.x16hj40l.x10b6aqq.x1yrsyyn"
    )
    except:
      pass
    print("Getting Page post details", end='', flush=True)
    posts = await getPagePosts(page,fbPageId, post_urls)
    inf = await getPageInfos(page, fbPageUrl)
    PG['Page'].update(inf)
    # Get bottom of the website
    PG['Page'].update(posts)
    pv = await getPagePV(page, photo_number, video_number, PG["Page"]["name"].replace(":", ""), waiting_time_for_photo, fbPageUrl)
    PG['Page'].update(pv["Page"])
    # Save the information in a JSON file
    page_name = re.sub(r'[^\x00-\x7F]+', '',  PG["Page"]["name"].replace(":", ""))
    file_name = f"{page_name}/{page_name}.json"
    
    cleaned_file_name = re.sub(r'[^\x00-\x7F]+', '', file_name)
    
    with open(cleaned_file_name, 'w', encoding='utf-8') as json_file:
        json.dump(PG, json_file, indent=2, ensure_ascii=False)
    await page.close()
    # Close the browser
    await browser.close()
    # await asyncio.sleep(1000)

# Run the main function
asyncio.get_event_loop().run_until_complete(main())
