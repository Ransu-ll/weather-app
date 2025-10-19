from pathlib import Path
import json
import logging
import os
from ftplib import FTP
import time
import xml.etree.ElementTree as ET
from datetime import datetime

from typing import Union

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def get_town_files(location: str) -> Union[str, None]:
    """Gets town information based on the specified location"""

    # Get location of the file
    file_mappings_location = Path(__file__).parent.resolve() / "data/mappings_finalised.json"
    file_mappings_location = file_mappings_location.resolve()

    if file_mappings_location.exists() is False:
        logger.critical(f"Could not find the mappings file at the specified location:\n{file_mappings_location}")
        return None
    
    with open(file_mappings_location, "r") as f:
        mapping = json.load(f)

    return mapping[location]["ids"]

def download_file_from_bom(location: Path, name: Path) -> int:
    """Downloads a file from within the fwo directory of the BOM"""
    
    ftp = FTP("ftp.bom.gov.au")
    response = ftp.login()

    if response[:3] != "230":
        logger.critical(f"Received response other than a successful login. Message:\n{response}")
        return 1

    try:
        with open(Path(location / name).resolve(), "wb") as f:
            ftp.retrbinary(f"RETR /anon/gen/fwo/{name}", f.write)

        logger.info(f"Downloaded the file {name} to {location / name}")
        return 0
    except Exception as e:
        logger.critical(f"Could not save the file {name} in the FTP server. Reason:\n{e}")
        return 1
    

def download_town_files(files: str) -> list[str]:
    """Downloads specified files from the BOM from a list of IDs"""
    individual_files = files.split(",")

    
    file_path = Path(Path(__file__).parent, "webapp_downloads")

    if file_path.exists() is False:
        os.makedirs(file_path)

    results = []

    for file in individual_files:
        file_name = Path(file + ".xml")

        full_filepath = file_path / file_name
        full_filepath = full_filepath.resolve()

        if full_filepath.exists() is False:
            logger.info(f"Downloading file {file}.xml due to it not existing yet.")
            download_file_from_bom(file_path, file_name)
            results.append(full_filepath)

        else:
            last_modified = os.path.getmtime(full_filepath)
            diff = time.time() - last_modified

            threshold = 1*60*10 # 10 minutes

            if diff > threshold:
                logger.info(f"Downloading file {file}.xml due to it existing but being too old.")
                download_file_from_bom(file_path, file_name)
                results.append(full_filepath)
            else:
                logger.info(f"Not updating the file {file} due to it being too new.")
                results.append(full_filepath)
    
    return results

def parse_file_for_location(file_location: Path, town: str) -> dict:
    """Parses a single file, looking for information on a specific town"""

    with open(file_location, "r") as f:
        tree = ET.parse(f)

    root_main = tree.getroot()[1] # 0th element is amoc

    result = root_main.findall(f".area[@description='{town}'][@type='location']")
    if not result:
        logger.warning(f"File {str(file_location)[-12:]} could not find results for {town}, skipping")
        return None

    if len(result[0]) < 7: # data can be sometimes seven or 8
        logger.warning(f"File {str(file_location)[-12:]} does not have all the required information, skipping")
        return None


    d1 = {}
    d0 = {}

    for forecast in result[0]:
        # Within each element, extract the information type, as well as the information
        # Stored in its own dictionary
        for element in forecast:
            if element.attrib['type'] == "forecast_icon_code":
                # add the extension for the image
                d0[element.attrib['type']] = element.text + ".png"
            else:
                d0[element.attrib['type']] = element.text
            

        _date = datetime.fromisoformat(forecast.attrib["start-time-local"]).strftime(r"%Y-%m-%d")

        d1[_date] = d0
        d0 = {}
    
    return d1

def get_town_info(files_locations: list[Path], town: str) -> Union[dict, None]:
    """Get the forecast information given a specific list of files """
    
    town_query = town.split(", ")[0]

    # If the results aren't in one file, they are in another file.
    for file in files_locations:
        result = parse_file_for_location(str(file), town_query)
        if result is None:
            continue
        return result
    
    logger.error(f"Could not find information about {town} in files: \n{"\n".join(files_locations)}")

def retreive_town_info(location: str):
    town_files = get_town_files(location)
    town_files_file_locations = download_town_files(town_files)
    return get_town_info(town_files_file_locations, location)

# Example usecase: 
# if __name__ == "__main__":
#     location = "Melbourne, VIC"
#     town_files = get_town_files(location)
#     town_files_locations = download_town_files(town_files)
#     from pprint import pprint
#     pprint(get_town_info(town_files_locations, location))
    
