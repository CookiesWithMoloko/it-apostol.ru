import os
import importlib


def import_dir(path: str, log: bool = False):
    for i in os.listdir('%s/' % path):
        if i.endswith('.py') and i != '__init__.py':
            if log:
                print('import %s.%s' % (path, i[:-3]))
            importlib.import_module('%s.%s' % (path, i[:-3]))

