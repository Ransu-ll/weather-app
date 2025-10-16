import json

with open("./data_collection/mappings_old.json", "r") as f1:
    data = json.load(f1)

towns = {}

for entry in data:
    towns[entry["name"]] = {"link": entry["link"], "ids": entry["ids"]}

with open("./data_collection/mappings_finalised.json", "w") as f2:
    json.dump(towns, f2, indent=4)