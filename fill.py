import view
import pandas as pd
from exception_guard import exception_guard
from config import *

class FillFactory:
    def __init__(self):
        self._fillers = {
            'on_points': view.point.add_on_point,
            'off_points': view.point.add_off_point,
            'reactions': view.reaction.add_reaction, # TODO: СОЗДАТЬ КОЛОНКУ С ТИПОМ В CSV: ONLINE/OFFLINE!!!!!
            'files': view.file.add_file
        }

    @exception_guard
    def fill(self, format, file_path):
        data = pd.read_csv(file_path)
        for index, row in data.iterrows():
            kwargs = {key: row[key] for key in row.keys()}
            self._fillers[format](kwargs) # TODO: когда буду вводить эту функцию, поменять add-функцию на kwargs
            print(index, 'OK')
        return SUCCESS  # TODO: выводить OK и SUCCESS только если правда все успешно
