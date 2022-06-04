import os
import importlib
import types
from typing import List


def import_dir(path: str, log: bool = False) -> List[types.ModuleType]:
    r: List[types.ModuleType] = []
    for i in os.listdir('%s/' % path):
        if i.endswith('.py') and i != '__init__.py':
            if log:
                print('import %s.%s' % (path, i[:-3]))
            r.append(importlib.import_module('%s.%s' % (path, i[:-3])))
    return r

