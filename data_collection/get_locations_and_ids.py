from bs4 import BeautifulSoup
from selenium import webdriver
import re
from time import sleep
import json

driver = webdriver.Firefox()

locations_info = []
pattern_product = re.compile(r"ID[DNQSTVW]\d{5}")

states = ["tas", "vic", "sa", "wa", "nt", "qld", "nsw"] # excluding ACT since that's part of nsw according to the BoM

for state in states:
    print("Current State: ", state)
    sleep(1.5)
    driver.get(f"http://www.bom.gov.au/{state}/forecasts/towns.shtml")

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # For each available location in the towns page,
    # create an entry with the name of the town (and its state)
    # and the link to it
    for tag in soup.select("td:has(a)"):

        # Interestingly, ACT is part of NSW so we need to make an exception
        # for ACT areas.
        if tag.text.strip() in ["Belconnen", "Gungahlin", "Woden Valley", "Canberra", "Tuggeranong", "Mount Ginini"]: 
            state_location = "ACT"
        else:
            state_location = state.upper()

        locations_info.append({
            "name": tag.text.strip() + f", {state_location}",
            "link": "http://www.bom.gov.au" + tag.find("a")["href"]
        })


# furthermore, for each location in the towns page,
# find the associated product IDs
for i in range(len(locations_info)):
    sleep(1.5)
    driver.get(locations_info[i]["link"])
    soup = BeautifulSoup(driver.page_source, "html.parser")

    ids = soup.find_all("p", class_="p-id")[0].text
    ids = pattern_product.findall(ids)

    locations_info[i]["ids"] = ",".join(ids)

with open("mappings.json", "w") as f:
    json.dump(locations_info, f, indent=4)

driver.quit()