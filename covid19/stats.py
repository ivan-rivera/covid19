"""Statistical models"""
from datetime import datetime
from typing import Dict, Union
from typing import Tuple

import numpy as np
from sklearn.linear_model import LinearRegression

from covid19.types import Infections


def fit_infection_trend(kind: str, infection_data: Infections) -> Tuple[list, list]:
    """
    Fit a linear model to the log of infection data
    :param kind: Infection status (deaths, confirmed, recovered)
    :param infection_data: infection data
    :return: A tuple of unique days  (from zero) and predicted infections for that day
    """
    exclude_countries = [
        "China",
        "Diamond Princess"
    ]
    linear_model = LinearRegression()
    predictors, response = [], []
    for country, content in infection_data.items():
        if country not in exclude_countries:
            counts = [day[kind] for day in content]
            days = [day for day in range(len(counts))]
            predictors.extend(days)
            response.extend(np.log10(counts))
    trend_days = sorted(list(set(predictors)))
    linear_model.fit(np.array(predictors).reshape(-1, 1), response)
    predictions = linear_model.predict(np.array(trend_days).reshape(-1, 1))
    rescaled_predictions = [int(np.power(10, p)) for p in predictions]
    return trend_days, rescaled_predictions


def build_summary_stats(infection_data: Infections) -> Dict[str, Union[int, str, float]]:
    """
    Build summary stats from the infection dataset
    :param infection_data: a dictionary with infection records
    :return: a dictionary with summary stats
    """
    get_cases = lambda kind, lag=1: [i[-lag][kind] for i in infection_data.values() if len(i) >= lag]
    last_update = max([datetime.strptime(c, "%Y-%m-%d") for c in get_cases("date")])
    cases_yesterday = sum(get_cases("confirmed", 2))
    cases = sum(get_cases("confirmed"))
    deaths = sum(get_cases("deaths"))
    mortality = deaths / cases
    return {
        "last update": last_update.strftime("%Y-%m-%d"),
        "total cases": f"{cases:,}",
        "total deaths": f"{deaths:,}",
        "mortality rate": f"{mortality:.2%}",
        "global growth": f"{cases/cases_yesterday-1:.2%}",
    }
