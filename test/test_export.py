import csv, json, pathlib

from heartbridge import Health
from heartbridge.export import CSVExporter, JSONExporter, export_filepath
import test.sample_inputs as samples


def test_export_filepath_directoryAlreadyExists(tmp_path):
    path = export_filepath('test', tmp_path, 'csv')
    assert path == tmp_path / 'test.csv'

def test_export_filepath_directoryDoesNotExist(tmp_path):
    directory = tmp_path / 'apples'
    path = export_filepath('test', directory, 'csv')
    assert path == tmp_path / 'apples/test.csv'

def test_export_filepath_useCurrentWorkingDir():
    """If output_dir is not specified, the filepath returned should be in the 
    current working directory
    """
    path = export_filepath(filename='test', output_dir=None, filetype='csv')
    assert path == pathlib.Path('test.csv')

def test_csv_exporter(tmp_path):
    health = Health()
    data = samples.HR_TYPICAL_INPUT
    health.load_from_shortcuts(data)

    filename = tmp_path / 'test.csv'

    filepath = CSVExporter().readings_to_file(health.readings, filename=filename)
    
    with open(filepath, 'r') as created_csv:
         reader = csv.DictReader(created_csv, ['timestamp', 'heart_rate'])
         next(reader) # skip the header line
         for i, row in enumerate(reader):
            health_sample = health.readings[i]
            assert health_sample.timestamp_string == row['timestamp']
            assert str(health_sample.heart_rate) == row['heart_rate']

def test_json_exporter(tmp_path):
    health = Health()
    data = samples.HR_TYPICAL_INPUT
    health.load_from_shortcuts(data)

    filename = tmp_path / 'test.json'

    filepath = JSONExporter().readings_to_file(health.readings, filename=filename)

    with open(filepath, 'r') as json_derulo:
        loaded = json.load(json_derulo)
        for i, reading in enumerate(loaded):
            health_sample = health.readings[i]
            assert health_sample.timestamp_string == reading['timestamp']
            assert health_sample.heart_rate == reading['heart_rate']