import asyncio
import os
import re
import argparse
import importlib
import subprocess
import time
import platform
library_names = ['pyppeteer', 'pyppeteer_stealth', 'requests', 'datefinder', 'datetime', 'json', 'tqdm']
for library_name in library_names:
    try:
        importlib.import_module(library_name)
    except ImportError:
        print(f"{library_name} is not installed. Installing...")
        subprocess.check_call(['pip', 'install', library_name])
        print(f"{library_name} has been successfully installed.")
from pyppeteer import launch
from pyppeteer_stealth import stealth
from datetime import datetime
import requests
import datefinder
import json
from tqdm import tqdm
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

# Assign values from command-line arguments
fbPageUrl = args.url
post_count = args.ptc
photo_number = args.phc
video_number = args.vnc
waiting_time_for_photo = args.wtp
vscroll_count = video_number // 5

# Set up Pyppeteer
async def setup_browser():
    global chrome_path
    browser = await launch({
        # 'headless': False,
        'args': ['--start-maximized', ],
        'defaultViewport': {'width':1280,'height':800},
        'executablePath': "/opt/google/chrome/google-chrome",
        'timeout': 60000  # Set navigation timeout here
    })
    return browser

# Download image function
async def download_image(page, url, file_path):
    try:
        response = await page.evaluate(
            """async (url) => {
                const response = await fetch(url);
                const arrayBuffer = await response.arrayBuffer();
                return Array.from(new Uint8Array(arrayBuffer));
            }""",
            url
        )

        # Convert the list to bytes and write to the file
        with open(file_path, 'wb') as file:
            file.write(bytes(response))
    except Exception as error:
        print("Error downloading image:", error)

# Find mobile number function
def convert_suffix_to_number(input_string):
    # Define a dictionary to map multipliers to their corresponding values
    multiplier_mapping = {'K': 1000, 'M': 1000000, 'B': 1000000000}

    # Remove unnecessary words
    cleaned_string = input_string.replace('likes', '').replace('followers', '').replace('following', '').strip()

    # Extract numerical part and multiplier (if any)
    if cleaned_string[-1] in multiplier_mapping:
        multiplier = multiplier_mapping[cleaned_string[-1]]
        numeric_part = cleaned_string[:-1]
    else:
        multiplier = 1
        numeric_part = cleaned_string

    # Convert the numerical part to an integer and apply the multiplier
    try:
        result = int(float(numeric_part) * multiplier)
        return result
    except ValueError:
        print("Invalid input format. Unable to extract a valid number.")
        return None

def extract_date_from_text(text):
    matches = datefinder.find_dates(text)
    for match in matches:
        return match.strftime("%d %B %Y")
    return None

    for suffix, multiplier in suffix_multipliers.items():
        if suffix in value_str:
            numeric_part = float(value_str.replace(suffix, ''))
            return int(numeric_part * multiplier)

    # If no matching suffix is found, return the original value as an integer
    return int(value_str)
def get_categories(texts):
    contains_dot = any("·" in text for text in texts)
    new_texts = []
    if contains_dot:
        for text in texts:
            if "·" in text and text:
                split_text = text.split("·")
                # Remove the first index
                split_text = split_text[1:]
                # Trim leading and trailing spaces
                split_text = [word.strip() for word in split_text]
                new_texts.append(split_text)
    return new_texts
def convert_to_epoch(date_str):
    try:
        # Try parsing with comma
        date_obj = datetime.strptime(date_str, "%B %d, %Y")
    except ValueError:
        # If parsing with comma fails, try without comma
        date_obj = datetime.strptime(date_str, "%B %d %Y")

    # Convert datetime object to epoch format
    epoch_time = int(date_obj.timestamp())
    return epoch_time
