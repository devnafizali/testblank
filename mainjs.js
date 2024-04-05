// // const fs = require("fs");
// // const fetch = require("node-fetch");
// import { KnownDevices } from "puppeteer";
// import puppeteer from "puppeteer";
// import fs from "fs";
// import fetch from "node-fetch";

// (async () => {
//   // Launch browser
//   const iPhone = KnownDevices["iPhone 13"];
//   const browser = await puppeteer.launch({
//     headless: false,
//     args: ["--start-maximized", "--no-sandbox"],
//     defaultViewport: null,
//     // executablePath: "/usr/bin/google-chrome",
//     executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe",
//     devtools: true,
//     ignoreHTTPSErrors: true,
//   }); // Set to true for headless mode

//   const page = await browser.newPage();
//     // await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36');
//   await page.emulate(iPhone);

//   // await page.setViewport({ width: 1000, height: 695, isMobile: true });

//   //   await page.setViewport({ width: 1920, height: 1080 });
//   // Check if cookies file exists
//   // const cookies = JSON.parse(fs.readFileSync('cookies.json', 'utf8'));

//   // Set cookies for the page
//   // await page.setCookie(...cookies);
//   const navigationTimeout = 60000;
//   await page.setDefaultNavigationTimeout(navigationTimeout);
//   const PG = {
//     Page: {},
//   };

//   const fbPageUrl = "https://www.facebook.com/bayyinahinst";

//   function findMobileNumber(texts) {
//     // Regular expression to match a generic mobile number format
//     const mobileNumberRegex = /\b\d{10,14}\b/;

//     // Loop through each text in the array
//     for (const text of texts) {
//       // Use regex to find matches in the given text
//       const matches = text.match(mobileNumberRegex);

//       // If a match is found, return the first mobile number
//       if (matches) {
//         return matches[0];
//       }
//     }

//     // Return null if no mobile number is found
//     return null;
//   }
// //   await page.goto("https://mobile.facebook.com/entrptaher");
// //   var popup = await page.waitForSelector(
// //     '[data-comp-id="22222"][data-type="container"]'
// //   );
//   // if (popup) {
//   //   popup.click();
//   // }

//   const posts = []; // Array to store posts
//   function getStoryFbid(url) {
//     // Split the URL based on '?' and '&'
//     const parts = url.split(/[?&]/);
    
//     // Loop through the parts to find the one containing 'story_fbid'
//     for (const part of parts) {
//       if (part.includes('story_fbid')) {
//         // Split the part again based on '=' to get the value
//         const value = part.split('=')[1];
//         return value;
//       }
//     }
    
//     // Return null if 'story_fbid' is not found in the URL
//     return null;
//   }

//   // Loop to iterate over a set number of times (in this case, only once)
//   for (let i = 0; i < 1; i++) {
//     // Navigate to a specific Facebook page
//     await page.goto("http://mobile.facebook.com/entrptaher");

//     // Remove a specific container element if it exists
//     const containerToRemove = await page.waitForSelector('[data-comp-id="22222"][data-type="container"]')
//     if (containerToRemove) {
//       await page.evaluate((element) => element.remove(), containerToRemove);
//       console.log("Widget removed successfully.");
//     } else {
//       console.log("Widget not found.");
//     }
  
//     // Scroll to the bottom of the page
//     await page.evaluate(async () => {
//       window.scrollTo(0, document.body.scrollHeight - 500);
//     });
//     await page.screenshot({ path: 'example_element.png' });
//     // Wait for a specific element to appear
//     await page.waitForXPath('//*[text()="󰤥"]');
//     const targetElements = await page.$x('//*[text()="󰤥"]');
//     if (targetElements[i] == undefined) {
//       continue;
//     }
  
//     // Click on the next sibling of the target element
//     const nextSibling = await targetElements[i].evaluateHandle((element) => {
//       return element.parentElement.parentElement.parentElement.parentElement.nextElementSibling;
//     });
//     await nextSibling.click();
  
//     // Reload the page after a timeout or if a specific element is found
//     try {
//       await page.waitForSelector('[data-comp-id="22222"][data-type="container"]', { timeout: 3000 });
//       await page.reload();
//     } catch (error) {
//       await page.reload();
//     }
  
//     // Wait for a specific element to appear after the click
//     try {
//       await page.waitForSelector('[data-comp-id="22222"][data-type="container"]', { timeout: 3000 });
  
