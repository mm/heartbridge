from starlette.responses import JSONResponse
from starlette.testclient import TestClient
from heartbridge.app import app
import test.sample_inputs as samples
import pathlib
import pytest

@pytest.mark.parametrize('output_format', ['csv', 'json'])
def test_endpoint_validDataShouldReturn200(tmp_path, output_format):
    app.state.OUTPUT_DIRECTORY = str(tmp_path)
    app.state.OUTPUT_FORMAT = output_format
    data = samples.HR_TYPICAL_INPUT

    client = TestClient(app)
    response = client.post('/', json=data)

    file = pathlib.Path(tmp_path / 'heart-rate-Dec16-2019.{}'.format(output_format))
    assert response.status_code == 200
    assert file.exists()

@pytest.mark.filterwarnings("ignore::FutureWarning")
@pytest.mark.parametrize('output_format', ['csv', 'json'])
def test_endpoint_validLegacyDataShouldReturn200(tmp_path, output_format):
    app.state.OUTPUT_DIRECTORY = str(tmp_path)
    app.state.OUTPUT_FORMAT = output_format
    data = samples.LEGACY_TYPICAL_INPUT

    client = TestClient(app)
    response = client.post('/', json=data)

    file = pathlib.Path(tmp_path / 'heart-rate-legacy-Dec16-2019.{}'.format(output_format))
    assert response.status_code == 200
    assert file.exists()

def test_endpoint_withoutType_shouldRaise400(tmp_path):
    app.state.OUTPUT_DIRECTORY = str(tmp_path)
    app.state.OUTPUT_FORMAT = '.out'

    data = {
        'dates': [],
        'values': []
    }

    client = TestClient(app)
    response = client.post('/', json=data)

    assert response.status_code == 400

def test_endpoint_validationError_shouldRaise422(tmp_path):
    app.state.OUTPUT_DIRECTORY = str(tmp_path)
    app.state.OUTPUT_FORMAT = '.out'
    data = {
        'type': 'Heart Rate',
        'dates': ['2020-03-20 09:40:22']

    }
    client = TestClient(app)
    response = client.post('/', json=data)
    assert response.status_code == 422