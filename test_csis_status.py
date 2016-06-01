import csis_status as cs
import unittest as utest
from config import configs


class TestCaseCSISStatus(utest.TestCase):
    def status_data_change(self, new_data):
        """
        Updates status.txt with new_data
        :param new_data: Iterable of length 7
        :return: No return
        """
        data_path = configs['test_data_path']
        joiner = '/'
        file_path = joiner.join((data_path, 'Status.txt'))
        with open(file_path, 'w') as file:
            template = "Batch ID: {0}\n" \
                       "Total: {1}\n" \
                       "Pass: {2}\n" \
                       "Fail: {3}\n" \
                       "Fail OD: {4}\n" \
                       "Backwards: {5}\n" \
                       "N/A: {6}\n" \
                       "Downstream Counter: 1"
            file_data = template.format(*new_data)
            file.write(file_data)

    def equal_data_sets(self, test_data):
        self.status_data_change(test_data)
        test_df = cs.CSISStatus().status_df.transpose()
        test_list = test_df.values.tolist()
        self.assertEqual(*test_list, test_data[1:])




