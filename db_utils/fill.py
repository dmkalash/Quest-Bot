import view
import pandas as pd
from exception_guard import exception_guard
from config import *


class FillFactory:
    def __init__(self):
        self._fillers = {
            ON_POINT_KEY: view.point.add_on_point,
            OFF_POINT_KEY: view.point.add_off_point,
            REACTION_KEY: view.reaction.add_reaction,
            FILE_KEY: view.file.add_file
        }

    @exception_guard
    def fill(self, format, file_path):
        data = pd.read_csv(file_path, sep=CSV_SEP)
        print(format)
        for index, row in data.iterrows():
            kwargs = {key: row[key] for key in row.keys()}
            self._fillers[format](**kwargs)
            print(index, 'OK')
        return SUCCESS
