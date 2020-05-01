import unittest, datetime, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from heartbridge import heart

class TestSampleLoading(unittest.TestCase):

    def setUp(self):
        self.normal_input = {
            "hrDates": ["16-12-2019 08:24:36", "16-12-2019 09:32:17", "16-12-2019 14:53:35", "16-12-2019 16:13:35", "16-12-2019 19:23:28", "16-12-2019 23:56:25"],
            "hrValues": ["74", "83", "89", "157", "95", "80"]
        }

    def test_valid_json(self):
        self.assertTrue(heart.valid_heart_json(self.normal_input))

    def test_incomplete_json(self):
        incomplete_input = {
            "hrDates": ["16-12-2019 08:24:36", "16-12-2019 14:53:35", "16-12-2019 16:13:35", "16-12-2019 19:23:28", "16-12-2019 23:56:25"],
            "hrValues": ["74", "83", "89", "157"]
        }
        self.assertFalse(heart.valid_heart_json(incomplete_input))

class TestSampleParsing(unittest.TestCase):

    def setUp(self):
        self.normal_input = {
            "hrDates": ["16-12-2019 08:24:36", "16-12-2019 09:32:17", "16-12-2019 14:53:35", "16-12-2019 16:13:35", "16-12-2019 19:23:28", "16-12-2019 23:56:25"],
            "hrValues": ["74", "83", "89", "157", "95", "80"]
        }
        self.parsed_input = heart.parse_heart_json(self.normal_input)

    def test_date_parsing(self):
        self.assertEqual(datetime.datetime.strptime(self.normal_input['hrDates'][1], '%d-%m-%Y %H:%M:%S'), self.parsed_input[1][0])

    def test_hr_parsing(self):
        self.assertEqual(float(self.normal_input['hrValues'][3]), self.parsed_input[3][1])

    def test_combining(self):
        sample_tuple = (datetime.datetime.strptime(self.normal_input['hrDates'][4], '%d-%m-%Y %H:%M:%S'), float(self.normal_input['hrValues'][4]))
        self.assertEqual(sample_tuple, self.parsed_input[4])

class TestFileMethods(unittest.TestCase):

    def setUp(self):
        self.one_date_set = [(datetime.datetime(2019, 12, 2), 40), (datetime.datetime(2019, 12, 2), 45), (datetime.datetime(2019, 12, 2), 94)]
        self.one_sample = [(datetime.datetime(2019, 12, 2), 40)]
        self.multiple_date_set = [(datetime.datetime(2019, 12, 2), 40), (datetime.datetime(2019, 12, 3), 45), (datetime.datetime(2020, 12, 9), 94)]

    def test_recognizing_single_date(self):
        self.assertEqual(heart.string_date_range(self.one_date_set), "Dec02-2019")
        self.assertEqual(heart.string_date_range(self.one_sample), "Dec02-2019")
    
    def test_recognizing_date_range(self):
        self.assertEqual(heart.string_date_range(self.multiple_date_set), "Dec02-2019-Dec09-2020")

if __name__ == '__main__':
    unittest.main()