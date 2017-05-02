import os
import time
import requests
import shutil
from pathlib import Path

# setup
folder = '9' # setup folder name - use term number
if not os.path.exists(folder):
    os.makedirs(folder)

file_type = 'jpg' # assume all file type - use jpg
csv = 'http://data.ly.gov.tw/odw/usageFile.action?id=9&type=CSV&fname=9_CSV.csv' # list of legislators

# get data
response = requests.get(csv)
rows = response.text.split("\n")
name_is_at = 0
photo_url_is_at = 0
for index, row in enumerate(rows):
    if ',' in row:
        cols = row.split(',')
        if index == 0: # find the name and photo URL column
            name_is_at = cols.index('name')
            photo_url_is_at = cols.index('picUrl')
        else:
            name = cols[name_is_at]
            photo_url = cols[photo_url_is_at]
            file_name = folder + '/' + name + '.' + file_type
            print(index, file_name)

            file = Path(file_name)
            if file.is_file() == False:
                response = requests.get(photo_url, stream=True)
                with open(file_name, 'wb') as output:
                    shutil.copyfileobj(response.raw, output)
                time.sleep(5)
del response
