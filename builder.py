from scraper import *
import datetime

BASE_URL='https://reservation.frontdesksuite.ca/'
SUBMISSION_URL_SUFFIX = "/ReserveTime/SubmitSlotCount?culture=en"
SUBMISSION_URL_PREFIX = "rcfs/"

def build_activities_for_facility_reservation(facility_reservation):
    activities = []
    reservation_page_url = BASE_URL + SUBMISSION_URL_PREFIX + facility_reservation
    activity_titles = scrape_activity_titles(reservation_page_url)
    print(activity_titles)
    for activity_title in activity_titles:
        title = activity_title
        submission_link = "/"+SUBMISSION_URL_PREFIX+facility_reservation+SUBMISSION_URL_SUFFIX
        activity_details = scrape_activity_details(reservation_page_url, activity_title, submission_link)
        try:
            for activity_detail in activity_details:
                activity = {
                    "facilityReservation": facility_reservation,
                    "title": title.strip().lower().replace("–", "-").replace("’", "'"),
                    "time": string_to_datetime(activity_detail["time"]),
                    "isAvailable": activity_detail["available"],
                    "lastUpdated": datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
                }
                activities.append(activity)
        except(Exception) as e:
            print(e)
    return activities;