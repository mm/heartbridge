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
