import asyncio
async def getPagePosts(page, pagId, post_urls):
    PG = {"Page":{}}
    all_the_posts = []
    for post_url in post_urls:
        await page.goto("https://www.facebook.com/"+pagId+"/posts/" + post_url)
        
        try:
          await page.waitForSelector(".__fb-light-mode.x1n2onr6.xzkaem6")

          await page.evaluate('''() => {
              const elementToRemove = document.querySelector(".__fb-light-mode.x1n2onr6.xzkaem6");
              if (elementToRemove) {
                  elementToRemove.remove();
              }
          }''')
        except:
          print("")

        try:
            await page.waitForSelector(".x78zum5.x1iyjqo2.x21xpn4.x1n2onr6", timeout=1000)
            await page.evaluate('''() => {
                const replyElements = document.querySelectorAll(".x78zum5.x1iyjqo2.x21xpn4.x1n2onr6");
                replyElements.forEach((e) => {
                    console.log(e);
                    e.childNodes[1].click();
                });
            }''')
        except Exception as error:
            print(error)

        try:
          post_details = await page.evaluate('''() => {
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
          postDetails = {};
          const postPage = document.querySelector(
            ".html-div.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd"
          );
          const element = postPage.childNodes[0].childNodes[2];
          const meta = postPage.childNodes[0].childNodes[3];
          postDetails.post_text = element.textContent;
          postDetails.post_date = convertToEpoch(
            formatTime(
              document
                .querySelector(
                  ".x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.xt0b8zv.xo1l8bm"
                )
                .textContent.replace(" ")
            )
          );
          postDetails.post_url = window.location.href
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
          postDetails.post_image = srcList;
          postDetails.post_video = vsrcList;
          const reactionCountElement = meta.querySelector(
            ".xrbpyxo.x6ikm8r.x10wlt62.xlyipyv.x1exxlbk"
          );
          postDetails.number_likes = reactionCountElement
            ? convertSuffixToNumber(reactionCountElement.textContent.trim())
            : 0;
          const iconElements = document.querySelectorAll("i"); // Select all <i> elements (you can use a more specific selector if needed)
          for (const element of iconElements) {
            const style = window.getComputedStyle(element); // Get the computed style of the element
            const backgroundPosition = style.getPropertyValue(
              "background-position"
            ); // Get the background-image property value
            if (backgroundPosition.includes("0px -1270px")) {
              const commentCount =
                element.parentElement.previousElementSibling.textContent;
              postDetails.number_comment = commentCount
                ? convertSuffixToNumber(commentCount)
                : 0;
            }
            if (backgroundPosition.includes("0px -1287px")) {
              const shareCount =
                element.parentElement.previousElementSibling.textContent;
              postDetails.number_shares = shareCount
                ? convertSuffixToNumber(shareCount)
                : 0;
            }
          }
          const allComments = [];
          try {
        const newCommentsWidget = document.querySelectorAll(".x169t7cy.x19f6ikt");
      console.log(newCommentsWidget);
      if (newCommentsWidget) {
        newCommentsWidget.forEach((element) => {
          const repList = [];
          var singleComment = {};
          const list = element.querySelectorAll("div .x46jau6");
          const mainComment = element.childNodes[0];
          const authorSelector = `span .xt0psk2`;
          const cTextSelector =
            ".xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs div";
          const rNumberSelector =
            ".x3nfvp2.x1n2onr6.xxymvpz.xh8yej3 .xi81zsa.x1nxh6w3.x1fcty0u.x1sibtaa.xexx8yu.xg83lxy.x18d9i69.x1h0ha7o.xuxw1ft";
          const timeStampSelector =
            ".x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.xt0b8zv.xi81zsa.xo1l8bm";
          const author = mainComment.querySelector(authorSelector);
          const cText = mainComment.querySelector(cTextSelector);
          const rNumber = mainComment.querySelector(rNumberSelector);
          const timeStamp = mainComment.querySelector(timeStampSelector);
          console.log(author);
          if (author && cText && timeStamp) {
            singleComment = {
              author: author.textContent,
              comment: getCommentText(cText),
              comment_timestamp: convertToEpoch(
                formatTime(
                  timeStamp.textContent.trim().replace(" ", "")
                ).replace("5undefined", "")
              ),
              author_url: author
                ? author.getAttribute("href")
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
              const timeStamp = element.querySelector(timeStampSelector);
              if (author && cText && timeStamp) {
                repList.push({
                  author: author.textContent,
                  comment: getCommentText(cText),
                  comment_timestamp: convertToEpoch(
                    formatTime(
                      timeStamp.textContent.trim().replace(" ", "")
                    ).replace("5undefined", "")
                  ),
                  author_url: author ? author.getAttribute("href") : "",
                  number_likes: rNumber
                    ? convertSuffixToNumber(rNumber.textContent)
                    : 0,
                });
              }
            });
          }
          singleComment.replies = repList;
          if (singleComment.author) {
            allComments.push(singleComment);
          }
        });
      }
      } catch (error) {
        console.log(error)
      }
          postDetails.comments = allComments;
          return postDetails;
        }''')
          all_the_posts.append(post_details)
        except:
          print("")
    PG['Page']['posts'] = all_the_posts
    return PG['Page']