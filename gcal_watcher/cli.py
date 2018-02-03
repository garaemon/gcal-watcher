# Commandline entry point

import fire

from .gcal_watcher import GcalWatcher

class CliApp(object):
    def run(self):
        watcher = GcalWatcher()
        watcher.watch()

def main():
    'Entrypoint for setup.py'
    fire.Fire(CliApp)

if __name__ == '__main__':
    main()


