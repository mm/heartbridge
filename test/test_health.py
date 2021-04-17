import pytest
from datetime import datetime
from heartbridge import Health
from heartbridge.exceptions import LoadingError, ValidationError
from heartbridge.constants import LEGACY_RECORD_TYPE
import test.sample_inputs as samples


@pytest.mark.parametrize(
    "input_data, expected",
    [
        ({"type": "Heart Rate", "dates": [], "values": []}, "heart-rate"),
        ({"dates": [], "values": []}, None),
    ],
)
def test_extract_record_type(input_data, expected):
    health = Health()
    if expected is not None:
        reading_type = health._extract_record_type(input_data)
        assert reading_type == expected
    else:
        with pytest.raises(LoadingError):
            health._extract_record_type(input_data)


@pytest.mark.filterwarnings("ignore::FutureWarning")
def test_extract_record_type_legacy():
    data = {"hrDates": [], "hrValues": []}
    health = Health()
    assert health._extract_record_type(data) == LEGACY_RECORD_TYPE


@pytest.mark.parametrize(
    "input_data, reading_type, expect_ve",
    [
        ({"type": "Heart Rate", "dates": [], "values": []}, "heart-rate", False),
        ({"hrDates": [], "hrValues": []}, "heart-rate-legacy", False),
        ({"hrDates": []}, "heart-rate-legacy", True),
        ({"dates": []}, "heart-rate", True),
        ({"type": "Heart Rate", "dates": [], "values": [1]}, "heart-rate", True),
    ],
)
def test_validate_input_fields(input_data, reading_type, expect_ve):
    health = Health()

    if expect_ve:
        with pytest.raises(ValidationError):
            health._validate_input_fields(input_data, reading_type)
    else:
        assert health._validate_input_fields(input_data, reading_type)


def test_shortcuts_data_parse_heart_rate():
    data = samples.HR_TYPICAL_INPUT

    health = Health()
    health.load_from_shortcuts(data)
    given_sample = health.readings[3].to_dict()

    assert len(health.readings) == len(data["dates"])
    assert given_sample["timestamp"] == data["dates"][3]
    assert given_sample["heart_rate"] == int(data["values"][3])
    assert health.reading_type_slug == "heart-rate"


def test_recognize_date_range_singleDay():
    data = {
        "type": "Heart Rate",
        "dates": ["2020-05-02 09:20:00", "2020-05-02 14:52:00"],
        "values": ["120", "50"],
    }
    health = Health()
    health.load_from_shortcuts(data)
    assert health._string_date_range() == "May02-2020"


def test_recognize_date_range_multiDay():
    data = {
        "type": "Heart Rate",
        "dates": ["2020-05-20 09:20:00", "2020-06-14 14:52:00"],
        "values": ["120", "50"],
    }
    health = Health()
    health.load_from_shortcuts(data)
    assert health._string_date_range() == "May20-2020-Jun14-2020"
