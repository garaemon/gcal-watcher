#!/usr/bin/env python

from __future__ import print_function

import argparse
import datetime
import json
import logging
import os

from googleapiclient.discovery import build
import httplib2
from oauth2client import client
from oauth2client.file import Storage
from oauth2client import tools
import dateutil.parser

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = os.path.expanduser('~/.config/raspi_home/google_calendar_client_id.json')
APPLICATION_NAME = os.environ['GCAL_WATCHER_GCAL_APPLICATION_NAME']


def get_credentials():
    '''Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    '''
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.raspi-home-secrets/')
    credential_path = os.path.join(credential_dir, 'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if credentials:
        logging.info('You already have credentials')
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        credentials = tools.run_flow(flow, store, flags)
        logging.info('Storing credentials to ' + credential_path)
    return credentials


def verify_client_id():
    'Verify there is client_id.json in ~/.raspi-home-secrets/ directory.'
    if os.path.exists(CLIENT_SECRET_FILE):
        logging.info('Found client secret file at {}'.format(CLIENT_SECRET_FILE))
        return True
    else:
        raise Exception('No client secret file at {}'.format(CLIENT_SECRET_FILE))


class GCalClient(object):
    'Wrapper of google calendar api'

    def __init__(self, calendar_name, calendar_id):
        self.credentials = get_credentials()

        self.calendar_name = calendar_name
        self.calendar_id = calendar_id

    def build_service(self):
        http = self.credentials.authorize(httplib2.Http())
        return build('calendar', 'v3', http=http)

    def get_upcoming_events(self, num):
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        service = self.build_service()
        events_result = service.events().list(
            calendarId=self.calendar_id,
            timeMin=now,
            maxResults=num,
            singleEvents=True,
            orderBy='startTime').execute()
        return events_result.get('items', [])


def remove_ptag(description):
    if description.startswith('<p>'):
        description = description[len('<p>'):]
    if description.endswith('</p>'):
        description = description[:-len('</p>')]
    return description


def parse_start_datetime(event):
    # 2018-01-28T00:05:00+09:00
    event_date_str = event['start']['dateTime']
    return dateutil.parser.parse(event_date_str)


def get_description(event):
    try:
        return json.loads(remove_ptag(event['description']))
    except Exception as e:
        print('Failed to parse', remove_ptag(event['description']))
        raise e


def create_dummy_event(date, description):
    date_str = datetime.datetime.strftime(date, '%Y-%m-%dT%H:%M:%S%z')
    description_str = json.dumps(description)
    return {'description': description_str, 'start': {'dateTime': date_str}}


if __name__ == '__main__':
    # verify_client_id()
    get_credentials()
    gcalclient = GCalClient(os.environ['GCAL_WATCHER_CALENDAR_NAME'],
                            os.environ['GCAL_WATCHER_CALENDAR_ID'])
    for event in gcalclient.get_upcoming_events(10):
        #print(event)
        event_date = parse_start_datetime(event)
        #print(event_date)

        description = remove_ptag(event['description'])
        desc = json.loads(description)
        #print(desc)
        print(event['id'])
