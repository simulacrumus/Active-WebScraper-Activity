import requests
from bs4 import BeautifulSoup
import re
from util import *

RESERVATION_BASE_URL='https://reservation.frontdesksuite.ca/'
SUBMISSION_URL_SUFFIX = "/ReserveTime/SubmitSlotCount?culture=en"
SUBMISSION_URL_PREFIX = "rcfs/"
RESERVATION_BASE_URL='https://reservation.frontdesksuite.ca/'
BASE_URL = "https://ottawa.ca"

# Scrape all activity titles from facility's reservation page
def scrape_activity_titles(url:str):
    print("scraping activity titles for URL: " + url)
    try:
        activity_titles = []
        session = requests.Session()
        response = session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        activities = soup.find_all("div", {"class":"content"})
        if activities is not None:
            for activity in activities:
                if activity is not None:
                    a = activity.string
                    activity_titles.append(a)
        return activity_titles
    except(ConnectionError, Exception) as e:
        print(e)

# Scrape active times and availibility for an activity
def scrape_activity_details(url, activity_title, submission_link):
    try:
        times_and_availibility = []
        session = requests.Session()
        response = session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        activity_url = soup.find("div", string=re.compile(activity_title)).parent.attrs.get('href')
        response = session.get(url=RESERVATION_BASE_URL+activity_url)
        soup = BeautifulSoup(response.text, "html.parser")
        form_data_tags = soup.find_all("input", {"type" : "hidden"})
        form_data = {}
        for tag in form_data_tags:
            form_data[tag.get('name')] = tag.get("value")
        response = session.post(url=RESERVATION_BASE_URL+submission_link, data=form_data)
        soup = BeautifulSoup(response.text, "html.parser")
        time_tags = soup.find_all("a", {"class":"time-container"})
        for tag in time_tags:
            times_and_availibility.append({
                "time":tag.get('aria-label'),
                "available": tag.get("onclick") != "return false;"
            })
        return times_and_availibility
    except(ConnectionError, Exception) as e:
        print(e)