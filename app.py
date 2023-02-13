from builder import build_activities_for_facility_reservation
from util import get_json_data
import schedule
import time
import requests
from os import environ as env

def run():
    try:
        URL = 'http://{HOST}:{PORT}/api/v1/activities/all?key={API_KEY}'.format(
            HOST = env['SERVER_HOST'],
            PORT = env['SERVER_PORT'],
            API_KEY = env['API_KEY']
        )
        facilities = get_json_data('facilities.json')
        activities = []
        for facility in facilities:
            reservations = facility['reservations']
            for reservation in reservations:
                activities_for_facility = build_activities_for_facility_reservation(reservation)
                activities += activities_for_facility
        response = requests.post(url=URL, json=activities)
        if response.ok:
            print("\nActivities successfully transferred\n")
        else:
            print("\nActivities could not transferred\n")
    except(ConnectionError, Exception) as e:
        print(e)

if __name__ == '__main__':
    print("Starting Python Web Scraper..")
    schedule.every().hour.at(":01").do(run)
    schedule.every().hour.at(":15").do(run)
    schedule.every().hour.at(":30").do(run)
    schedule.every().hour.at(":45").do(run)
    while 1:
        schedule.run_pending()
        time.sleep(1)