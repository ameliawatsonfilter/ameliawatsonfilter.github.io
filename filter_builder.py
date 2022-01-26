# Use 4chan's API to build a large filter of images containing Amelia Watson,
# by scraping the Amelia Watson split thread for image MD5 hashes.
#
# Best used run at a regular interval through cron jobs on Linux or task scheduler
# on Windows.

import requests
import json
import re
import time
import os


def get_catalog_and_search_for_thread():
    r_catalog = requests.get("https://a.4cdn.org/vt/catalog.json")
    if not r_catalog.status_code == 200:
        print("Error: could not retrieve the catalog from 4chan's API endpoint!")
        exit(-1)
    else:
        print("Retrieved the /vt/ catalog.")

    target_thread_no = None
    j_catalog = r_catalog.json()
    for page in j_catalog:
        for thread in page["threads"]:
            if "com" not in thread.keys():
                break
            comment = thread["com"].lower()
            pattern = re.compile("amelia\swatson\sappreciation")
            if pattern.match(comment):
                target_thread_no = thread["no"]

    return target_thread_no


max_attempts = 5
delay_between_attempts = 1
for i in range(max_attempts):
    target_thread_no = get_catalog_and_search_for_thread()
    if target_thread_no:
        print(f"Hit thread no. {target_thread_no}, next request will retrieve posts...")
        break
    else:
        print(
            f"Couldn't find matching thread, trying again in {delay_between_attempts} minutes..."
        )
        time.sleep(delay_between_attempts * 60)

if not target_thread_no:
    print("Couldn't find the thread to scrape for MD5 hashes, exiting.")
    exit(-1)

# 4chan API does not allow more than 1 request per second
time.sleep(1.0)

md5s = []
r_thread = requests.get(f"https://a.4cdn.org/vt/thread/{target_thread_no}.json")
j_thread = r_thread.json()
for post in j_thread["posts"]:
    if "md5" in post.keys():
        md5s.append(f'/{post["md5"]}/')

print(f"Hit {len(md5s)} suspected Amelia Watson images.")
print(f"Opening filter.txt to write them...")
mode = "r+" if os.path.exists("filter.txt") else "w"
if mode == "r+":
    with open("filter.txt", mode=mode) as filterfile:
        filterlines = filterfile.readlines()
else:
    filterlines = []

with open("filter.txt", mode=mode) as filterfile:
    for existing_filterline in filterlines:
        for md5 in md5s:
            md5_filterline = f"{md5}\n"
            if md5_filterline == existing_filterline:
                md5s.remove(md5)
                break
        filterfile.write(existing_filterline)
    for md5 in md5s:
        md5_filterline = f"{md5}\n"
        filterfile.write(md5_filterline)


print(f"Wrote {len(md5s)} new suspected Amelia Watson images to filter.")
