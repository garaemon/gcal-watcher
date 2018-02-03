#!/usr/bin/env python

import datetime
import json
import fire
import sys

import inquirer

from gcal_watcher.command import Command

RECORD_URL = 'http://localhost:5000/record'
POST_METHOD = 'POST'


class RadioRecordTask(object):

    def __init__(self, task_name, url, method, params):
        self.task_name = task_name
        self.url = url
        self.method = method
        self.params = params

    def to_json(self, pretty=True):
        event = {'url': self.url, 'method': self.method, 'params': self.params}
        if pretty:
            return json.dumps(event, indent=4)
        else:
            return json.dumps(event)

    def to_command(self):
        return ' '.join([
            "curl", self.url, '-X', self.method, '-H', 'Content-Type:application/json', '-d',
            '\'%s\'' % json.dumps(self.params)
        ])


def generate_tasks():
    weekend_shuffle_task = RadioRecordTask(
        'weekend_shuffle', RECORD_URL, POST_METHOD, {
            'artist': '宇多丸',
            'album': 'ウィークエンド・シャッフル(2018)',
            'station_id': 'TBS',
            'name': '${yesterday.year}-${yesterday.month}-${yesterday.day}-ウィークエンド・シャッフル(2018)',
            'start_date': '${yesterday.year}-${yesterday.month}-${yesterday.day}-22-00'
        })
    mygame_mylife = RadioRecordTask(
        'mygame_mylife', RECORD_URL, POST_METHOD, {
            'artist': '宇多丸',
            'album': 'マイゲーム・マイライフ(2018)',
            'station_id': 'TBS',
            'name': '${today.year}-${today.month}-${today.day}-マイゲーム・マイライフ(2018)',
            'start_date': '${today.year}-${today.month}-${today.day}-00-00'
        })
    toradio_first = RadioRecordTask(
        'toradio_first', RECORD_URL, POST_METHOD, {
            'artist': '伊集院光',
            'album': '伊集院光とらじおと(2018)',
            'station_id': 'TBS',
            'name': '${today.year}-${today.month}-${today.day}-1-伊集院光とらじおと(2018)',
            'start_date': '${today.year}-${today.month}-${today.day}-08-30'
        })
    toradio_latter = RadioRecordTask(
        'toradio_latter', RECORD_URL, POST_METHOD, {
            'artist': '伊集院光',
            'album': '伊集院光とらじおと(2018)',
            'station_id': 'TBS',
            'name': '${today.year}-${today.month}-${today.day}-2-伊集院光とらじおと(2018)',
            'start_date': '${today.year}-${today.month}-${today.day}-10-00'
        })
    bakazikara = RadioRecordTask(
        'bakazikara', RECORD_URL, POST_METHOD, {
            'artist': '伊集院光',
            'album': '深夜の馬鹿力(2018)',
            'station_id': 'TBS',
            'name': '${today.year}-${today.month}-${today.day}-深夜の馬鹿力(2018)',
            'start_date': '${today.year}-${today.month}-${today.day}-01-00'
        })
    session22 = RadioRecordTask(
        'session22', RECORD_URL, POST_METHOD, {
            'artist': '荻上チキ',
            'album': 'Session-22(2018)',
            'station_id': 'TBS',
            'name': '${yesterday.year}-${yesterday.month}-${yesterday.day}-Session-22(2018)',
            'start_date': '${yesterday.year}-${yesterday.month}-${yesterday.day}-22-00'
        })
    barakan_beat = RadioRecordTask(
        'barakan beat', RECORD_URL, POST_METHOD, {
            'artist': 'Peter Barakan',
            'album': 'Barakan Beat(2018)',
            'station_id': 'INT',
            'name': '${today.year}-${today.month}-${today.day}-Barakan-Beat(2018)',
            'start_date': '${today.year}-${today.month}-${today.day}-18-00'
        })
    return [
        weekend_shuffle_task, mygame_mylife, toradio_first, toradio_latter, bakazikara, session22,
        barakan_beat
    ]


def interactive_query_task(task_array):
    q = inquirer.List(
        'task',
        message="Which task?",
        choices=[t.task_name for t in task_array],
    )
    return inquirer.prompt([q])['task']


def interactive_query_date():
    today = datetime.datetime.now()
    date_format = '%Y-%m-%d (%A)'
    q = [inquirer.List(
        'day',
        message="Which day?",
        choices=[(today - datetime.timedelta(days=i)).strftime(date_format) for i in range(7)],
    )]
    return inquirer.prompt(q)['day']


class App(object):

    def tasks(self):
        tasks = generate_tasks()
        for t in tasks:
            print(t.task_name)

    def json(self, task=None, pretty=False):
        tasks = generate_tasks()
        if task:
            target_task = [t for t in tasks if t.task_name == task]
            if len(target_task) == 0:
                print('unknown task: %s' % (task))
                sys.exit(1)
            print(target_task[0].to_json(pretty=pretty))
        else:
            for t in tasks:
                print(t.to_json(pretty=pretty))

    def command(self, interactive=False, task=None, date=None):
        task_array = generate_tasks()
        if interactive and task is None:
            task = interactive_query_task(task_array)
        if interactive and date is None:
            date = interactive_query_date()
        # re-parse date
        task_obj = task_array[[t.task_name for t in task_array].index(task)]
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d (%A)')
        replaced_params = {}
        for key in task_obj.params:
            replaced_params[key] = Command.replace_vars(task_obj.params[key],
            date_obj, date_obj, date_obj)
        task_obj.params = replaced_params
        print(task_obj.to_command())

if __name__ == '__main__':
    fire.Fire(App)
