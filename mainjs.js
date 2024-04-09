
import { KnownDevices } from "puppeteer";
import puppeteer from "puppeteer";
import fs from "fs";
import fetch from "node-fetch";

(async () => {
  // Launch browser
  const iPhone = KnownDevices["iPhone 13"];
  const browser = await puppeteer.launch({
       headless: false,
    args: ["--start-maximized", "--no-sandbox"],
    defaultViewport: null,
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

  const containerToRemove = await page.waitForSelector(
    '[data-comp-id="22222"][data-type="container"]'
  );

  // Check if the container element exists
  if (containerToRemove) {
    // Remove the container element from the DOM
    await page.evaluate((element) => element.remove(), containerToRemove);
    console.log("Widget removed successfully.");
  } else {
    console.log("Widget not found.");
  }
  const postUrls = []
  for (let i = 0; i < 10; i++) {
    try {
      const containerToRemove = await page.waitForSelector(
        '[data-comp-id="22222"][data-type="container"]', {timeout:1000}
      );
    
      // Check if the container element exists
      if (containerToRemove) {
        // Remove the container element from the DOM
        await page.evaluate((element) => element.remove(), containerToRemove);
        console.log("Widget removed successfully.");
      } else {
        console.log("Widget not found.");
      }
    } catch (error) {
      console.log("Widget not found.");
    }
    await page.evaluate(async () => {
      window.scrollTo(0, document.body.scrollHeight);
    });
    await page.waitForSelector('[style="width:29px;"]');
    const targetElements = await page.$$('[style="width:29px;"]');
    console.log(targetElements)
    console.log(targetElements[i])
      if(targetElements[i]){
        const nextSibling = await targetElements[i].evaluate((element) => {
            console.log(element)
            const relement = element.parentElement.parentElement.parentElement.previousElementSibling
            relement.click()
            console.log(relement)
          return relement;
        });
        await page.waitForSelector(
          '[data-comp-id="22222"][data-type="container"]'
        );
        postUrls.push(getStoryFbid(page.url()))
        await page.goBack();
        await page.waitForNavigation();
      }
  }
  console.log(postUrls)
})();
