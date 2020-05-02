import unittest, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from heartbridge import app

def delete_test_file(filename):
        try:
            os.remove(filename)
        except OSError:
            pass

class TestHealthSampleWorkflow(unittest.TestCase):

    def setUp(self):
        self.typical_data = {
            "hrDates": ["16-12-2019 08:24:36", "16-12-2019 09:32:17", "16-12-2019 14:53:35", "16-12-2019 16:13:35", "16-12-2019 19:23:28", "16-12-2019 23:56:25"],
            "hrValues": ["74", "83", "89", "157", "95", "80"]
        }

    def test_process_health_data_success(self):
        # Test whether the process_health_data function returns True on success:
        success_csv = app.process_health_data(self.typical_data, output_format = 'csv')
        success_json = app.process_health_data(self.typical_data, output_format = 'json')

        self.assertTrue(success_csv, msg = 'process_health_data should return True if processing data succeeded')
        self.assertTrue(success_json, msg = 'process_health_data should return True if processing data succeeded')

    def test_process_health_data_default_dir(self):
        # Test whether CSV/JSON files get written to the current working directory as a result of running the app
        app.process_health_data(self.typical_data, output_format = 'csv')
        app.process_health_data(self.typical_data, output_format = 'json')
        self.assertTrue(os.path.exists('Dec16-2019.csv'), msg = 'process_health_data should write a CSV to disk if successful and CSV was selected')
        self.assertTrue(os.path.exists('Dec16-2019.json'), msg = 'process_health_data should write a JSON file to disk if successful and JSON was selected')

    def test_process_health_data_custom_dir(self):
        # Test whether CSV/JSON files get written to a custom directory as a result of running the app
        app.process_health_data(self.typical_data, output_dir = 'test_results_temp', output_format = 'csv')
        app.process_health_data(self.typical_data, output_dir = 'test_results_temp', output_format = 'json')
        self.assertTrue(os.path.exists('test_results_temp/Dec16-2019.csv'), msg = 'process_health_data should write a CSV to the directory specified if successful and CSV was selected')
        self.assertTrue(os.path.exists('test_results_temp/Dec16-2019.json'), msg = 'process_health_data should write a JSON file to the directory specified if successful and JSON was selected')

    def tearDown(self):
        delete_test_file('Dec16-2019.csv')
        delete_test_file('Dec16-2019.json')
        delete_test_file('test_results_temp/Dec16-2019.csv')
        delete_test_file('test_results_temp/Dec16-2019.json')

        try:
            os.rmdir('test_results_temp')
        except OSError:
            pass

if __name__ == '__main__':
    unittest.main()