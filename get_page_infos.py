from functions import convert_suffix_to_number
from functions import extract_date_from_text
from functions import get_categories

async def getPageInfos(page, fbPageUrl):
    PG = {'Page': {}}
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
      print(extract_date_from_text(texts))
      PG["Page"]["creation_date"] = extract_date_from_text(texts)
      print("Done")
    except:
        PG["Page"]["creation_date"] = ""
    
    
    # Navigate to page home
    print("Getting Page Infos...", end='', flush=True)
    await page.goto(fbPageUrl)

    # Remove pop up
    try:
      await page.waitForSelector(".x92rtbv.x10l6tqk.x1tk7jg1.x1vjfegm")
      await page.click(".x92rtbv.x10l6tqk.x1tk7jg1.x1vjfegm")
    except:
      print("")
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
    return PG['Page']