from config import CSISConfigs
import os
from datetime import datetime
from collections import namedtuple
from typing import NamedTuple
from operator import itemgetter


class CSISFolders(CSISConfigs):

    def parse_folder_data(self) -> \
            NamedTuple('Parse', (('folder_path', str), ('batch_name', str),
                                 ('end_datetime', datetime))):
        """
        Pull all folder names from the csis_config data_path variable,
        and parse it into a list containing: file path, batch name,
        batch date, batch time
        :return: (namedtuple) Parse:[file_path, batch_name, batch_datetime]
        """
        point = NamedTuple('Parse', (('folder_path', str), ('batch_name', str),
                                 ('end_datetime', datetime)))

        def parse(folder):
            return folder[0].split("\\")[-1].split("-")

        parsed_folders = [
            point(
                *(x[0],
                  parse(x)[0],
                  datetime(year=int(parse(x)[1][0:4]), month=int(parse(x)[1][4:6]),
                           day=int(parse(x)[1][6:8]), hour=int(parse(x)[2][0:2]),
                           minute=int(parse(x)[2][2:4]), second=int(parse(x)[2][4:6]))
                  )
            )
            for x in os.walk(self.data_path)
            if x[0] != self.data_path and len(x[0].split("\\")) == 2
            ]
        return parsed_folders

    def current_batch(self) -> NamedTuple:
        """
        sorts parsed folders and returns most recent batch set
        :return: (namedtuple) most recent batch info
        """
        batch_list = self.parse_folder_data()
        sorted_batch_list = sorted(batch_list, key=itemgetter(2))
        return sorted_batch_list[-1]



if __name__ == '__main__':
    print(CSISFolders().parse_folder_data())
    print(CSISFolders().current_batch())