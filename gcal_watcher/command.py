import datetime
from threading import Thread
import json

import requests


class CommandException(Exception):
    pass


class Command(object):
    REQUIRED_FIELDS = ['method', 'url']

    def __init__(self, json_object, event_date):
        Command.verify_fields(json_object)
        self.is_started = False
        self.method = json_object['method']
        self.url = Command.replace_vars(json_object['url'], event_date)
        self.params = dict()
        self.json_object = json_object
        self.event_date = event_date
        if 'params' in json_object:
            for key in json_object['params']:
                self.params[key] = Command.replace_vars(json_object['params'][key], event_date)

    def invoke(self):
        print('invoked!', self.json_object)
        self.thread = Thread(target=self.invoke_thread)
        self.thread.daemon = True
        self.thread.run()
        self.is_started = True

    def invoke_thread(self):
        try:
            if self.method.upper() == 'GET':
                res = requests.get(self.url)
            elif self.method.upper() == 'POST':
                res = requests.post(
                    self.url, json.dumps(self.params), headers={
                        'Content-Type': 'application/json'
                    })
        except Exception as e:
            print('Failed to execute command', self.json_object)
        print('Done')

    def __eq__(self, other):
        return (self.method == other.method and self.url == other.url and
                self.params == other.params)

    @classmethod
    def verify_fields(cls, obj):
        for field in cls.REQUIRED_FIELDS:
            if field not in obj:
                raise CommandException('no {} is specified'.format(field))
        return True

    @classmethod
    def replace_vars(_cls, string, event_date):
        today = event_date
        yesterday = event_date + datetime.timedelta(days=-1)
        tomorrow = event_date + datetime.timedelta(days=1)
        replace_rules = {
            '${today.year}': '%04d' % today.year,
            '${today.month}': '%02d' % today.month,
            '${today.day}': '%02d' % today.day,
            '${yesterday.year}': '%04d' % yesterday.year,
            '${yesterday.month}': '%02d' % yesterday.month,
            '${yesterday.day}': '%02d' % yesterday.day,
            '${tomorrow.year}': '%04d' % tomorrow.year,
            '${tomorrow.month}': '%02d' % tomorrow.month,
            '${tomorrow.day}': '%02d' % tomorrow.day,
        }
        for from_string, to_string in replace_rules.items():
            string = string.replace(from_string, to_string)
        return string


def main():
    command = Command({
        'method': 'GET',
        'url': 'http://localhost:8000',
    }, datetime.datetime.now())
    command.invoke()


if __name__ == '__main__':
    main()

#
# {"method": "POST",
#  "url": "http://localhost:5000/record",
#  "params": {
#    "station_id": "TBS",
#    "start_date": "${today.year}-${today.month}-${today.day}-22-00",
#    "artist": "Foo",
#    "album": "Foo-album",
#    "title": "Foo-${today.year}-${today.month}-${today.day}"
#   }
# }
