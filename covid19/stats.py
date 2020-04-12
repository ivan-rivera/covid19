"""Statistical models"""
from datetime import datetime
from typing import Tuple
from typing import Union, List

import numpy as np
from sklearn.linear_model import LinearRegression

from covid19 import types as t
from covid19.utils import read_config

config = read_config()


def fit_infection_trend(kind: t.InfectionStatus,
                        infection_data: t.Infections) -> Tuple[list, list]:
    """
    Fit a linear model to the log of infection data
    :param kind: Infection status (deaths, confirmed, recovered)
    :param infection_data: infection data
    :return: A tuple of unique days  (from zero) and predicted infections for that day
    """
    linear_model = LinearRegression()
    predictors, response = [], []
    for country, content in infection_data.items():
        if country not in config["exclude"]["trend"]:
            counts = [day[kind.value] for day in content]
            days = [day for day in range(len(counts))]
            predictors.extend(days)
            response.extend(np.log10(counts))
    trend_days = sorted(list(set(predictors)))
    linear_model.fit(np.array(predictors).reshape(-1, 1), response)
    predictions = linear_model.predict(np.array(trend_days).reshape(-1, 1))
    rescaled_predictions = [int(np.power(10, p)) for p in predictions]
    return trend_days, rescaled_predictions


def build_summary_stats(infection_data: t.Infections) -> t.Summary:
    """
    Build summary stats from the infection dataset
    :param infection_data: a dictionary with infection records
    :return: a dictionary with summary stats
    """
    last_update = max([datetime.strptime(c, "%Y-%m-%d") for c in get_cases(infection_data, "date")])
    cases_yesterday = sum(get_cases(infection_data, t.InfectionStatus.CONFIRMED.value, 2))
    cases = sum(get_cases(infection_data, t.InfectionStatus.CONFIRMED.value))
    deaths = sum(get_cases(infection_data, t.InfectionStatus.DEATHS.value))
    return t.Summary(
        last_update=t.SummaryDate(title="Last update", value=last_update),
        total_cases=t.SummaryCount(title="Global cases", value=cases),
        total_deaths=t.SummaryCount(title="Global deaths", value=deaths),
        global_growth=t.SummaryPercentage(title="Latest growth", value=cases/cases_yesterday-1),
    )


def get_cases(infection_data: t.Infections,
              kind_str: str,
              lag: int = 1) -> List[Union[str, int, float]]:
    """
    A support function that is used to extract a particular statistic per country
    for a given relative date
    :param infection_data: infection data
    :param kind_str: one of the values that can be found inside infection data (confirmed, deaths, recovered, date)
    :param lag: how many days back from the most recent time to go (1 is latest date)
    :return: a list of kind values of each country
    """
    return [i[-lag][kind_str]
            for i in infection_data.values()
            if len(i) >= lag]
