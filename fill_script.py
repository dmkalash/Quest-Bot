# -*- coding: utf-8 -*-
from utils import create_tables, fill_on_points, fill_off_points, fill_on_reactions, fill_off_reactions, fill_files

class ScriptFactory:
    def __init__(self):
        self._scripts = {
            'create_tables': create_tables,
            'on_points': fill_on_points,
            'off_points': fill_off_points,
            'on_reactions': fill_on_reactions,
            'off_reactions': fill_off_reactions,
            'files': fill_files
        }

    def run(self):
        for key in self._scripts:
            self._scripts[key]()
            print(key, ': OK')

def fill_script():
    factory = ScriptFactory()
    factory.run()