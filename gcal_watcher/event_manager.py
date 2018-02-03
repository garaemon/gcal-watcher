import json
from threading import Lock, Thread
import time
import datetime

from .googlecalendar import (parse_start_datetime, get_description, create_dummy_event)
from .command import Command


class EventManager(object):
    SLEEP_DURATION_SEC = 60

    def __init__(self):
        self.lock = Lock()
        self.events = []

    def run(self):
        self.thread = Thread(target=self.run_thread)
        self.thread.daemon = True
        self.thread.start()

    def run_thread(self):
        while True:
            self.tick()
            time.sleep(self.SLEEP_DURATION_SEC)

    def tick(self):
        print('running tick')
        with self.lock:
            for event in self.events:
                now = datetime.datetime.now(event.event_date.tzinfo)
                if not event.is_started and event.event_date < now:
                    event.invoke()
            # remove 'started' event from `self.events`
            self.events = [e for e in self.events if e.is_started is False]
            print('Left %d events' % len(self.events))

    def add(self, events):
        for event in events:
            event_date = parse_start_datetime(event)
            desc_json = get_description(event)
            command = Command(desc_json, event_date)
            with self.lock:
                if command not in self.events:
                    self.events.append(command)
                else:
                    print('Already added event', desc_json)


def main():
    manager = EventManager()
    manager.SLEEP_DURATION_SEC = 1
    manager.run()
    manager.add([create_dummy_event(datetime.datetime.now(), {
        'method': 'GET',
        'url': 'http://localhost:8000',
    }),
    create_dummy_event(datetime.datetime.now() + datetime.timedelta(seconds=10), {
        'method': 'GET',
        'url': 'http://localhost:8000/2',
    })])
    time.sleep(60 * 10)


if __name__ == '__main__':
    main()