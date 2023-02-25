import requests
from bs4 import BeautifulSoup
import re
from util import *
import logging
import os

RESERVATION_BASE_URL='https://reservation.frontdesksuite.ca/'
SUBMISSION_URL_SUFFIX = "/ReserveTime/SubmitSlotCount?culture=en"
SUBMISSION_URL_PREFIX = "rcfs/"
BASE_URL = "https://ottawa.ca"
FACILITIES_LIST_BASE_URL = "https://ottawa.ca/en/recreation-and-parks/recreation-facilities/place-listing?text=&page="
BASE_URL = "https://ottawa.ca"
NUM_OF_PAGES = 4 # Number of pages for facilities list

# Scrape all activity titles from facility's reservation page
def scrape_activity_titles(url:str):
    logging.info("Scraping activity titles for URL: " + url)
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
        logging.warning('Could not scrape activities for url: {}'.format(url))
        logging.warning(e)

# Scrape active times and availibility for an activity
def scrape_activity_details(url, activity_title, submission_link):
    try:
        times_and_availibility = []
        session = requests.Session()
        response = session.get(url=url)
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
                # "available": "reserved" not in tag.parent.attrs.get('class')
                "available": tag.get("onclick") != "return false;"
            })
        return times_and_availibility
    except(ConnectionError, Exception) as e:
        logging.warning('{} does not have any scheduled availability'.format(activity_title))
        logging.warning(e)

# Scrape all facilities from facilities pages
def scrape_all_facilities():
    logging.info('Scraping facilities..')
    all_facilities = []
    for i in range(NUM_OF_PAGES):
        url = FACILITIES_LIST_BASE_URL + str(i)
        facilities_for_url = scrape_facilities(url)
        for facility in facilities_for_url:
            all_facilities.append(facility)
    return all_facilities

# Scrape facilities information from list of facilities page
def scrape_facilities(url:str):
    try:
        facilities = []
        session = requests.Session()
        response = session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        facility_list = soup.find("tbody").find_all("tr")
        for facility in facility_list:
            fc = {}
            fc["url"] = BASE_URL+facility.find("a").attrs.get("href")
            fc["title"] = facility.find("a").string
            fc["address"] = ""
            address_fields = facility.find("p", {"class":"address"}).find_all("span")
            for field in address_fields:
                fc["address"] += field.string+" "
            fc["address"] = fc["address"].strip()
            facilities.append(fc)
        return facilities
    except(ConnectionError, Exception) as e:
        logging.warning(e)

# Scrape facility details from facility's home page
def scrape_facility_details(url:str):
    logging.info('Scraping details from ' + url)
    try:
        facility = {}
        session = requests.Session()
        response = session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        phone = soup.find(text=re.compile('613'))
        facility["phone"] = get_phone_from_string(phone)
        email = soup.find("a", {"href":re.compile('mailto')})
        if email is not None:
            email = email.string
            if email is not None: email = email.lower()
        facility["email"] = email
        reservation_links = soup.find_all("a", text=re.compile("Reserve a spot"))
        reservations = []
        for rl in reservation_links:
            reservations.append(os.path.basename(os.path.normpath(rl.attrs.get("href"))))
        facility["reservations"] = remove_duplicates_from_list(reservations)
        return facility
    except(ConnectionError, Exception) as e:
        logging.warning(e)

# Scrape facility information from facility's reservation page
def scrape_facility_info(facility_reservation):
    logging.info('Scraping facilitiy information for '+facility_reservation)
    try:
        facility ={}
        session = requests.Session()
        url = RESERVATION_BASE_URL+SUBMISSION_URL_PREFIX+facility_reservation
        facility["url"] = url
        response = session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        facility_title = soup.find("span", {"class":"mdc-top-app-bar__title"})
        if(facility_title is not None): facility_title = facility_title.string
        facility["title"] = facility_title
        facility["phone"] = soup.find(text=re.compile('613'))
        google_maps_url = soup.find("a", {"href":re.compile('google')})
        if(google_maps_url is not None): google_maps_url = google_maps_url.attrs.get("href")
        facility["google_maps_url"] = google_maps_url
        street = soup.find("div", {"class":"thoroughfare"})
        if(street is not None): street = street.string
        city = "Ottawa"
        province = "ON"
        postal_code = soup.find("span", {"class":"postal-code"})
        if(postal_code is not None): postal_code = postal_code.string
        facility["address"] = "% s % s, % s % s" % (street, city, province, postal_code)
        facility["reservation"]=facility_reservation
        if(google_maps_url is not None):
            facility["longitude"] = google_maps_url_to_longitude(google_maps_url)
            facility["latitude"] = google_maps_url_to_latitude(google_maps_url)
        else:
            facility["longitude"] = None
            facility["latitude"] = None
        return facility
    except(ConnectionError, Exception) as e:
        logging.warning(e)