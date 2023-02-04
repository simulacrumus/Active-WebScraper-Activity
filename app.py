from builder import build_activities_for_facility_reservation, build_active_facilities
from util import get_json_data
import json

def run():
    facilities = get_json_data('facilities.json')
    activities = []
    for facility in facilities:
        reservations = facility['reservations']
        for reservation in reservations:
            activities_for_facility = build_activities_for_facility_reservation(reservation)
            activities += activities_for_facility
    with open('available_activities.json', 'w') as outfile:
                json.dump(activities, outfile)

if __name__ == '__main__':
    run()