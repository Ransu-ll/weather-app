import pytest
from webapp import LocationInfoDownloader as lid
import os
from pathlib import Path
import shutil


def test_getting_associated_town_files():
    # Tests that should always pass
    assert lid.get_town_files("Melbourne, VIC") == "IDV10450"
    assert lid.get_town_files("Hughenden, QLD") == "IDQ11295,IDQ10130"

    # Tests that should always raise an error
    with pytest.raises(KeyError):
        lid.get_town_files("melbourne, vic")
        lid.get_town_files(".\\sdjsds")
        lid.get_town_files(1)
        lid.get_town_files(None)

def test_downloader():

    temp_downloads = Path(__file__).parent / "temp"
    temp_downloads = temp_downloads.resolve()

    # create directory if it does not exist
    if temp_downloads.exists() is False:
        os.mkdir(str(temp_downloads))

    files_pass = ["IDV10450.xml", "IDQ11295.xml", "IDQ10130.xml"]

    for file in files_pass:
        assert lid.download_file_from_bom(temp_downloads, file) == 0
    
    files_fail = [1, 2, "..", "12-s.xml"]

    for file in files_fail:
        assert lid.download_file_from_bom(temp_downloads, file) == 1

    # remove directory and all its contents
    shutil.rmtree(temp_downloads)