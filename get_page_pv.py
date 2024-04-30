import re
import os
import time
import asyncio
from functions import download_image
async def getPagePV(page, photo_number, video_number, name, waiting_time_for_photo, fbPageUrl):
    PG = {'Page':{}}
    try:
      # await page.goto(fbPageUrl + "/photos")
      # # Remove the first Facebook popup
      # await page.waitForSelector(".x92rtbv.x10l6tqk.x1tk7jg1.x1vjfegm")
      # await page.click(".x92rtbv.x10l6tqk.x1tk7jg1.x1vjfegm")
      
      # await page.waitForSelector(".xzg4506.xycxndf.xua58t2.x4xrfw5.x1lq5wgf.xgqcy7u.x30kzoy.x9jhf4c.x9f619.x5yr21d.xl1xv1r.xh8yej3")
      # await page.click("xzg4506.xycxndf.xua58t2.x4xrfw5.x1lq5wgf.xgqcy7u.x30kzoy.x9jhf4c.x9f619.x5yr21d.xl1xv1r.xh8yej3")
            # Wait for the element to load (adjust as needed)
        await page.waitForSelector(".x78zum5.x12nagc.x1n2onr6.x1s6qhgt")

        await page.click(".x78zum5.x12nagc.x1n2onr6.x1s6qhgt")
        await page.waitForFunction('''() => {
            return window.performance.getEntriesByType("resource").every(resource => resource.responseEnd <= window.performance.now());
        }''')
        start_time = time.time()
        photo_urls = []
        while True:
            await asyncio.sleep(0.1)
            await page.waitForSelector(".x1bwycvy")
            
            # Get the src attribute of the img element with class 'x1bwycvy'
            img_src = await page.evaluate('''() => {
                const img = document.querySelector(".x1bwycvy");
                return img ? img.src : null;
            }''')

            if img_src not in photo_urls:
                photo_urls.append(img_src)

            # Check the length of photo_urls and elapsed time
            if len(photo_urls) >= photo_number or (time.time() - start_time) >= waiting_time_for_photo:
                break

            await asyncio.sleep(0.1)
            await page.keyboard.press("ArrowRight")
    except:
      photo_urls = []
    print("Getting Page Videos...")
    # Get the videos
    try:
        await page.goto(fbPageUrl + "/videos")
        await page.waitForSelector(".x92rtbv.x10l6tqk.x1tk7jg1.x1vjfegm")
        # Click the element
        await page.click(".x92rtbv.x10l6tqk.x1tk7jg1.x1vjfegm")
        for i in range(int(video_number/5)):
            # Scroll to the bottom of the page
            await page.evaluate('''() => {
                window.scrollTo(0, document.body.scrollHeight);
            }''')

            # Wait for network requests to complete
            await page.waitForFunction('''() => {
                const requests = performance.getEntriesByType("resource");
                return requests.every(request => request.responseEnd > 0);
            }''')

            # Optionally, wait for a short interval to ensure all content is loaded
            await asyncio.sleep(0.5)
        await page.waitForSelector(".x78zum5.x1n2onr6.xh8yej3")
        video_elements = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll(".x78zum5.x1n2onr6.xh8yej3"), element => {
                const nestedElement = element.querySelector("a");
                if (nestedElement) {
                    return nestedElement.getAttribute("href");
                }
                return null;
            }).filter(href => href !== null);
        }''')

        PG["Page"]['videos'] = video_elements
    except:
      PG["Page"]['videos'] = []
    # Check if directory exists, if not create it
    page_name = re.sub(r'[^\x00-\x7F]+', '', name)
    print("Saving The json...")
    
    if page_name and not os.path.exists(page_name):
        os.mkdir(page_name)
    print("Downloading the images...")
    PG["Page"]["photos"] = []
    # Download and save images
    for i, element in enumerate(photo_urls):
        name = f"image_{i}_{int(time.time())}.jpg"
        name_of_photo = f"{page_name}/{name}"
        await download_image(page, element, name_of_photo)
        PG["Page"]["photos"].append(name) 
    return PG