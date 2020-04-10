"""Extract data for the dashboard"""

import json
import logging
from datetime import datetime

import requests
from cachetools.func import ttl_cache

from covid19.types import Infections, InfectionStatus
from covid19.utils import read_config, to_date

logger = logging.getLogger(__name__)


@ttl_cache(maxsize=None, ttl=24*60*60)
def get_infection_data() -> Infections:
    """
    Retrieve infections (confirmed cases, deaths and recoveries) by country and date.
    Data is cached for 24 hours
    :return: A dictionary of countries with a list of dates and counts
    """
    config = read_config()
    endpoint = config["endpoints"]["infections"]
    text = requests.get(endpoint).text
    infection_data = json.loads(text)
    logger.info(f"retrieved infection data with {len(infection_data)} countries")
    return infection_data


def filter_infection_data(
        infection_data: Infections,
        kind: InfectionStatus = InfectionStatus.CONFIRMED,
        min_cases: int = 100,
        min_date: datetime = datetime(2020, 1, 1)
) -> Infections:
    """
    Retrieve a subset of infection data filtered by the number of confirmed cases and minimum date
    :param infection_data: dictionary with infection records
    :param kind: either confirmed or deaths
    :param min_cases: min. number of confirmed cases per country for it to be included into the dataset
    :param min_date: first date to be included into the data
    :return: filtered infection data
    """
    filtered_countries = {
        country: [day for day in content
                  if to_date(day["date"]) >= min_date
                  and day[kind.value] >= min_cases]
        for country, content in infection_data.items()}
    return {country: content for country, content
            in filtered_countries.items() if content}