//       // Remove a specific container element again if it exists
//       const containerToRemove = await page.$('[data-comp-id="22222"][data-type="container"]');
//       if (containerToRemove) {
//         await page.evaluate((element) => element.remove(), containerToRemove);
//         console.log("Widget removed successfully.");
//       } else {
//         console.log("Widget not found.");
//       }
  
//       // Click on 'View previous reply' links
//       const viewmore = await page.$x('//*[text()="View previous reply"]');
//       for (const repl of viewmore) {
//         await repl.click();
//       }
  
//       // Wait for a timeout
//       await page.waitForTimeout(3000);
  
//       // Extract post data
//       const targetElements2 = await page.$x('//*[text()="󰤥"]');
//       const thepost = await targetElements2[0].evaluateHandle((element) => {
//         // Initialize post object
//         const post = {};
//         const comments = [];
  
//         // Extract post text and image
//         const prev = element.parentElement.parentElement.parentElement.parentElement.previousElementSibling.previousElementSibling;
//         post.post_text = prev.textContent;
//         const imgs = prev.querySelectorAll("[src]");
//         const srcValues = [];
//         imgs.forEach((element) => {
//           srcValues.push(element.getAttribute("src"));
//         });
//         post.post_image = srcValues;
  
//         // Function to extract comments and replies
//         function nextElement(element) {
//           let current = element.parentElement.parentElement.parentElement.parentElement;
//           for (let i = 0; i < 5; i++) {
//             const comment = {};
//             const replies = [];
//             if (current.nextElementSibling) {
//               current = current.nextElementSibling;
//               current.childNodes.forEach((element, index) => {
//                 if (index == 1) {
//                   const texts = element.childNodes[0].childNodes[0].childNodes;
//                   if (texts.length > 2) {
//                     comment.author = texts[2].textContent;
//                     comment.comment = texts[3].textContent;
//                   } else {
//                     comment.author = texts[0].textContent;
//                     comment.comment = texts[1].textContent;
//                   }
//                 }
//                 if (index == 2) {
//                   const texts = element.childNodes[0].childNodes;
//                   if (texts.length > 1) {
//                     comment.comment_timestamp = texts[0].textContent;
//                     comment.number_likes = texts[1].textContent;
//                   } else {
//                     comment.comment_timestamp = texts[0].textContent;
//                     comment.number_likes = 0;
//                   }
//                 } else if (index > 2) {
//                   const reply = {};
//                   element.childNodes.forEach((element, index) => {
//                     if (index == 1) {
//                       const texts = element.childNodes[0].childNodes[0].childNodes;
//                       if (texts.length > 2) {
//                         reply.author = texts[2].textContent;
//                         reply.comment = texts[3].textContent;
//                       } else {
//                         reply.author = texts[0].textContent;
//                         reply.comment = texts[1].textContent;
//                       }
//                     }
//                     if (index == 2) {
//                       const texts = element.childNodes[0].childNodes;
//                       if (texts.length > 1) {
//                         reply.comment_timestamp = texts[0].textContent;
//                         reply.number_likes = texts[1].textContent;
//                       } else {
//                         reply.comment_timestamp = texts[0].textContent;
//                         reply.number_likes = 0;
//                       }
//                     }
//                   });
//                   replies.push(reply);
//                 }
//               });
//               comment.replies = replies;
//               if (comment.author != undefined) {
//                 comments.push(comment);
//               }
//             } else {
//               break;
//             }
//           }
//         }
//         nextElement(element);
  
//         // Assign comments to the post object
//         post.post_comments = comments;
//         return post;
//       });
  
//       // Push the post object to the posts array
//       posts.push(await thepost.jsonValue());
//       await page.screenshot({ path: 'example_element.png' });

//     } catch (error) {
//       console.error("Error:", error.message);
//     }
//   }
  
//   // Output the posts array
//   console.log(posts);
  
// })();














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
  await page.goto("https://mobile.facebook.com/entrptaher");
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
    console.log("Widget removed successfully.");
  } else {
    console.log("Widget not found.");
  }
  const postUrls = []

  for (let i = 0; i < 20; i++) {
    await page.evaluate(async () => {
      window.scrollTo(0, document.body.scrollHeight - 500);
    });
    await page.waitForXPath('//*[text()="󰤥"]');
    const targetElements = await page.$x('//*[text()="󰤥"]');
      if(targetElements[i]){
        const nextSibling = await targetElements[i].evaluateHandle((element) => {
          return element.parentElement.parentElement.parentElement.parentElement
            .nextElementSibling;
        });
        console.log(nextSibling);
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
