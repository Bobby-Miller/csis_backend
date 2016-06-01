from converter import StringArrayConverter as sac
import unittest


class TestCaseSACcols(unittest.TestCase):
    """Base class for all col tests."""

    def col_gen_equal(self, sac_object, ref_gen):
        self.assertEqual(sac_object.cols, ref_gen)

    def long_array(self):
        return [['a', 'b', 'c', 'd', 'e', 'f'], ['g', 'h', 'i', 'j', 'k', 'l']]


class TestSACcols(TestCaseSACcols):
    def test_col_generator(self):
        string_array = [['a'], ['b']]
        converter = sac(string_array)
        self.col_gen_equal(converter, range(1))

    def test_col_generator_longer_array(self):
        string_array = [['a', 'd'], ['b', 'd']]
        converter = sac(string_array)
        self.col_gen_equal(converter, range(2))

    def test_manual_entry(self):
        converter = sac(self.long_array(), cols=(1, 3, 5))
        self.col_gen_equal(converter, (1, 3, 5))

    def test_error_when_manual_out_of_range(self):
        with self.assertRaises(AssertionError):
            converter = sac(self.long_array(), cols=[7])

# class TestCaseSACConverterMap(unittest.TestCase):
#
#
# class TestSACConverterMap(unittest.TestCase):



