from flask import Flask, request
from flask_restful import Resource, Api
from heart import valid_heart_json, parse_heart_json
import pandas as pd
import plotly.express as px

app = Flask(__name__)
api = Api(app)

class HeartRateData(Resource):

    def get(self):
        return {'status': 'success'}, 200

    def post(self):
        if(request.is_json and valid_heart_json(request.json)):
            parsed_data = parse_heart_json(request.json)
            df = pd.DataFrame(data = parsed_data, columns = ['Timestamp', 'HeartRate'])
            fig = px.line(df, x = 'Timestamp', y = 'HeartRate')
            fig.show()
            return {'status': 'accepted' }, 200
        else:
            return 'invalid data', 400

api.add_resource(HeartRateData, '/heartrate')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')