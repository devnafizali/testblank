import asyncio
from pyppeteer import launch
import pyppeteer
import re
import sys
import json
args = sys.argv

# Print the entire sys.argv array
# Check if arguments were provided
if len(args) < 3:
    print('Usage: python get_links.py url ws')
    print(args)
    sys.exit(1)  # Exit the script with an error code

# Get the parameter passed as an argument
param = args[1]
ws = json.loads(args[2])["webSocketDebuggerUrl"]
print(ws)
pRange = 10
async def main():
    # Launch browser
    print("Getting Page Posts list...")
    wsChromeEndpointurl = ws
    browser = await pyppeteer.connect({"browserWSEndpoint": wsChromeEndpointurl, "headless": True})
    # browser = await launch({'executablePath': 'C:/Program Files/Google/Chrome/Application/chrome.exe', 'headless':False})  # Set to True for headless mode
    page = await browser.newPage()
    await page.goto(f"https://m.facebook.com/{param}")

    async def get_story_fbid(url):
        # Split the URL based on '?' and '&'
        parts = re.split('[?&]', url)
        
        # Loop through the parts to find the one containing 'story_fbid'
        for part in parts:
            if 'story_fbid' in part:
                # Split the part again based on '=' to get the value
                value = part.split('=')[1]
                return value
        
        # Return None if 'story_fbid' is not found in the URL
        return None
    try:
        container_to_remove = await page.waitForSelector(
            '[data-comp-id="22222"][data-type="container"]', timeout=1000
        )
        # Check if the container element exists
        if container_to_remove:
            # Remove the container element from the DOM
            await page.evaluate('(element) => element.remove()', container_to_remove)
    except Exception as e:
        pass

    post_urls = []
    prevLength = 0
    postElements = []
    while True:
        target_elements = await page.querySelectorAll('[style="width:29px;"]')
        currentLength = len(target_elements)
        print(currentLength)
        if len(target_elements) < pRange:
            # await page.evaluate('window.scrollTo(0, 0-document.body.scrollHeight);')
            if currentLength > prevLength:
                await page.evaluate('window.scrollTo(0, document.body.scrollHeight);')
                prevLength = currentLength
        else:
            postElements = target_elements
            break
    for element in postElements:
        await asyncio.sleep(1)
        await page.evaluate('(element) => {element.parentElement.parentElement.parentElement.previousElementSibling.click(); return true;}', element)
        await page.waitForSelector('[style="width:32px; color:#4b4f56;"]')
        postUrl = await get_story_fbid(await page.evaluate('()=>{return window.location.href}'))
        if postUrl != None:
            print(postUrl)
            post_urls.append(postUrl)
        await asyncio.sleep(1)
        # await page.goBack()
        try:
            await page.waitForSelector('[data-comp-id="22222"]', timout=3000)
            await page.evaluate('()=>{const element = document.querySelector(`[data-comp-id="22222"]`); element.remove()}')
        except Exception as e:
            print(e)
        try:
            await page.waitForSelector('[data-action-id="32761"]', timeout=3000)
            await page.evaluate('() => {document.querySelector(`[data-action-id="32761"]`).click();}')
        except Exception as e:
            print(e)

        element = await page.querySelector('[class="rtl-ignore f2 a"]')
        # Perform the double click on the element
        try:        
            await page.waitForSelector('[class="rtl-ignore f2 a"]', timout=3000)
            element = await page.querySelector('[class="rtl-ignore f2 a"]')
            await element.click(clickCount=2)
            print("Double click successful!")
        except Exception as e:
            print("Double click failed:", e)
        try:
            await page.waitForSelector('[aria-label="Follow"]', timout=3000)
        except:
            continue
        
    # for i in range(pRange-1):
    #     prevPage = await page.evaluate('()=>{return window.location.href}') 
    #     try:
    #         # container_to_remove = await page.waitForSelector(
    #         #     '[data-comp-id="22222"][data-type="container"]', timeout=1000
    #         # )
    #         # # Check if the container element exists
    #         # if container_to_remove:
    #         #     # Remove the container element from the DOM
    #         #     await page.evaluate('(element) => element.remove()', container_to_remove)
    #         await page.waitForSelector('[style="width:29px;"]')
    #         target_elements = await page.querySelectorAll('[style="width:29px;"]')
    #         if target_elements[i]:
    #             await page.evaluate('(element) => {element.parentElement.parentElement.parentElement.previousElementSibling.click(); return true;}', target_elements[i])
    #             # next_sibling = await target_elements[i].evaluateHandle('(element) => {element.parentElement.parentElement.parentElement.previousElementSibling.click(); return true;}')
    #             while await page.evaluate('()=>{return window.location.href}') == prevPage:
    #                 print(await page.evaluate('()=>{return window.location.href}'))
    #                 continue
    #             await page.waitForSelector('[data-comp-id="22222"][data-type="container"]')
    #             if await page.evaluate('()=>{return window.location.href}') != None:
    #                 post_urls.append(await get_story_fbid(age.evaluate('()=>{return window.location.href}')))
    #             await page.goBack()
    #             await page.waitForNavigation()
    #             print(target_elements[i])
    #     except Exception as e:
    #         print(e)
    
    print(post_urls)
    
    with open('postUrls.txt', 'w') as file:
        file.write('\n'.join(post_urls))

    print('postUrls written to postUrls.txt file.')
    await asyncio.sleep(600)
    # await browser.close()

asyncio.get_event_loop().run_until_complete(main())
