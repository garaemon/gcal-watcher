import time
import os

from .googlecalendar import GCalClient
from .event_manager import EventManager

class GcalWatcher(object):
    TIMESTEP_SEC = 60 * 10 # every 10 minutes
    # TIMESTEP_SEC = 10
    UPCOMING_EVENTS_NUM = 10
    def __init__(self):
        self.event_manager = EventManager()
        self.event_manager.run()

    def watch(self):
        # run loop
        self.invoke()
        while True:
            time.sleep(self.TIMESTEP_SEC)
            self.invoke()

    def invoke(self):
        print('Checking google calendar events')
        client = GCalClient('raspi_tasks', os.environ['GCAL_WATCHER_CALENDAR_ID'])
        events = client.get_upcoming_events(self.UPCOMING_EVENTS_NUM)
        print(events)
        self.event_manager.add(events)

def main():
    watcher = GcalWatcher()
    watcher.TIMESTEP_SEC = 1 # shorter seconds for test
    watcher.watch()


if __name__ == '__main__':
    main()
