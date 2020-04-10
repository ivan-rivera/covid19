"""Helper utilities"""
import re
from copy import deepcopy
from datetime import datetime
from logging import getLogger
from pathlib import Path
from typing import Dict, Union

import yaml

logger = getLogger(__name__)


def get_app_dir() -> Path:
    """
    Fetch project path
    :return: A Path of to the app directory
    """
    current_dir = Path(__file__).resolve()
    return current_dir.parent.parent


def read_config() -> Dict[str, Dict[str, Union[str, int, float]]]:
    """
    Read project configuration file
    :return: A dictionary with configurations
    """
    app_dir = get_app_dir()
    config_path = app_dir / "config.yaml"
    with open(str(config_path)) as stream:
        config = yaml.safe_load(stream)
    logger.debug(f"config file loaded with the following content: {config}")
    return config


def to_date(date_str: str) -> datetime:
    """
    Format string dates to datetime
    :param date_str: date string in format Y-m-d
    :return: datetime
    """
    return datetime.strptime(date_str, "%Y-%m-%d")


def translate_countries(countries: Dict[str, int]) -> Dict[str, int]:
    """
    Convert inconsistent country names into the format recognized by Plotly Choropleth
    :param countries: a dictionary with countries and counts
    :return: updated dictionary with countries and counts
    """
    modified_countries = deepcopy(countries)
    country_mapping = {
        "DRC": ["Congo (Brazzaville)", "Congo (Kinshasa)"],
        "Czech Republic": ["Czechia"],
        "Macedonia": ["North Macedonia"],
        "Myanmar": ["Burma"],
        "Taiwan": ["Taiwan*"],
        "Ivory Coast": ["Cote d'Ivoire"],
    }
    for country, content in country_mapping.items():
        modified = {country: sum([modified_countries[lookup]
                                  for lookup in content
                                  if lookup in modified_countries])}
        modified_countries.update(modified)
        for lookup in content:
            if lookup in modified_countries:
                logger.debug(f"updated country {lookup}")
                del modified_countries[lookup]
    return modified_countries


def extract_css_variables():
    css_styles = {}
    variable_pattern = r"\s+-{2}(\w?|-?)+:\s.*;$"
    app_dir = get_app_dir()
    css_path = app_dir / "assets" / "style.css"
    with open(str(css_path)) as css:
        for line in css.readlines():
            if re.match(variable_pattern, line):
                variable, value = re.sub(r"\s|--|;", "", line).split(":")
                css_styles[variable] = value
    logger.debug(f"The following CSS variables were identified: {css_styles}")
    return css_styles
