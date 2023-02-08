from builder import build_activities_for_facility_reservation
from util import get_json_data
import schedule
import time
import requests

def run():
    try:
        facilities = get_json_data('facilities.json')
        activities = []
        for facility in facilities:
            reservations = facility['reservations']
            for reservation in reservations:
                activities_for_facility = build_activities_for_facility_reservation(reservation)
                activities += activities_for_facility
        response = requests.post(url="http://localhost:8080/api/v1/activities/all?key=YOUR_API_KEY", json=activities)
        if response.ok:
            print("\nActivities successfully transferred\n")
        else:
            print("\nActivities could not transferred\n")
    except(ConnectionError, Exception) as e:
        print(e)

if __name__ == '__main__':
    schedule.every().hour.at(":05").do(run)
    schedule.every().hour.at(":35").do(run)
    while 1:
        schedule.run_pending()
        time.sleep(1)