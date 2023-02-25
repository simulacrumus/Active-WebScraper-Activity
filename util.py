from datetime import datetime
import json
import re

# Convert string to date object 
# <8:00 PM Friday October 21, 2022> to <2022-10-21 20:00:00>
def string_to_datetime(datetime_str:str):
    return datetime.strptime(datetime_str, '%I:%M %p %A %B %d, %Y').strftime('%Y-%m-%dT%H:%M:%S.%f')

def get_json_data(file):
    with open(file) as json_file:
        return json.load(json_file)

def write_json_data(data, filename):
    with open(filename, 'w') as outfile:
                json.dump(data, outfile)

def string_to_num(str:str):
    return int(filter(str.isdigit, str))

def remove_duplicates_from_list(list:list):
    return [*set(list)]

# Strip longitude from Google Maps URI
def google_maps_url_to_longitude(google_maps_url:str):
    i = re.search("45.", google_maps_url).start()
    return google_maps_url[i:i+10]

# Strip latitude from Google Maps URI
def google_maps_url_to_latitude(google_maps_url:str):
    i = re.search("-75", google_maps_url).start()
    return google_maps_url[i:i+11]

# Get only phone number part from phone string. 
# Some phone numbers include extension, html elements or unnecessary words.
def get_phone_from_string(str:str):
    index = str.find("613")
    if index != -1:
        return str[index:index+12]
    else: return str