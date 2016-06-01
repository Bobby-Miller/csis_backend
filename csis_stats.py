from config import CSISConfigs
from types import GeneratorType
from csis_folders import CSISFolders
from collections import namedtuple as nt
import csv
import os
import datetime


class Stats(CSISConfigs):
    def __init__(self, batch: nt):
        super().__init__()
        self.batch = batch
        self.file_path = self.batch[0] + '/' + self.batch[1] + '_stats.txt'

    def exists(self) -> bool:
        """
        :return: (bool) Summary file exists for the given batch
        """
        return os.path.isfile(self.file_path)

    def stats_data(self) -> GeneratorType:
        sleep = int(self.configs['ignore_stats_lines'])
        if self.exists():
            with open(self.file_path, 'r') as file_data:
                reader = csv.reader(file_data, delimiter='\t')
                ignore_count = 0
                for data in reader:
                    ignore_count += 1
                    if sleep != 0:
                        sleep -= 1
                    else:
                        yield data

    def field_zip(self) -> GeneratorType:
        field_list = [
            "id",
            "overall_result",
            "re_station",
            "fe_station",
            "odp_station",
            "ss_station",
            "time",
            "re_valid_master",
            "re_present",
            "re_orientation",
            "re_valid",
            "re_inner_bright",
            "re_inner_small_dark",
            "re_inner_large",
            "re_outer_bright",
            "re_outer_small_dark",
            "re_outer_large_dark",
            "re_ida_bright",
            "re_ida_large_dark",
            "re_ida_small_dark",
            "re_oda_bright",
            "re_oda_large_dark",
            "re_oda_small_dark",
            "re_m_center_x",
            "re_m_center_y",
            "re_uut_center_x",
            "re_uut_center_y",
            "fe_valid_master",
            "fe_orientation",
            "fe_valid",
            "fe_inner_diameter",
            "fe_obstruction",
            "fe_chip",
            "fe_inner_dia_min",
            "fe_inner_dia_max",
            "fe_obstr_area",
            "fe_chip_area",
            "odp_position",
            "odp_length",
            "odp_bumps",
            "odp_chips",
            "odp_envelope",
            "odp_nose",
            "odp_num_images",
            "odp_length_mm",
            "odp_max_bump_mm",
            "odp_max_chip_mm",
            "odp_envelope_mm",
            "_",
            "odp_nose_w_min_max",
            "_",
            "odp_mdn_od_mm",
            "ss_valid",
            "ss_bright_defect",
            "ss_blemish_defect",
            "ss_spot_crack_defect",
            "ss_bright_da_mm2",
            "ss_blemish_da_mm2",
            "ss_spot_crack_da_mm2",
            "ss_num_frames"
        ]
        ignore_list = [49, 51]
        return (dict(zip(field_list, data)) for i, data in enumerate(self.stats_data())
                if i not in ignore_list)

    @staticmethod
    def field_map(dictseq, name, func) -> GeneratorType:
        for d in dictseq:
            d[name] = func(d[name])
            yield d

    def type_map(self) -> GeneratorType:
        pass_fail_names = ['re_station', 'fe_station', 'odp_station', 'ss_station',
                           're_valid_master', 're_present', 're_orientation',
                           're_valid', 're_inner_bright', 're_inner_small_dark',
                           're_inner_large', 're_outer_bright', 're_outer_small_dark',
                           're_outer_large_dark', 'fe_valid_master', 're_valid_master',
                           'fe_orientation', 'fe_valid', 'fe_inner_diameter',
                           'fe_obstruction', 'fe_chip', 'odp_position', 'odp_length',
                           'odp_bumps', 'odp_chips', 'odp_envelope', 'odp_nose',
                           'ss_valid', 'ss_bright_defect', 'ss_blemish_defect',
                           'ss_spot_crack_defect']
        float_names = ['re_ida_bright', 're_ida_large_dark', 're_ida_small_dark',
                       're_oda_bright', 're_oda_large_dark', 're_oda_small_dark',
                       're_m_center_x', 're_m_center_y', 're_uut_center_x',
                       're_uut_center_y','fe_inner_dia_min',
                       'fe_inner_dia_max', 'fe_obstr_area', 'fe_chip_area',
                       'odp_length_mm', 'odp_max_bump_mm', 'odp_max_chip_mm',
                       'odp_envelope_mm', 'odp_nose_w_min_max', 'odp_mdn_od_mm',
                       'ss_bright_da_mm2', 'ss_blemish_da_mm2', 'ss_spot_crack_da_mm2']
        int_names = ['id', 'odp_num_images', 'ss_num_frames']
        d = self.field_zip()
        for name in pass_fail_names:
            d = self.field_map(d, name, lambda v: True if v == 'Pass' else False)
        for name in float_names:
            d = self.field_map(d, name, lambda v: 0 if v == 'NaN' else float(v))
        for name in int_names:
            d = self.field_map(d, name, int)
        d = self.field_map(d, 'time', lambda v: datetime.datetime.strptime(
                                                      v, '%I:%M:%S.%f %p %m/%d/%Y'))
        for d in d:
            del d['_']
            yield d

if __name__ == "__main__":
    stats = Stats(CSISFolders().current_batch())
    data_gen = stats.stats_data()
    print(len(next(data_gen)))
    field_gen = stats.field_zip()
    print(len(next(field_gen)))
    converted_gen = stats.type_map()
    print(next(converted_gen))

