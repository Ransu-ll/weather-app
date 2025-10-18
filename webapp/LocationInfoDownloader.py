from pathlib import Path
import json
import logging
import os
from ftplib import FTP
import time

from typing import Union

logger = logging.getLogger(__name__)

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
    

def download_town_files(files: str):
    """Downloads specified files from the BOM from a list of IDs"""
    individual_files = files.split(",")

    
    file_path = Path(Path(__file__).parent, "webapp_downloads")

    if file_path.exists() is False:
        os.makedirs(file_path)

    for file in individual_files:
        file_name = Path(file + ".xml")

        full_filepath = file_path / file_name
        full_filepath = full_filepath.resolve()

        if full_filepath.exists() is False:
            logger.info(f"Downloading file {file}.xml due to it not existing yet.")
            download_file_from_bom(file_path, file_name)
            pass

        else:
            last_modified = os.path.getmtime(full_filepath)
            diff = time.time() - last_modified

            threshold = 1*60*10 # 10 minutes

            if diff > threshold:
                pass
                download_file_from_bom(file_path, file_name)

# Example usecase: 
if __name__ == "__main__":
    location = "Penguin, TAS"
    files = get_town_files("Penguin, TAS")
    download_town_files(files)
