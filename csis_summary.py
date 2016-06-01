from config import CSISConfigs
from csis_folders import CSISFolders
from collections import namedtuple
import os, csv


class Summary(CSISConfigs):
    def __init__(self, batch: namedtuple):
        super().__init__()
        self.batch = batch
        self.file_path = self.batch[0] + '/' + self.batch[1] + '_summary.txt'

    def exists(self):
        """
        :return: (bool) Summary file exists for the given batch
        """
        return os.path.isfile(self.file_path)

    def summary_data(self) -> namedtuple:
        """
        Pulls data from a batch summary table.
        :return: (namedtuple) summary table data.
        """
        sleep = int(self.configs['ignore_summary_lines'])
        if self.exists():
            with open(self.file_path, 'r') as file_data:
                reader = csv.reader(file_data, delimiter='\t')
                data_list = []
                for data in reader:
                    if sleep != 0:
                        sleep -= 1
                    else:
                        data_list.append(data)
                point = namedtuple('summary', 'inspected, good, good_percent, '
                                              'fail_general, fail_gen_percent, '
                                              'fail_od, fail_od_percent, fail_backward, '
                                              'fail_backward_percent, n_a, n_a_percent')
                str_list = (data_list[0][1], *data_list[1][1:3], *data_list[2][1:3],
                            *data_list[3][1:3], *data_list[4][1:3], *data_list[5][1:3])
                converted_list = self.converted_summary_list(str_list)
                return point(*converted_list)

    @staticmethod
    def converted_summary_list(summary_list):
        converted_list = []
        for item in summary_list:
            try:
                converted_list.append(int(item))
            except ValueError:
                converted_list.append(float(item))
        return converted_list


if __name__ == '__main__':
    print(CSISFolders().current_batch())
    print(CSISSummary(CSISFolders().current_batch()).exists())