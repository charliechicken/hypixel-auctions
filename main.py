import grequests
import json
from pprint import pprint
import time
import pyautogui
import os
import pyperclip
import sys
from plyer import notification
import beepy
from colorama import Fore, Back, Style
val = input("What Item do you want to search for?")
stars = input("How many stars does this item have? (0 - 5)")

#Figure out how do make a while loop here
if stars == "0":
    stars = ""
    val = val + " " + stars
if stars == "1":
    stars = "✪"
    val = val + " " + stars
elif stars == "2":
    stars = "✪✪"
    val = val + " " + stars
elif stars == "3":
    stars = "✪✪✪"
    val = val + " " + stars
elif stars == "4":
    stars = "✪✪✪✪"
    val = val + " " + stars
elif stars == "5":
    stars = "✪✪✪✪✪"
    val = val + " " + stars
else:
    stars = input("Not a number 0 - 5. Enter again.")

print(stars)
tier1 = input("What tier (EPIC, LEGENDARY, MYTHIC, etc...)")
tier2 = tier1.upper()
price = input("What is the maximum price to be searched for?")

auc_requirements = {
                    val : {"item_name": val, "tier": tier2, "category": "", "price": int(price)}
                    }

#enter api key in ""
API_KEY = ""

data = {}
auction_final = []
auction_final_cheapest = {}
auction_final_cheapest_sorted = []

start_time = time.time()

url_base = f"https://api.hypixel.net/skyblock/auctions?key={API_KEY}"
url_base_bazaar = f"https://api.hypixel.net/skyblock/bazaar?key={API_KEY}"

def checkAuctionItem(auction_item):
    if auction_item["bin"] != True:
        return (False, "Not BIN")
    if(auction_item["claimed"] == True):
        return (False, "Already claimed")
    for id in auc_requirements:
        valid = True
        for req in auc_requirements[id]:
            if(req != "price"):
                if(auc_requirements[id][req] not in auction_item[req]):
                    valid = False
                    break
        if(valid):
            if(auction_item["starting_bid"] < auc_requirements[id]["price"]):
                dashed_uuid = auction_item['uuid'][:8] + '-' + auction_item['uuid'][8:12] + '-' + auction_item['uuid'][12:16]
                dashed_uuid += '-' + auction_item['uuid'][16:20] + '-' + auction_item['uuid'][20:]
                return (True, (id, f"/viewauction {dashed_uuid}", auction_item['starting_bid'], auction_item["item_name"]), auction_item["item_lore"])
    return (False, "Not all requirements met")

resp = grequests.get(url_base)
resp2 = grequests.get(url_base_bazaar)

for res in grequests.map([resp]):
    data = json.loads(res.content)
    total_pages = data['totalPages']
    print(f"Total Pages found: {data['totalPages']}")


    if(data["success"]):
        for auction_item in data["auctions"]:
            try:
                item_ans = checkAuctionItem(auction_item)
                if(item_ans[0]):
                    auction_final.append(item_ans[1])
                else:
                    pass
            except:
                hi = "hi";
    else:
        print(f"Failed GET request: {data['cause']}")

priceOfRecomb = 0
priceOfUltWise5 = 0
for res in grequests.map([resp2]):
    data = json.loads(res.content)
    for bz_item, bz_data in data.get("products", {}).items():
        if bz_item == "RECOMBOBULATOR_3000":
            priceOfRecomb = bz_data['sell_summary'][1]['pricePerUnit']
        if bz_item == "ULTIMATE_WISE_5":
            priceOfUltWise5 = bz_data['sell_summary'][1]['pricePerUnit']

first_page_time = time.time()

urls = []
for page_count in range(1, total_pages+1):
    urls.append(f"{url_base}&page={page_count}")

resp = (grequests.get(url) for url in urls)

made_requests_time = time.time()

for res in grequests.map(resp):
    data = json.loads(res.content)

    if(data["success"]):
        for auction_item in data["auctions"]:
            try:
                item_ans = checkAuctionItem(auction_item)
                if(item_ans[0]):
                    auction_final.append(item_ans[1])
                else:
                    pass
            except:
                hi = "hi"

    else:
        print(f"Failed GET request: {data['cause']}")

print(f"{len(auction_final)} items found")
auction_final = sorted(auction_final, key=lambda x: (x[0], x[2]))


#all auctions
pprint(auction_final)

#num = priceOfRecomb + auction_final[0][2]
#print(f"Total Cost: {num:,}")

#copies to clipboard -- dont use this, throws weird errors
#pyperclip.copy(auction_final[0][1])
