import xml.etree.ElementTree as ET
from pathlib import Path
from fuzzysearch import find_near_matches

from datetime import date, timedelta, datetime

files = ["./data_collection/downloads/IDQ11295.xml", "./data_collection/downloads/IDQ10230.xml"]

file = "./data_collection/downloads/IDQ11295.xml"

query = "Beaudesert"
query = query.translate(str.maketrans({
    "-":  r"\-",
    "]":  r"\]",
    "\\": r"\\",
    "^":  r"\^",
    "$":  r"\$",
    "*":  r"\*",
    ".":  r"\."
}))

with open(file, "r") as f:
    tree = ET.parse(file)

root_main = tree.getroot()[1] # 0th element is amoc

result = root_main.findall(f".area[@description='{query}'][@type='location']")


if len(result[0]) != 8:
    print("error: what?")
    breakpoint()

d1 = {}
d0 = {}

for forecast in result[0]:
    # Within each element, extract the information type, as well as the information
    # Stored in its own dictionary
    for element in forecast:
        print(f"{element.attrib['type']} : {element.text}")
        d0[element.attrib['type']] = element.text
    breakpoint()

    _date = datetime.fromisoformat(forecast.attrib["start-time-local"]).strftime(r"%Y-%m-%d")

    d1[_date] = d0
    d0 = {}

breakpoint()
    
    





# for file in files:
#     path = Path(file).resolve()
#     with open(path, "r") as f:
#         tree = ET.parse(path)
#         root = tree.getroot()[1]
#         breakpoint()

# root.findall("./forecast/area[@description='Stanthorpe']")

# finding icon meanings in data: http://www.bom.gov.au/catalogue/adfdUserGuide.pdf