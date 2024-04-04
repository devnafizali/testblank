// const fs = require("fs");
// const fetch = require("node-fetch");
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
    defaultViewport: null,
    executablePath: "/usr/bin/google-chrome",
    // executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe",
    devtools: true,
    ignoreHTTPSErrors: true,
    
  }); // Set to true for headless mode

  const page = await browser.newPage();
  await page.emulate(iPhone);

  // await page.setViewport({ width: 1000, height: 695, isMobile: true });

  //   await page.setViewport({ width: 1920, height: 1080 });
  // Check if cookies file exists
  // const cookies = JSON.parse(fs.readFileSync('cookies.json', 'utf8'));

  // Set cookies for the page
  // await page.setCookie(...cookies);
  const navigationTimeout = 60000;
  await page.setDefaultNavigationTimeout(navigationTimeout);
  const PG = {
    Page: {},
  };

  const fbPageUrl = "https://www.facebook.com/bayyinahinst";

  async function downloadImage(url, filePath) {
    try {
      const response = await fetch(url);
      const buffer = await response.buffer();

      // Write the buffer to the specified file path
      await fs.promises.writeFile(filePath, buffer);

      console.log("Image downloaded to:", filePath);
    } catch (error) {
      console.error("Error downloading image:", error);
    }
  }

  function findMobileNumber(texts) {
    // Regular expression to match a generic mobile number format
    const mobileNumberRegex = /\b\d{10,14}\b/;

    // Loop through each text in the array
    for (const text of texts) {
      // Use regex to find matches in the given text
      const matches = text.match(mobileNumberRegex);

      // If a match is found, return the first mobile number
      if (matches) {
        return matches[0];
      }
    }

    // Return null if no mobile number is found
    return null;
  }
  await page.goto("https://mobile.facebook.com/entrptaher");
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
    console.log("Widget removed successfully.");
  } else {
    console.log("Widget not found.");
  }
  await page.evaluate(async () => {
    window.scrollTo(0, document.body.scrollHeight - 500);
  });
  const posts = []
  for (let i = 0; i < 7; i++) {
    await page.waitForXPath('//*[text()="󰤥"]');
    const targetElements = await page.$x('//*[text()="󰤥"]');
    if (targetElements[i] == undefined) {
      continue;
    }
    const nextSibling = await targetElements[i].evaluateHandle((element) => {
      return element.parentElement.parentElement.parentElement.parentElement
        .nextElementSibling;
    });
    console.log(nextSibling);
    await nextSibling.click();
    // Wait for a specific element to appear after the click
    try {
      await page.waitForSelector(
        '[data-comp-id="22222"][data-type="container"]',
        { timeout: 3000 }
      );

      // Perform actions on the page
      const containerToRemove = await page.$(
        '[data-comp-id="22222"][data-type="container"]'
      );
      if (containerToRemove) {
        await page.evaluate((element) => element.remove(), containerToRemove);
        console.log("Widget removed successfully.");
      } else {
        console.log("Widget not found.");
      }
      const viewmore = await page.$x('//*[text()="View previous reply"]');
      for (const repl of viewmore) {
        await repl.click();
      }
      await page.waitForTimeout(3000);
      try {
        // Navigate to the page containing the comments
        // Wait for comments to load
        const targetElements2 = await page.$x('//*[text()="󰤥"]');
        const thepost = await targetElements2[0].evaluateHandle((element) => {
          const post = {};
          const comments = [];
          const prev =
            element.parentElement.parentElement.parentElement.parentElement
              .previousElementSibling.previousElementSibling;
          post.post_text = prev.textContent;
          const imgs = prev.querySelectorAll("[src]");
          const srcValues = [];
          imgs.forEach((element) => {
            srcValues.push(element.getAttribute("src"));
          });
          post.post_image = srcValues
          console.log(post)
          function nextElement(element) {
            let current =
              element.parentElement.parentElement.parentElement.parentElement;

            for (let i = 0; i < 5; i++) {
              const comment = {};
              const replies = [];
              if (current.nextElementSibling) {
                current = current.nextElementSibling;
                current.childNodes.forEach((element, index) => {
                  if (index == 1) {
                    const texts =
                      element.childNodes[0].childNodes[0].childNodes;
                    if (texts.length > 2) {
                      comment.author = texts[2].textContent;
                      comment.comment = texts[3].textContent;
                    } else {
                      comment.author = texts[0].textContent;
                      comment.comment = texts[1].textContent;
                    }
                  }
                  if (index == 2) {
                    const texts = element.childNodes[0].childNodes;
                    if (texts.length > 1) {
                      comment.comment_timestamp = texts[0].textContent;
                      comment.number_likes = texts[1].textContent;
                    } else {
                      comment.comment_timestamp = texts[0].textContent;
                      comment.number_likes = 0;
                    }
                  } else if (index > 2) {
                    const reply = {};
                    element.childNodes.forEach((element, index) => {
                      if (index == 1) {
                        const texts =
                          element.childNodes[0].childNodes[0].childNodes;
                        if (texts.length > 2) {
                          reply.author = texts[2].textContent;
                          reply.comment = texts[3].textContent;
                        } else {
                          reply.author = texts[0].textContent;
                          reply.comment = texts[1].textContent;
                        }
                      }
                      if (index == 2) {
                        const texts = element.childNodes[0].childNodes;
                        if (texts.length > 1) {
                          reply.comment_timestamp = texts[0].textContent;
                          reply.number_likes = texts[1].textContent;
                        } else {
                          reply.comment_timestamp = texts[0].textContent;
                          reply.number_likes = 0;
                        }
                      }
                    });
                    replies.push(reply);
                  }
                });
                comment.replies = replies;
                if (comment.author != undefined) {
                  comments.push(comment);
                }
              } else {
                break;
              }
            }
          }
          nextElement(element);
          console.log(comments);
          post.post_comments = comments
          return post;
        });
        posts.push(thepost.jsonValue())
      } catch (error) {
        console.error("Error:", error.message);
      }
    } catch (error) {
      console.log("No element");
    }
    await page.goBack();
    await page.waitForNavigation();
    // break;
    // Go back to the previous page

    // Wait for the page to be loaded after navigation
    // }
  }
  console.log(posts)
})();
