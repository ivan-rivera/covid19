"""Tests for the project"""
from datetime import datetime

import pytest

from covid19.data import get_infection_data, filter_infection_data
from covid19.stats import get_cases
from covid19.types import InfectionStatus
from covid19.utils import read_config, to_date, translate_countries


def test_read_config():
    config = read_config()
    config_has_content = bool(config)
    config_is_dict = isinstance(config, dict)
    assert config_has_content and config_is_dict, "malformed config"


def test_get_infection_data():
    infection_data = get_infection_data()
    first_country = list(infection_data.keys())[0]
    latest_entry_date = infection_data[first_country][-1]["date"]
    max_date = max([entry["date"] for entry in infection_data[first_country]])
    assert max_date == latest_entry_date, "dates in infection data are not sorted"


@pytest.mark.parametrize("infection_data, kind, min_cases, min_date, expected", [
    (
            {"Country": [
                {"date": "2020-01-01", "confirmed": 1},
                {"date": "2020-01-02", "confirmed": 2}
            ]},
            InfectionStatus.CONFIRMED, 2, datetime(2020, 1, 2),
            {"Country": [{"date": "2020-01-02", "confirmed": 2}]}
    ),

])
def test_filter_infection_data(infection_data, kind, min_cases, min_date, expected):
    print(filter_infection_data(infection_data, kind, min_cases, min_date))
    assert filter_infection_data(infection_data, kind, min_cases, min_date) == expected


@pytest.mark.parametrize("infection_data, kind_str, lag, expected_date", [
    ({"Country": [{"date": "2020-01-01", "confirmed": 1}, {"date": "2020-01-02", "confirmed": 2}]},
     "date", 1, "2020-01-02")
])
def test_get_cases(infection_data, kind_str, lag, expected_date):
    selected = get_cases(infection_data, kind_str, lag)[0]
    assert selected == expected_date


@pytest.mark.parametrize("date_str, date", [
    ("2020-01-01", datetime(2020, 1, 1)),
    ("2020-12-31", datetime(2020, 12, 31)),
])
def test_to_date(date_str, date):
    assert to_date(date_str) == date, "date conversion is incorrect"


@pytest.mark.parametrize("raw, translated", [
    ({"CountryX": 1, "Taiwan*": 2}, {"CountryX": 1, "Taiwan": 2})
])
def test_translate_countries(raw, translated):
    assert translate_countries(raw) == translated, "country translation is broken"
