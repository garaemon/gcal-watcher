from unittest import TestCase as PythonTestCase
from datetime import datetime

from gcal_watcher.command import Command, CommandException


class CommandTestCase(PythonTestCase):

    def test_replace_vars(self):
        event_date = datetime(year=2018, month=2, day=10)
        self.assertEqual(
            Command.replace_vars('${today.year}-${today.month}-${today.day}-foo', event_date),
            '2018-02-10-foo')
        self.assertEqual(
            Command.replace_vars('${yesterday.year}-${yesterday.month}-${yesterday.day}-foo',
                                 event_date), '2018-02-09-foo')
        self.assertEqual(
            Command.replace_vars('${tomorrow.year}-${tomorrow.month}-${tomorrow.day}-foo',
                                 event_date), '2018-02-11-foo')

    def test_verify_fields(self):
        self.assertRaises(CommandException, lambda: Command.verify_fields({}))
        self.assertRaises(CommandException, lambda: Command.verify_fields({'method': 'POST'}))
        self.assertRaises(CommandException, lambda: Command.verify_fields({'url': 'http://localhost/'}))
        self.assertTrue(Command.verify_fields({'method': 'POST', 'url': 'http://localhost/'}))
        self.assertTrue(
            Command.verify_fields({
                'method': 'POST',
                'url': 'http://localhost/',
                'params': {
                    'aaa': 1
                }
            }))

    def test_parse_radirec_request(self):
        json_request = {
            'method': 'POST',
            'url': 'http://localhost:5000/record',
            'params': {
                'station_id': 'TBS',
                'start_date': '${today.year}-${today.month}-${today.day}-22-00',
                'artist': 'Foo',
                'album': 'Foo-album',
                'title': 'Foo-${today.year}-${today.month}-${today.day}'
            }
        }
        event_date = datetime(year=2018, month=2, day=10)
        command = Command(json_request, event_date)
        self.assertEqual(command.method, 'POST')
        self.assertEqual(command.url, 'http://localhost:5000/record')
        self.assertEqual(command.params['station_id'], 'TBS')
        self.assertEqual(command.params['start_date'], '2018-02-10-22-00')
        self.assertEqual(command.params['artist'], 'Foo')
        self.assertEqual(command.params['album'], 'Foo-album')
        self.assertEqual(command.params['title'], 'Foo-2018-02-10')

    def test_command_eq(self):
        json_request1 = {
            'method': 'POST',
            'url': 'http://localhost:5000/record',
            'params': {
                'station_id': 'TBS',
                'start_date': '${today.year}-${today.month}-${today.day}-22-00',
                'artist': 'Foo',
                'album': 'Foo-album',
                'title': 'Foo-${today.year}-${today.month}-${today.day}'
            }
        }
        json_request2 = {
            'method': 'POST',
            'url': 'http://localhost:5000/record',
            'params': {
                'station_id': 'JOLF',
                'start_date': '${today.year}-${today.month}-${today.day}-22-00',
                'artist': 'Foo',
                'album': 'Foo-album',
                'title': 'Foo-${today.year}-${today.month}-${today.day}'
            }
        }
        event_date1 = datetime(year=2018, month=2, day=10)
        event_date2 = datetime(year=2018, month=2, day=11)
        command1 = Command(json_request1, event_date1)
        command2 = Command(json_request1, event_date2)
        self.assertTrue(Command(json_request1, event_date1) == Command(json_request1, event_date1))
        self.assertTrue(Command(json_request2, event_date2) == Command(json_request2, event_date2))
        self.assertFalse(Command(json_request1, event_date1) == Command(json_request2, event_date1))
        self.assertFalse(Command(json_request1, event_date1) == Command(json_request1, event_date2))
        self.assertFalse(Command(json_request1, event_date1) == Command(json_request2, event_date2))
        self.assertTrue(
            Command(json_request1, event_date1) in [
                Command(json_request1, event_date1),
                Command(json_request1, event_date2),
                Command(json_request2, event_date2)
            ])
        self.assertFalse(
            Command(json_request2, event_date1) in [
                Command(json_request1, event_date1),
                Command(json_request1, event_date2),
                Command(json_request2, event_date2)
            ])
