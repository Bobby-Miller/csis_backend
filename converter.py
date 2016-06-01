"""
converter.py

converter converts data in a table from one type to another
"""
from collections import namedtuple, defaultdict

class StringArrayConverter:
    """
    converts a table that is all strings into different data types for more
    consistent usage.
    """
    def __init__(self, string_array, cols=None):
        """
        initialize converter
        :param string_table: The array of strings to be converted
        :param cols:
        """
        self.string_array = string_array
        self.cols = cols

        self.converter_map = None

    @property
    def cols(self):
        return self.__cols

    @cols.setter
    def cols(self, cols):
        if cols is None:
            self.__cols = range(len(self.string_array[0]))
        else:
            self.__cols = (num for num in cols)
        assert all(col < len(self.string_array[0]) for col in self.__cols),\
            'some element(s) in cols is outside of range of the array'

    @property
    def converter_map(self):
        return self.__converter_map

    @converter_map.setter
    def converter_map(self, map):
        if map is None:
            self.__converter_map = {}
            self.to_str(self.cols)
        else:
            self.__converter_map = map

    def to_bool(self, true_string, false_string, cols):
        """
        Converts column to boolean.
        :param true_string: string that correlates to True
        :param false_string: string that correlates to False
        :param cols: iterable list of columns to be converted to boolean
        :return: No return
        """
        bool_dict = {true_string: True, false_string: False}
        for col in cols:
            Pointer = namedtuple('Pointer', ('Method', 'kwargs'))
            self.converter_map[col] = Pointer(self.bool_convert, bool_dict)

    def to_str(self, cols):
        """
        Converts column to boolean.
        :param cols: iterable list of columns to be converted to boolean
        :return: No return
        """
        for col in cols:
            Pointer = namedtuple('Pointer', ('Method', 'kwargs'))
            self.converter_map[col] = Pointer(self.keep_string, {})

    def to_num(self, cols):
        pass

    @staticmethod
    def bool_convert(string, bool_dict):
        return bool_dict[string]

    @staticmethod
    def keep_string(string):
        return string

    @staticmethod
    def num_convert(string):
        try:
            return int(string)
        except ValueError:
            return float(string)

    def convert(self):
        for row in self.string_array:
            for idx, cell in row:
                kwargs = self.converter_map[idx].kwargs
                self.converter_map[idx].Method(cell, **kwargs)


if __name__ == '__main__':
    example = StringArrayConverter([['a', 'b', 'c'],['d', 'e', 'f']], cols=[7])
    # example.to_bool(true_string='a', false_string='d', cols=[0])
    # print(example.converter_map)