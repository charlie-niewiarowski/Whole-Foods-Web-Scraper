########################################  Deps ###########################################  

import requests
import csv
import time

######################################## Configure ######################################## 

STORE_ID = int(input("Store ID: "))
SUMMARY_URL = f"https://www.wholefoodsmarket.com/stores/{STORE_ID}/summary"
response = requests.get(SUMMARY_URL)
if response.json() is None:
    print(f"Store {STORE_ID} is invalid or inactive.")
    exit()


WANTSID = False
res = input("Do you want to know the product ID? (Y/N) | Warning: This will reduce speeds | : ")
if res.lower() == "y":
    WANTSID = True

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
    writer.writerow(["id", "name", "brand", "slug", "price", "image", "uom", "isLocal", "store"])

    for offset in range(0, total, LIMIT):
        print(f"Fetching items {offset}-{offset + LIMIT}...")
        params["offset"] = offset
        resp = requests.get(BASE_URL, params=params)
        data = resp.json()
        results = data.get("results", [])

        for item in results:
            id = "None"
            if WANTSID:
                slug = item.get("slug")
                product = requests.get(f"https://www.wholefoodsmarket.com/api/product/{slug}?store={STORE_ID}").json()
                if product:
                    id = (product.get("id", "")).strip("[]")
            
            writer.writerow([
                id,
                item.get("name"),
                item.get("brand"),
                item.get("slug"),
                item.get("regularPrice"),
                item.get("imageThumbnail"),
                item.get("uom", ""),
                item.get("isLocal"),
                item.get("store")
            ])