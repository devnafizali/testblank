import asyncio
async def getPagePosts(page, post_count):
    # Get bottom of the website
    PG = {"Page":{}}    
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
    return PG['Page']