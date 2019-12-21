from flask import Flask, request
from flask_restful import Resource, Api
from heart import valid_heart_json, parse_heart_json, write_csv

app = Flask(__name__)
api = Api(app)

class HeartRateData(Resource):

    def post(self):
        if(request.is_json and valid_heart_json(request.json)):
            parsed_data = parse_heart_json(request.json)
            write_csv(parsed_data, "dec16.csv")
            return {'status': 'accepted' }, 200
        else:
            return 'invalid data', 400

api.add_resource(HeartRateData, '/heartrate')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')