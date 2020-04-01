"""Statistical models"""
from typing import Tuple

import numpy as np
from sklearn.linear_model import LinearRegression

from covid19.types import Infections, InfectionStatus


def fit_infection_trend(infection_status: InfectionStatus, infection_data: Infections) -> Tuple[list, list]:
    """
    Fit a linear model to the log of infection data
    :param infection_status: Infection status (deaths, confirmed, recovered)
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
            counts = [day[infection_status.value] for day in content]
            days = [day for day in range(len(counts))]
            predictors.extend(days)
            response.extend(np.log10(counts))
    trend_days = sorted(list(set(predictors)))
    linear_model.fit(np.array(predictors).reshape(-1, 1), response)
    predictions = linear_model.predict(np.array(trend_days).reshape(-1, 1))
    rescaled_predictions = [int(np.power(10, p)) for p in predictions]
    return trend_days, rescaled_predictions
