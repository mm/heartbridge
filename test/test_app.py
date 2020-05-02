import unittest, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from heartbridge import app

class TestHealthSampleWorkflow(unittest.TestCase):

    def test_process_health_data(self):
        testing_data = {
            "hrDates": ["16-12-2019 08:24:36", "16-12-2019 09:32:17", "16-12-2019 14:53:35", "16-12-2019 16:13:35", "16-12-2019 19:23:28", "16-12-2019 23:56:25"],
            "hrValues": ["74", "83", "89", "157", "95", "80"]
        }

        self.assertTrue(app.process_health_data(testing_data), msg = 'process_health_data should return True if processing data succeeded')

if __name__ == '__main__':
    unittest.main()