async def main():
    start_time = time.time()
    # Set up browser
    browser = await setup_browser()

    # Create a new page
    page = await browser.newPage()

    # Placeholder for PG
    PG = {'Page': {}}
        # Command Epoch Timespan
    PG["Page"]["scrape_epoch_timestamp"] = ""
    # Facebook page URL
    # Navigate to the specified URL
    print("Accessing ", fbPageUrl)
    await page.goto(fbPageUrl + "/about_profile_transparency")

    # Remove the first Facebook popup
    await page.waitForSelector(".x92rtbv.x10l6tqk.x1tk7jg1.x1vjfegm")
    await page.click(".x92rtbv.x10l6tqk.x1tk7jg1.x1vjfegm")

    # Wait for the element to load
    await page.waitForSelector(
        ".x9f619.x1n2onr6.x1ja2u2z.x78zum5.xdt5ytf.x193iq5w.xeuugli.x1r8uery.x1iyjqo2.xs83m0k.xamitd3.xsyo7zv.x16hj40l.x10b6aqq.x1yrsyyn"
    )
    
    # Get the page ID
    print("Getting Page ID & creation date...", end='', flush=True)
    try:
        texts = await page.evaluate(
            """() => {
                const spans = document.querySelectorAll(
                    ".x13faqbe.x78zum5.xdt5ytf"
                ); 
                var pid = ""
                try{
                  spans.forEach((span) => {
                  const image = span ? span.querySelector("img").getAttribute("src"):""
                  if(image == "https://static.xx.fbcdn.net/rsrc.php/v3/y-/r/olD6qzqyixJ.png"){
                    pid = span.textContent
                  }
                });
                } catch (e){
                }
                return pid
            }"""
        )
        page_id = texts.replace("Page ID", "").strip()
        PG["Page"]["id"] = page_id
    except:
        PG["Page"]["id"] = ""
        print("Not found")

    # Get the page Creation
    try:
        texts = await page.evaluate(
            """() => {
                const spans = document.querySelectorAll(
                    ".x13faqbe.x78zum5.xdt5ytf"
                ); 
                var pid = ""
                try{
                  spans.forEach((span) => {
                  const image = span ? span.querySelector("img").getAttribute("src"):""
                  if(image == "https://static.xx.fbcdn.net/rsrc.php/v3/yG/r/p7Pf4gSWotr.png"){
                    pid = span.textContent
                  }
                });
                } catch (e){
                }
                return pid
            }"""
        )
        PG["Page"]["creation_date"] = extract_date_from_text(texts)
        print("Done")
    except:
        PG["Page"]["creation_date"] = ""
        print("Not found", end='', flush=True)
    
    
    # Navigate to page home
    print("Getting Page Infos...", end='', flush=True)
    await page.goto(fbPageUrl)

    # Remove pop up
    try:
      await page.waitForSelector(".x92rtbv.x10l6tqk.x1tk7jg1.x1vjfegm")
      await page.click(".x92rtbv.x10l6tqk.x1tk7jg1.x1vjfegm")
    except:
      main()
    # Remove login suggest
    # await page.waitForSelector(
    #     ".x78zum5.xdt5ytf.x2lah0s.x193iq5w.x2bj2ny.x1ey2m1c.xayqjjm.x9f619.xds687c.x1xy6bms.xn6708d.x1s14bel.x1ye3gou.xixxii4.x17qophe.x1u8a7rm"
    # )
    # await page.evaluate(
    #     '''() => {
    #         const element = document.querySelector(".x78zum5.xdt5ytf.x2lah0s.x193iq5w.x2bj2ny.x1ey2m1c.xayqjjm.x9f619.xds687c.x1xy6bms.xn6708d.x1s14bel.x1ye3gou.xixxii4.x17qophe.x1u8a7rm");
    #         if (element)
    #             element.remove();
    #     }'''
    # )

    # Get Page name
    try:
      await page.waitForSelector(".x1heor9g.x1qlqyl8.x1pd3egz.x1a2a7pz")
      infos = await page.evaluate('''() => {
        const spans = document.querySelectorAll(".x1heor9g.x1qlqyl8.x1pd3egz.x1a2a7pz");
        return Array.from(spans, span => span.textContent);
      }''')
      PG['Page']['name'] = infos[0].replace("Verified account", "")
    except:
      PG['Page']['name'] = ""
    # Get URL
    purl = page.url
    PG['Page']['url'] = fbPageUrl
    
    # Get cover photo
    image_url = await page.evaluate('''
        () => {
            // Find the image element with the specified attribute
            const imageElement = document.querySelector('[data-imgperflogname="profileCoverPhoto"]');

            // Check if the element is found and has the "src" attribute
            if (imageElement && imageElement.hasAttribute("src")) {
                // Return the value of the "src" attribute
                return imageElement.getAttribute("src");
            } else {
                // Return None or an indication that the image wasn't found
                return null;
            }
        }
    ''')
    PG['Page']['cover_photo'] = image_url if image_url else None

    # Profie picture
    image_url2 = await page.evaluate('''
        () => {
            // Find the image element with the specified mask attribute
            const imageElement = document.querySelector("image");

            // Check if the element is found and has the "xlink:href" or "href" attribute
            if (imageElement) {
                const xlinkHref = imageElement.getAttribute("xlink:href");
                const href = imageElement.getAttribute("href");

                // Return the value of the "xlink:href" or "href" attribute
                return xlinkHref || href;
            } else {
                // Return None or an indication that the image wasn't found
                return null;
            }
        }
    ''')

    PG['Page']['profile_photo'] = image_url2 if image_url2 else None
    # Getting the address
    locationPart = await page.evaluate('''()=>{
        const targetDiv = document.querySelectorAll(".x1b0d499.xuo83w3");
    var loc = "";
    targetDiv.forEach((element) => {

      src = element.getAttribute("src");
      if (
        src == "https://static.xx.fbcdn.net/rsrc.php/v3/yW/r/8k_Y-oVxbuU.png"
      ) {
        loc = element.parentElement.parentElement.textContent;
      }
    });
    return loc;
        }''')
    PG['Page']['location'] = locationPart

    # Intro
    all_texts = await page.evaluate('''
        () => {
            // Find all elements with the specified class
            const elements = document.querySelectorAll('.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.xzsf02u');

            // Extract text content from each element and return as an array
            return Array.from(elements, element => element.textContent.trim());
        }
    ''')
    # Getting the categories
    categoryPart = await page.evaluate('''()=>{
        const targetDiv = document.querySelectorAll(".x1b0d499.xuo83w3");
    var cry = "";
    targetDiv.forEach((element) => {

      src = element.getAttribute("src");
      if (
        src == "https://static.xx.fbcdn.net/rsrc.php/v3/ye/r/4PEEs7qlhJk.png"
      ) {
        cry = element.parentElement.parentElement.textContent;
      }
    });
    return cry;
        }''')
    PG['Page']['categories'] = get_categories([categoryPart])
    # Getting the number
    numberPart = await page.evaluate('''()=>{
      const targetDiv = document.querySelectorAll(".x1b0d499.xuo83w3");
  var phn = "";
  targetDiv.forEach((element) => {
    src = element.getAttribute("src");
    if (
      src == "https://static.xx.fbcdn.net/rsrc.php/v3/yE/r/7KDVc3hw483.png" || src == "https://static.xx.fbcdn.net/rsrc.php/v3/yT/r/Dc7-7AgwkwS.png"
    ) {
      phn = element.parentElement.parentElement.textContent;
    }
  });
  return phn;
        }''')
    PG['Page']['phone'] = {'mobile': numberPart}
    # Getting intro
    if all_texts and len(all_texts) > 1:
        PG['Page']['intro'] = all_texts[1]    
    # Social Links using page.evaluate
    try:
        await page.waitForSelector(
            '.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.x1qq9wsj.x1yc453h', {"timeout": 3000})

        links = await page.evaluate('''
            () => {
                const elements = document.querySelectorAll('.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.x1qq9wsj.x1yc453h');
                return Array.from(elements, element => element.textContent);
            }
        ''')

        PG['Page']['websites_and_social_links'] = links

    except Exception as e:
        PG['Page']['websites_and_social_links'] = []
        
        # Get followers and likes using page.evaluate
    try:
      await page.waitForSelector('.x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.xt0b8zv.xi81zsa.x1s688f')

      fl = await page.evaluate('''
          () => {
              const elements = document.querySelectorAll('.x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.xt0b8zv.xi81zsa.x1s688f');
              return Array.from(elements, element => element.textContent);
          }
      ''')

      PG['Page']['total_likes'] = convert_suffix_to_number(fl[0])
      PG['Page']['total_followers'] = convert_suffix_to_number(fl[1])
    except:
      PG['Page']['total_likes'] = 0
      PG['Page']['total_followers'] = 0
    
    print("Done")

    # Get bottom of the website
    print("Getting Posts...", end='', flush=True)
    
    # for _ in range(2):
    #     # Scroll to the bottom of the page
    #     await page.evaluate('''() => {
    #         window.scrollTo(0, document.body.scrollHeight);
    #     }''')

    #     # Wait for network requests to complete
    #     await page.waitForFunction('''() => {
    #         const requests = performance.getEntriesByType("resource");
    #         return requests.every(request => request.responseEnd > 0);
    #     }''')

    #     # Optionally, wait for a short interval to ensure all content is loaded
    #     await asyncio.sleep(1)
    # Get posts
    
    await page.waitForFunction('''() => {
        const requests = performance.getEntriesByType("resource");
        return requests.every(request => request.responseEnd > 0);
    }''')
    await asyncio.sleep(2)  # Adjust the sleep duration as needed

    await page.waitForSelector(".x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z")

    all_the_posts = await page.evaluate('''async (postCount) =>
    {
    const postDetails = [];
    function convertSuffixToNumber(valueStr) {
      if (valueStr == null) {
        return 0;
      }

      if (typeof valueStr !== "string") {
        return valueStr;
      }

      valueStr = valueStr.toUpperCase();

      const suffixMultipliers = {
        K: 1e3,
        M: 1e6,
        B: 1e9,
        // Add more suffixes if needed
      };

      const suffix = valueStr.charAt(valueStr.length - 1);
      const numericPart = parseFloat(valueStr);

      if (isNaN(numericPart)) {
        // Handle invalid input
        return NaN;
      }

      if (suffixMultipliers.hasOwnProperty(suffix)) {
        return numericPart * suffixMultipliers[suffix];
      } else {
        // If no matching suffix, return the original numeric value
        return numericPart;
      }
    }
    function convertToEpoch(dateStr) {
      // Check if the dateStr contains a comma
      var hasComma = dateStr.includes(",");
      dateStr = dateStr.replace("undefined", " ");
      try {
        // Try parsing with or without comma
        var dateObj;
        if (hasComma) {
          dateObj = new Date(dateStr.replace(/,/g, ""));
        } else {
          var parts = dateStr.split(" ");
          if (parts.length === 2) {
            // Add current year to the input string
            dateStr =
              parts[1] + " " + parts[0] + ", " + new Date().getFullYear();
          }
          dateObj = new Date(dateStr);
        }
      } catch (error) {
        console.error("Invalid date format");
        return dateStr;
      }

      // Convert Date object to epoch format in milliseconds
      var epochTime = dateObj.getTime();
      return epochTime;
    }

    async function waitForElement(selector, timeout) {
      const endTime = Date.now() + timeout;

      while (Date.now() < endTime) {
        const element = document.querySelector(selector);

        if (element) {
          return element;
        }
        // Wait for a short duration before the next check
        await new Promise((resolve) => setTimeout(resolve, 1000));
      }

      // If the element is not found within the specified timeout
      throw new Error(`Timeout: Element with selector ${selector} not found`);
    }
    function formatTime(input) {
      const currentTime = new Date();

      if (typeof input === "string") {
        if (input.endsWith("m")) {
          const minutes = parseInt(input, 10);
          currentTime.setMinutes(currentTime.getMinutes() - minutes);
        } else if (input.endsWith("h")) {
          const hours = parseInt(input, 10);
          currentTime.setHours(currentTime.getHours() - hours);
        } else if (input.endsWith("d")) {
          const days = parseInt(input, 10);
          currentTime.setDate(currentTime.getDate() - days);
        } else if (input.endsWith("w")) {
          const weeks = parseInt(input, 10);
          currentTime.setDate(currentTime.getDate() - weeks * 7);
        } else if (input.includes("at")) {
          // If it's a date string, no changes needed
          const d = input.split("at")["0"].replace("undefined", " ");
          const cd = d.split(" ");
          return `${cd[1]} ${cd[0]}, ${currentTime.getFullYear()}`;
        } else if (input.length > 5) {
          return input;
        }
        // Format the result as "Month Day, Year"
        const options = { year: "numeric", month: "long", day: "numeric" };
        return currentTime.toLocaleDateString(undefined, options);
      } else {
        // If it's not a string, return the input as is
        return input;
      }
    }
    function getCommentText(comment) {
      var result = Array.from(comment.childNodes)
        .map((node) => {
          if (node.nodeType === 3) {
            // Text node
            return node.nodeValue;
          } else if (node.nodeType === 1 && node.nodeName === "SPAN") {
            // Check if it's a span element (containing emoji)
            return Array.from(node.childNodes)
              .map((spanNode) => {
                if (spanNode.nodeType === 3) {
                  // Text node inside the span
                  return spanNode.nodeValue;
                } else if (
                  spanNode.nodeType === 1 &&
                  spanNode.nodeName === "IMG"
                ) {
                  // Image node (emoji)
                  return spanNode.alt;
                }
                return "";
              })
              .join("");
          }
          return "";
        })
        .join("");
      return result;
    }
    const postsDone = [];
    for (var i = 0; i < postCount*2 && postsDone.length < postCount; i++) {
      // Use a for...of loop to handle asynchronous operations
      const postWidgets = document.querySelectorAll(
        ".x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z"
      );
      for (const element of postWidgets) {
        if (!postsDone.includes(element)) {
          const description = element.querySelector(
            ".x1iorvi4.x1pi30zi.x1l90r2v.x1swvt13"
          );
          const date = element.querySelector(
            ".x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv.xo1l8bm"
          );
          const comment = element.querySelector(
            ".x1i10hfl.x1qjc9v5.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.x1ypdohk.xdl72j9.x2lah0s.xe8uvvx.x2lwn1j.xeuugli.x1hl2dhg.xggy1nq.x1t137rt.x1o1ewxj.x3x9cwd.x1e5q0jg.x13rtm0m.x3nfvp2.x1q0g3np.x87ps6o.x1a2a7pz.xjyslct.xjbqb8w.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1heor9g.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.x16tdsg8.x1ja2u2z.xt0b8zv"
          );
          const imageElements = element.querySelectorAll(".x1n2onr6 img");
          const videoElements = element.querySelectorAll("video");
          const srcList = [];
          const vsrcList = [];

          imageElements.forEach((element) => {
            const src = element.getAttribute("src");
            if (src && !src.includes("data:image") && !src.includes("emoji")) {
              srcList.push(src);
            }
          });
          videoElements.forEach((element) => {
            const src = element.getAttribute("src");
            vsrcList.push(src);
          });

          const reacts = element.querySelector(
            ".xrbpyxo.x6ikm8r.x10wlt62.xlyipyv.x1exxlbk span span"
          );
          var totalShares = "0";
          const totalReacts = reacts ? reacts.textContent : 0;
          var commentText = "0";
          const descriptionText = description ? description.textContent : "";
          const dateText = date
            ? formatTime(date.textContent.replace(" "))
            : "";
          const postUrl = date ? date.getAttribute("href") : "";
          const allComments = [];

          // Check if comment exists before clicking
          if (comment) {
            await comment.click();
            await new Promise((resolve) => setTimeout(resolve, 1000));
            try {
              const [commentsWidget0] = await Promise.all([
                waitForElement(
                  ".xwya9rg.x11i5rnm.x1e56ztr.x1mh8g0r.xh8yej3",
                  5000
                ),
              ]);
              const commentSections0 =
                commentsWidget0.querySelectorAll(".x169t7cy.x19f6ikt");
              if (commentSections0) {
                for (const element of commentSections0) {
                  const replies = element.querySelector(
                    ".x78zum5.x1w0mnb.xeuugli"
                  );
                  if (replies) {
                    replies.click();
                  }
                }
              }
            } catch (error) {
              try {
                document
                  .querySelector(
                    ".x1i10hfl.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x1ypdohk.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x16tdsg8.x1hl2dhg.xggy1nq.x87ps6o.x1lku1pv.x1a2a7pz.x6s0dn4.x14yjl9h.xudhj91.x18nykt9.xww2gxu.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x78zum5.xl56j7k.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.xc9qbxq.x14qfxbe.x1qhmfi1"
                  )
                  .click();
              } catch (e) {
                console.log(e);
              }
              console.log(error);
            }
            await new Promise((resolve) => setTimeout(resolve, 1000));
            try {
              const [commentsWidget] = await Promise.all([
                waitForElement(
                  ".xwya9rg.x11i5rnm.x1e56ztr.x1mh8g0r.xh8yej3",
                  5000
                ),
              ]);
              const cands = commentsWidget.querySelectorAll(
                ".x9f619.x1n2onr6.x1ja2u2z.x78zum5.xdt5ytf.x2lah0s.x193iq5w.xeuugli.xsyo7zv.x16hj40l.x10b6aqq.x1yrsyyn"
              );
              cands.forEach((element) => {
                const textel = element.textContent;
                if (textel.includes("comment") && !textel.includes("Most")) {
                  commentText = textel
                    .replace("comment", "")
                    .replace("s", "")
                    .replace(" ", "");
                } else if (textel.includes("share")) {
                  totalShares = textel
                    .replace("share", "")
                    .replace("s", "")
                    .replace(" ", "");
                }
              });
              const newCommentsWidget =
                commentsWidget.querySelectorAll(".x169t7cy.x19f6ikt");
              const replies = [];
              if (newCommentsWidget) {
                newCommentsWidget.forEach((element) => {
                  const repList = [];
                  var singleComment = {};
                  const list = element.querySelectorAll("div .x46jau6");
                  const mainComment = element.querySelector("div:nth-child(1)");
                  const authorSelector =
                    `.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x10flsy6.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1tu3fi.x3x7a5m.x1nxh6w3.x1sibtaa.x1s688f.xzsf02u`;
                  const cTextSelector =
                    ".xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs div";
                  const rNumberSelector =
                    ".x3nfvp2.x1n2onr6.xxymvpz.xh8yej3 .xi81zsa.x1nxh6w3.x1fcty0u.x1sibtaa.xexx8yu.xg83lxy.x18d9i69.x1h0ha7o.xuxw1ft";
                  const timeStampSelector =
                    ".x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.xt0b8zv.xi81zsa.xo1l8bm";
                  const author = mainComment.querySelector(authorSelector);
                  const cText = mainComment.querySelector(cTextSelector);
                  const rNumber = mainComment.querySelector(rNumberSelector);
                  const timeStamp =
                    mainComment.querySelector(timeStampSelector);
                    console.log(author)
                  if (author && cText && timeStamp) {
                    singleComment = {
                      author: author.textContent,
                      comment: getCommentText(cText),
                      comment_timestamp: convertToEpoch(
                        formatTime(timeStamp.textContent
                          .trim()
                          .replace(" ", ""))
                          .replace("5undefined", "")
                      ),
                      author_url: author
                        ? author.parentElement.parentElement.getAttribute("href")
                        : "url_not_available",
                      number_likes: rNumber
                        ? convertSuffixToNumber(rNumber.textContent)
                        : 0,
                    };
                  }
                  if (list && list.length > 0) {
                    list.forEach((element) => {
                      const author = element.querySelector(authorSelector);
                      const cText = element.querySelector(cTextSelector);
                      const rNumber = element.querySelector(rNumberSelector);
                      const timeStamp =
                        element.querySelector(timeStampSelector);
                      if (author && cText && timeStamp) {
                        repList.push({
                          author: author.textContent,
                          comment: getCommentText(cText),
                          comment_timestamp: convertToEpoch(
                            formatTime(timeStamp.textContent
                              .trim()
                              .replace(" ", ""))
                              .replace("5undefined", "")
                          ),
                          author_url: author
                            ? author.parentElement.parentElement.getAttribute("href")
                            : "url_not_available",
                          number_likes: rNumber
                            ? convertSuffixToNumber(rNumber.textContent)
                            : 0,
                        });
                      }
                    });
                  }
                  singleComment.replies = repList;
                  if(singleComment.author){
                    allComments.push(singleComment)
                  }
                });
              }
              document
                .querySelector(
                  ".x1i10hfl.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x1ypdohk.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x16tdsg8.x1hl2dhg.xggy1nq.x87ps6o.x1lku1pv.x1a2a7pz.x6s0dn4.x14yjl9h.xudhj91.x18nykt9.xww2gxu.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x78zum5.xl56j7k.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.xc9qbxq.x14qfxbe.x1qhmfi1"
                )
                .click();
            } catch (error) {
              console.log(error);
              try {
                document
                  .querySelector(
                    ".x1i10hfl.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x1ypdohk.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x16tdsg8.x1hl2dhg.xggy1nq.x87ps6o.x1lku1pv.x1a2a7pz.x6s0dn4.x14yjl9h.xudhj91.x18nykt9.xww2gxu.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x78zum5.xl56j7k.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.xc9qbxq.x14qfxbe.x1qhmfi1"
                  )
                  .click();
              } catch (e) {
                console.log(e);
              }
            }
          }
          postDetails.push({
            post_date: dateText ? convertToEpoch(dateText) : "",
            post_url: postUrl,
            post_text: descriptionText,
            post_image: srcList,
            post_video: vsrcList,
            number_likes: convertSuffixToNumber(totalReacts),
            number_shares: convertSuffixToNumber(totalShares),
            number_comment: commentText
              ? convertSuffixToNumber(commentText)
              : 0,
            comments: allComments ? allComments : [],
          });
          postsDone.push(element);
        }
      }
      // Scroll to the bottom of the page
      if (postDetails.length >= postCount) {
        break;
      }
      window.scrollTo(0, document.body.scrollHeight);
      await new Promise((resolve) => setTimeout(resolve, 500));
    }

    console.log(postDetails);
    return postDetails;
    }''', post_count)
    
    PG['Page']['posts'] = all_the_posts
    print("Done")
    print("Getting Page Photos...", end='', flush=True)
    photo_urls = []
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
    print("Done")
    print("Getting Page Videos...", end='', flush=True)

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
    
    
    print("Done")
    # Check if directory exists, if not create it
    page_name = PG.get('Page', {}).get('name', '').replace(":", "")
    print("Saving The json...", end='', flush=True)

    if page_name and not os.path.exists(page_name):
        os.mkdir(page_name)
    print("Done")
    print("Downloading the images...", end='', flush=True)
    PG["Page"]["photos"] = []
    # Download and save images
    for i, element in enumerate(photo_urls):
        name = f"image_{i}_{int(time.time())}.jpg"
        name_of_photo = f"{page_name}/{name}"
        await download_image(page, element, name_of_photo)
        PG["Page"]["photos"].append(name) 
    print("Done")
    end_time = time.time()
    elapsed_time_seconds = end_time-start_time
    minutes = int(elapsed_time_seconds // 60)
    seconds = int(elapsed_time_seconds % 60)
    PG["Page"]["scrape_epoch_timestamp"] = int(time.time())
    # Save the information in a JSON file
    file_name = f"{page_name}/{page_name}.json"
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(PG, json_file, indent=2, ensure_ascii=False)
    await page.close()
    # Close the browser
    await browser.close()
    # await asyncio.sleep(1000)

# Run the main function
asyncio.get_event_loop().run_until_complete(main())
