from ftplib import FTP
import re
from pathlib import Path

ftp = FTP("ftp.bom.gov.au")
ftp.login()
files = ftp.nlst("/anon/gen/fwo/")
pattern = re.compile(r"\/anon\/gen\/fwo\/ID[DNQSTVW]\d{5}\.xml")

files = [file for file in files if pattern.match(file)]

for file in files:
    destination = Path("./data_collection/downloads") / Path(file).name
    with open(destination, "wb") as downloaded_file:
        ftp.retrbinary(f"RETR {file}", downloaded_file.write)
