from builder import build_activities_for_facility_reservation
from util import get_json_data
import schedule
import time
import requests
import logging
from os import environ as env

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

def run():
    try:
        URL = 'http://{HOST}:{PORT}/api/v1/activities/all?key={API_KEY}'.format(
            HOST = env['SERVER_HOST'],
            PORT = env['SERVER_PORT'],
            API_KEY = env['API_KEY']
        )
        logging.info('API URL created')
        facilities = get_json_data('facilities.json')
        activities = []
        for facility in facilities:
            reservations = facility['reservations']
            for reservation in reservations:
                activities_for_facility = build_activities_for_facility_reservation(reservation)
                activities += activities_for_facility
        response = requests.post(url=URL, json=activities)
        if response.ok:
            logging.info('Activities successfully transferred')
        else:
            logging.warning('Activities could not transferred')
    except(ConnectionError, Exception) as e:
        logging.error('Something went wrong with the scraper app')
        logging.error(e)

if __name__ == '__main__':
    logging.info('Starting Python Web Scraper..')
    schedule.every().hour.at(":01").do(run)
    schedule.every().hour.at(":15").do(run)
    schedule.every().hour.at(":30").do(run)
    schedule.every().hour.at(":45").do(run)
    while 1:
        schedule.run_pending()
        time.sleep(1)