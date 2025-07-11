########################################  Deps ###########################################  

import requests
import csv
import time
import re

######################################## Helpers #########################################

def extract_upc_from_images(image_list):
    for image_obj in image_list:
        for key in ["image", "thumbnail", "image2x"]:
            url = image_obj.get(key)
            if url:
                match = re.search(r"[_-](\d{13})-", url)
                if match:
                    return match.group(1)
    return "No UPC Found"

######################################## Configure ######################################## 

STORE_ID = int(input("Store ID: "))
UPC = False
res = input("Do you want to know the UPC? (Y/N) | Warning: This will reduce speeds | : ")
if res.lower() == "y":
    UPC = True

SUMMARY_URL = f"https://www.wholefoodsmarket.com/stores/{STORE_ID}/summary"
response = requests.get(SUMMARY_URL)
if response.json() is None:
    print(f"Store {STORE_ID} is invalid or inactive.")
    exit()

OFFSET = 0
LIMIT = 60
BASE_URL = "https://www.wholefoodsmarket.com/api/products/category/all-products"
params = {
    "leafCategory": "all-products",
    "store": STORE_ID,
    "limit": LIMIT,
    "offset": OFFSET
}

response = requests.get(BASE_URL, params=params)
resp = requests.get(BASE_URL, params=params)
data = resp.json()
total = data["facets"][0]["refinements"][0]["count"]
print("Total items reported:", total)

################################## Parse and Write #########################################

time.sleep(2)
with open(f"whole_foods_products_{STORE_ID}.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "upc", "brand", "slug", "price", "image", "uom", "isLocal", "store"])

    for offset in range(0, total, LIMIT):
        print(f"Fetching offset {offset}...")
        params["offset"] = offset
        resp = requests.get(BASE_URL, params=params)
        data = resp.json()
        results = data.get("results", [])

        for item in results:
            upc = "No UPC available"
            if UPC:
                slug = item.get("slug")
                product = requests.get(f"https://www.wholefoodsmarket.com/api/product/{slug}?store={STORE_ID}").json()
                if product:
                    image_list = product.get("images", [])
                    upc = extract_upc_from_images(image_list)
                    print("UPC: ", upc)
            
            writer.writerow([
                item.get("name"),
                upc,
                item.get("brand"),
                item.get("slug"),
                item.get("regularPrice"),
                item.get("imageThumbnail"),
                item.get("uom", ""),
                item.get("isLocal"),
                item.get("store")
            ])