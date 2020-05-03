import unittest, datetime, os, sys, pathlib, csv, json, tempfile
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from heartbridge import heart

class TestSampleLoading(unittest.TestCase):

    def setUp(self):
        self.normal_input = {
            "hrDates": ["2019-12-16 08:24:36", "2019-12-16 09:32:17", "2019-12-16 14:53:35", "2019-12-16 16:13:35", "2019-12-16 19:23:28", "2019-12-16 23:56:25"],
            "hrValues": ["74", "83", "89", "157", "95", "80"]
        }

    def test_valid_json(self):
        # Passing a valid dictionary that meets all conditions should return True.
        self.assertTrue(heart.valid_heart_json(self.normal_input))

    def test_incomplete_json(self):
        # Passing a dictionary that contains the proper keys but contains lists of unequal length should return False.
        incomplete_input = {
            "hrDates": ["2019-12-16 08:24:36", "2019-12-16 14:53:35", "2019-12-16 16:13:35", "2019-12-16 19:23:28", "2019-12-16 23:56:25"],
            "hrValues": ["74", "83", "89", "157"]
        }
        self.assertFalse(heart.valid_heart_json(incomplete_input))

class TestSampleParsing(unittest.TestCase):

    def setUp(self):
        self.normal_input = {
            "hrDates": ["2019-12-16 08:24:36", "2019-12-16 09:32:17", "2019-12-16 14:53:35", "2019-12-16 16:13:35", "2019-12-16 19:23:28", "2019-12-16 23:56:25"],
            "hrValues": ["74", "83", "89", "157", "95", "80"]
        }
        self.parsed_input = heart.parse_heart_json(self.normal_input)

    def test_date_parsing(self):
        # Datetimes parsed from the raw data and stored in the processed data should be equal.
        self.assertEqual(datetime.datetime.strptime(self.normal_input['hrDates'][1], '%Y-%m-%d %H:%M:%S'), self.parsed_input[1][0])

    def test_hr_parsing(self):
        # The nth HR reading in the raw data should correspond to the nth reading in the parsed data.
        self.assertEqual(float(self.normal_input['hrValues'][3]), self.parsed_input[3][1])

    def test_combining(self):
        # Parsing the raw data should produce a list of tuples in the same order as the original data.
        sample_tuple = (datetime.datetime.strptime(self.normal_input['hrDates'][4], '%Y-%m-%d %H:%M:%S'), float(self.normal_input['hrValues'][4]))
        self.assertEqual(sample_tuple, self.parsed_input[4])

class TestFileMethods(unittest.TestCase):

    def setUp(self):
        # One date, and a few readings within that date:
        self.one_date_set = [(datetime.datetime(2019, 12, 2), 40), (datetime.datetime(2019, 12, 2), 45), (datetime.datetime(2019, 12, 2), 94)]
        # Literally only one health sample:
        self.one_sample = [(datetime.datetime(2019, 12, 2), 40)]
        # Multiple samples spanning multiple dates:
        self.multiple_date_set = [(datetime.datetime(2019, 12, 2), 40), (datetime.datetime(2019, 12, 3), 45), (datetime.datetime(2020, 12, 9), 94)]
        # Typical data input as received after being de-serialized from JSON:
        self.normal_input = {
            "hrDates": ["2019-12-16 08:24:36", "2019-12-16 09:32:17", "2019-12-16 14:53:35", "2019-12-16 16:13:35", "2019-12-16 19:23:28", "2019-12-16 23:56:25"],
            "hrValues": ["74", "83", "89", "157", "95", "80"]
        }
        self.parsed_input = heart.parse_heart_json(self.normal_input)

    def test_recognizing_single_date(self):
        # Data containing only one timestamp should produce a string corresponding to the date from that one timestamp.
        self.assertEqual(heart.string_date_range(self.one_date_set), "Dec02-2019")
        self.assertEqual(heart.string_date_range(self.one_sample), "Dec02-2019")
    
    def test_recognizing_date_range(self):
        # Data spanning multiple days should be reflected in the returned string.
        self.assertEqual(heart.string_date_range(self.multiple_date_set), "Dec02-2019-Dec09-2020")

    def test_export_filepath(self):
        # The export_filepath function should be able to handle when a directory isn't specified, doesn't exist or is a file.
        self.assertIsNone(heart.export_filepath('Dec16-2019', None, None), msg = "Passing proper data with no format specified should return None")
        self.assertEqual(heart.export_filepath('Dec16-2019', None, 'csv'), 'Dec16-2019.csv', msg = "Passing no output directory should return a filename and extension only")
        self.assertEqual(str(heart.export_filepath('Dec16-2019', str(os.getcwd()), 'csv')), str(os.getcwd())+'/Dec16-2019.csv', msg = 'Specifying a directory, filename and extension should yield a full file path')

class TestFileWriters(unittest.TestCase):

    def setUp(self):
        # Create a sample input with a few data points (typical, "good" input):
        self.normal_input = {
            "hrDates": ["2019-12-16 08:24:36", "2019-12-16 09:32:17", "2019-12-16 14:53:35", "2019-12-16 16:13:35", "2019-12-16 19:23:28", "2019-12-16 23:56:25"],
            "hrValues": ["74", "83", "89", "157", "95", "80"]
        }
        # Also parse that input into a list of tuples:
        self.parsed_input = heart.parse_heart_json(self.normal_input)

    def test_csv_writing(self):
        # Write a CSV to the cwd:
        path_of_csv_test = heart.write_csv(self.parsed_input, 'unittest_csv.csv')
        # First, make sure the function returns a CSV file path:
        self.assertEqual(path_of_csv_test, str(os.getcwd())+'/unittest_csv.csv')
        
        # Next check the CSV file itself:
        # Does the generated CSV file contain the same data in the same order as the input data?
        all_rows = []
        with open('unittest_csv.csv', newline='') as test_file:
            reader = csv.DictReader(test_file)
            for row in reader:
                all_rows.append((datetime.datetime.strptime(row['Timestamp'], '%Y-%m-%d %H:%M:%S'), float(row['HeartRate'])))
        self.assertEqual(all_rows, self.parsed_input)

    def test_json_writing(self):
        # Write a JSON file to the cwd:
        path_of_json_test = heart.write_json(self.parsed_input, 'unittest_json.json')
        # First, make sure the function returns a CSV file path:
        self.assertEqual(path_of_json_test, str(os.getcwd())+'/unittest_json.json')

        # Check the JSON file itself:
        # Does the generated JSON file contain the same data in the same order as the input data?
        with open('unittest_json.json') as json_derulo:
            loaded = json.load(json_derulo)
            all_rows = [(datetime.datetime.strptime(x['timestamp'], '%Y-%m-%d %H:%M:%S'), x['heartRate']) for x in loaded]
            self.assertEqual(all_rows, self.parsed_input)

    def delete_test_file(self, filename):
        try:
            os.remove(filename)
        except OSError:
            pass

    def tearDown(self):
        # Delete any test files that were created and verified during the unit tests
        self.delete_test_file('unittest_csv.csv')
        self.delete_test_file('unittest_json.json')


if __name__ == '__main__':
    unittest.main()