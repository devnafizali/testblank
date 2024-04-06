import asyncio
from pyppeteer import launch
import re
import tempfile
import os

async def fetch_post_urls(pageId):
    browser = await launch(
    headless=True,
    args=["--start-maximized", "--no-sandbox"],
    defaultViewport=None,
    executablePath = "/usr/bin/google-chrome",
    # executablePath ="C:/Program Files/Google/Chrome/Application/chrome.exe",
    devtools=True,
    ignoreHTTPSErrors=True,)
    
    try:
        page = await browser.newPage()
        await page.setUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1')
        await page.setViewport({'width': 390, 'height': 844, 'deviceScaleFactor': 3, 'isMobile': True, 'hasTouch': True})
        
        await page.goto("https://m.facebook.com/"+pageId+"/posts")
        await page.waitForSelector('[data-comp-id="22222"][data-type="container"]')
        container_to_remove = await page.querySelector('[data-comp-id="22222"][data-type="container"]')

        def get_story_fbid(url):
            # Use re to split the URL based on '?' and '&'
            parts = re.split(r'[?&]', url)
            
            # Loop through the parts to find the one containing 'story_fbid'
            for part in parts:
                if 'story_fbid' in part:
                    # Split the part again based on '=' to get the value
                    value = part.split('=')[1]
                    return value
            # Return None if 'story_fbid' is not found in the URL
            return None

        # Check if the container element exists
        if container_to_remove:
            # Remove the container element from the DOM
            await page.evaluate('(element) => element.remove()', container_to_remove)
            pass
        else:
            pass
            
        post_urls = []
        for i in range(20):
            try:
                containerToRemove = await page.waitForSelector('[data-comp-id="22222"][data-type="container"]', {'timeout': 1000})

                # Check if the container element exists
                if containerToRemove:
                    # Remove the container element from the DOM
                    await page.evaluate('(element) => element.remove()', containerToRemove)
                    pass
                else:
                    pass
            except Exception as e:
                pass
            await page.evaluate('''() => {
                window.scrollTo(0, document.body.scrollHeight-100);
            }''')
            await page.waitForSelector('[style="width:29px;"]')
            target_elements = await page.querySelectorAll('[style="width:29px;"]')
            
            if len(target_elements) > i:
                next_sibling = await page.evaluate('''(element) => {
                    const relement = element.parentElement.parentElement.parentElement.previousElementSibling;
                    relement.click();
                    return relement;
                }''', target_elements[i])

                await page.waitForSelector('[data-comp-id="22222"][data-type="container"]')
                url = get_story_fbid(await page.evaluate("window.location.href"))
                if url is not None:
                    post_urls.append(url)
                await page.goBack()
                await page.waitForNavigation()
        await browser.close()
        return post_urls
    except Exception as e:
        if browser:
            await browser.close()
    finally:
        if browser:
            await browser.close()
        

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(fetch_post_urls())

