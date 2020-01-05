import unittest
import app
from flask import jsonify, request

class TestHealthSampleWorkflow(unittest.TestCase):

    def test_json_processing(self):
        testing_data = {
            "hrDates": ["16-12-2019 08:24:36", "16-12-2019 09:32:17", "16-12-2019 14:53:35", "16-12-2019 16:13:35", "16-12-2019 19:23:28", "16-12-2019 23:56:25"],
            "hrValues": ["74", "83", "89", "157", "95", "80"]
        }

        test_app = app.app

        test_app.testing = True
        with test_app.test_client() as c:
            rv = c.post('/heartrate', json = testing_data)
            json_response = rv.get_json()
            self.assertIsInstance(json_response, dict, msg = "The /heartrate method must return valid JSON!")
            self.assertEqual(json_response['status'], 'Successful', msg = "The /heartrate method must return 'Successful' in its JSON response for the 'status' key.")
            self.assertEqual(json_response['fileName'], 'Dec16-2019')
            self.assertEqual(json_response['numberOfSamples'], 6)


if __name__ == '__main__':
    unittest.main()