import json

with open("./data_collection/mappings_finalised.json", "r") as f:
    data = json.load(f)

with open("./data_collection/towns.txt", "w") as f:
    for i, town in enumerate(list(data.keys())):
        f.write(f"{town}")
        
        if i != len(list(data.keys())) - 1:
            # do not write a new line on the last line
            f.write("\n")