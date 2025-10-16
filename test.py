import requests
from lxml import etree

def import_html(url: str):
  # Now let's read an HTML table!
  headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
  }

  return requests.get(url, headers=headers).text

print(import_html("https://beaconbio.org/en/"))

from lxml import html

def mui_xpaths_from_html(rendered_html: str):
    doc = html.fromstring(rendered_html)

    # collect all elements that have any class token starting with 'Mui'
    mui_elems = doc.xpath("//*[contains(concat(' ', normalize-space(@class), ' '), ' Mui')]")

    # gather distinct class tokens that start with 'Mui'
    mui_classes = set()
    for el in doc.xpath("//*[@class]"):
        for token in el.get("class").split():
            if token.startswith("Mui"):
                mui_classes.add(token)

    # build safe XPaths (token-aware contains)
    per_class_xpath = {
        cls: f"//*[contains(concat(' ', normalize-space(@class), ' '), ' {cls} ')]"
        for cls in sorted(mui_classes)
    }

    return {
        "count_mui_elements": len(mui_elems),
        "mui_classes": sorted(mui_classes),
        "xpaths_by_class": per_class_xpath,
    }

# example usage with a rendered DOM (see Selenium snippet below)
# data = mui_xpaths_from_html(driver.page_source)
# print(data["xpaths_by_class"].get("MuiTypography-body1"))
