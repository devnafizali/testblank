import { KnownDevices } from "puppeteer";
import puppeteer from "puppeteer";
import fs from "fs";
import fetch from "node-fetch";

(async () => {
  // Launch browser
  const iPhone = KnownDevices["iPhone 13"];
  const browser = await puppeteer.launch({
       headless: true,
    args: ["--start-maximized", "--no-sandbox"],
    // defaultViewport: null,
    executablePath: "/usr/bin/google-chrome",
    // executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe",
    devtools: true,
    ignoreHTTPSErrors: true,
  }); // Set to true for headless mode

  const page = await browser.newPage();
  await page.emulate(iPhone);
  await page.goto("https://mobile.facebook.com/Boeing");
  function getStoryFbid(url) {
    // Split the URL based on '?' and '&'
    const parts = url.split(/[?&]/);
    
    // Loop through the parts to find the one containing 'story_fbid'
    for (const part of parts) {
      if (part.includes('story_fbid')) {
        // Split the part again based on '=' to get the value
        const value = part.split('=')[1];
        return value;
      }
    }
    
    // Return null if 'story_fbid' is not found in the URL
    return null;
  }
  var popup = await page.waitForSelector(
    '[data-comp-id="22222"][data-type="container"]'
  );
  // if (popup) {
  //   popup.click();
  // }
  const containerToRemove = await page.$(
    '[data-comp-id="22222"][data-type="container"]'
  );

  // Check if the container element exists
  if (containerToRemove) {
    // Remove the container element from the DOM
    await page.evaluate((element) => element.remove(), containerToRemove);
  } else {
   
  }
  const postUrls = []

  for (let i = 0; i < 20; i++) {
    await page.evaluate(async () => {
      window.scrollTo(0, document.body.scrollHeight);
    });
    await page.waitForNetworkIdle()
    await page.waitForXPath('//*[text()="󰤥"]');
    const targetElements = await page.$x('//*[text()="󰤥"]');
      if(targetElements[i]){
        const nextSibling = await targetElements[i].evaluateHandle((element) => {
          return element.parentElement.parentElement.parentElement.parentElement
            .nextElementSibling;
        });
        await nextSibling.click();
        await page.waitForSelector(
          '[data-comp-id="22222"][data-type="container"]'
        );
        postUrls.push(getStoryFbid(page.url()))
        await page.goBack();
        await page.waitForNavigation();
      }
      
      // break;
      // Go back to the previous page

      // Wait for the page to be loaded after navigation
    // }
  }
  console.log(postUrls)
})();
