import xml.etree.ElementTree as ET
from pathlib import Path

from datetime import datetime
import logging

logger = logging.getLogger(__name__)

files = ["./data_collection/downloads/IDQ11295.xml", "./data_collection/downloads/IDQ10230.xml"]

# file = "./data_collection/downloads/IDQ11295.xml"

query = "Stanthorpe"
query = query.translate(str.maketrans({
    "-":  r"\-",
    "]":  r"\]",
    "\\": r"\\",
    "^":  r"\^",
    "$":  r"\$",
    "*":  r"\*",
    ".":  r"\."
}))

values = {}

for file in files:

    with open(file, "r") as f:
        tree = ET.parse(file)

    root_main = tree.getroot()[1] # 0th element is amoc

    result = root_main.findall(f".area[@description='{query}'][@type='location']")

    if not result:
        logger.warning(f"File {file[-12:]} could not find results for {query}, skipping")
        continue
    if len(result[0]) != 8:
        logger.warning(f"Filer  {file[-12:]} does not have all the required information, skipping")
        continue

    d1 = {}
    d0 = {}

    for forecast in result[0]:
        # Within each element, extract the information type, as well as the information
        # Stored in its own dictionary
        for element in forecast:
            print(f"{element.attrib['type']} : {element.text}")
            d0[element.attrib['type']] = element.text

        _date = datetime.fromisoformat(forecast.attrib["start-time-local"]).strftime(r"%Y-%m-%d")

        d1[_date] = d0
        d0 = {}
    values[file[-12:]] = d1

breakpoint()
    





# for file in files:
#     path = Path(file).resolve()
#     with open(path, "r") as f:
#         tree = ET.parse(path)
#         root = tree.getroot()[1]
#         breakpoint()

# root.findall("./forecast/area[@description='Stanthorpe']")

# finding icon meanings in data: http://www.bom.gov.au/catalogue/adfdUserGuide.pdf