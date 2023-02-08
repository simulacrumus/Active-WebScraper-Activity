from datetime import datetime
import json

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