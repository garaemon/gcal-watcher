from unittest import TestCase as PythonTestCase
from datetime import datetime

from gcal_watcher.googlecalendar import (remove_tag)
import json

class CommandTestCase(PythonTestCase):


    def test_remove_tag(self):
        self.assertEqual(remove_tag('<p>Hello World</p>'), 'Hello World')
        self.assertEqual(remove_tag('<a>Hello World</a>'), 'Hello World')
        self.assertEqual(remove_tag('<a href="foo bar piyo">Hello World</a>'), 'Hello World')
        self.assertEqual(remove_tag('Hello <a href="foo bar piyo">World</a>'), 'Hello World')
        self.assertEqual(
            remove_tag('Hello <a href="foo bar piyo">World</a> Bye'), 'Hello World Bye')

    def test_json_parse(self):
        json_doc = '{"method": "POST", "params": {"artist": "\u4f0a\u96c6\u9662\u5149", "album": "\u4f0a\u96c6\u9662\u5149\u3068\u3089\u3058\u304a\u3068(2018)", "name": "${today.year}-${today.month}-${today.day}-1-\u4f0a\u96c6\u9662\u5149\u3068\u3089\u3058\u304a\u3068(2018)", "station_id": "TBS", "start_date": "${today.year}-${today.month}-${today.day}-08-30"}, "url": "<a href="https://www.google.com/url?q=http%3A%2F%2Flocalhost%3A5000%2Frecord&amp;sa=D&amp;usd=2&amp;usg=AFQjCNEp2W7peMy5b_sc3LIrYOdwWyVFIA" target="_blank">http://localhost:5000/record</a>"}'
        try:
            json.loads(remove_tag(json_doc))
        except Exception:
            self.fail('Failed to parse %s' % json_doc)