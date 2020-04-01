"""Helper utilities"""

from datetime import datetime
from pathlib import Path
from typing import Dict, Union

import yaml


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
    return config


def to_date(date_str: str) -> datetime:
    """
    Format string dates to datetime
    :param date_str: date string in format Y-m-d
    :return: datetime
    """
    return datetime.strptime(date_str, "%Y-%m-%d")
