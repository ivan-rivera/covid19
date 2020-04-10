"""Visualizations of infection data. Note that plot types are found here to avoid circular imports"""

from dataclasses import dataclass

import numpy as np
import plotly.graph_objects as go

from covid19 import callbacks as cb
from covid19 import layout
from covid19.data import filter_infection_data
from covid19.stats import fit_infection_trend
from covid19.types import Infections, InfectionStatus, FigureInstance
from covid19.utils import to_date, translate_countries, read_config

config = read_config()


def plot_infection_curve(
        infection_data: Infections,
        kind: InfectionStatus = InfectionStatus.CONFIRMED
) -> go.Figure:
    """
    Plot global infection curves by country
    :param infection_data: a dictionary with the infection data
    :param kind: either confirmed or deaths -- used to select metric
    :return: Figure object with the infection plot
    """
    figure = go.Figure()
    plot_layout = {
        "title": {"text": "Infection Curves By Country"},
        "xaxis": {"title": "Date"},
        "yaxis": {"title": "Count"},
    }
    for country, content in infection_data.items():
        dates = [to_date(day["date"]) for day in content]
        if counts := [day[kind.value] for day in content]:
            lines = go.Scatter(x=dates, y=counts, opacity=0.25,
                               name=country, mode="lines", showlegend=False,
                               legendgroup=country, line=layout.line_style_layout,
                               hovertemplate=layout.trace_hover_template(country))
            figure.add_trace(lines)
    figure.update_layout(layout.global_layout)
    figure.update_layout(plot_layout)
    return figure


def plot_infection_trends(
        infection_data: Infections,
        kind: InfectionStatus = InfectionStatus.CONFIRMED,
        min_cases: int = 100
) -> go.Figure:
    """
    Plot infection trends since hitting the threshold number of infections
    Note that the anchor country is used to set limit the number of days since beginning
    :param infection_data: a dictionary with the infection data
    :param kind: either confirmed or deaths -- used to select metric
    :param min_cases: min number of cases needed to be plotted
    :return: a figure object
    """
    anchor_country = str(config["anchor"])
    filtered_infection_data = filter_infection_data(infection_data, kind=kind)
    global_days, trend = fit_infection_trend(kind, filtered_infection_data)
    day_limit = len(filtered_infection_data[anchor_country])
    figure = go.Figure()
    plot_layout = {
        "title": {"text": f"Days since reaching {min_cases} cases vs Log-scale counts", "y": 1},
        "xaxis": {"title": f"Days since reaching {min_cases} infections", "range": [0, day_limit]},
        "yaxis": {"title": "Count"},
        "yaxis_type": "log",
    }
    for country, content in filtered_infection_data.items():
        counts = [day[kind.value] for day in content]
        days = [day for day in range(len(counts))]
        if counts:
            lines = go.Scatter(x=days, y=counts, name=country, opacity=0.25,
                               mode="lines", line=layout.line_style_layout, showlegend=False,
                               hovertemplate=layout.trace_hover_template(country))
            figure.add_trace(lines)
    trend_line = go.Scatter(x=global_days, y=trend, name="Trend", mode="lines",
                            line={"color": layout.styles.default.alternative_color, "width": 3},
                            showlegend=False, hovertemplate=layout.trace_hover_template("Trend"))
    figure.add_trace(trend_line)
    figure.update_layout(layout.global_layout)
    figure.update_layout(plot_layout)
    return figure


def plot_infected_countries(
        infection_data: Infections,
        kind: InfectionStatus = InfectionStatus.CONFIRMED,
        top_n: int = 20) -> go.Figure:
    """
    Plot a bar chart of top N countries with registered infections
    :param infection_data: a dictionary with the infection data
    :param kind: either confirmed or deaths -- used to select metric
    :param top_n: top N number of countries to plot
    :return: a plotly figure object
    """
    plot_layout = {
        "title": {"text": f"Top {top_n} Countries"},
        "xaxis": {"title": ""},
        "yaxis": {"title": ""},
    }

    def sort_countries(data: dict, ascending: bool = True) -> list:
        """Support function for country sorting"""
        order = 1 if ascending else -1
        return sorted(data.items(), key=lambda item: order * item[1][kind])

    latest_data = {country: {
        InfectionStatus.CONFIRMED: content[-1][InfectionStatus.CONFIRMED.value],
        InfectionStatus.DEATHS: content[-1][InfectionStatus.DEATHS.value]}
        for country, content in infection_data.items() if content}

    top_countries = dict(sort_countries(latest_data, False)[0:top_n])
    sorted_countries = dict(sort_countries(top_countries))
    cases = [v[kind] for v in sorted_countries.values()]
    mortality = [v[InfectionStatus.DEATHS]/v[InfectionStatus.DEATHS]
                 for v in sorted_countries.values()]
    countries = list(sorted_countries.keys())
    bar = go.Bar(x=countries, y=cases, text=mortality, showlegend=False,
                 marker={"color": layout.styles.default.color},
                 hovertemplate=layout.bar_hover_template)
    figure = go.Figure()
    figure.add_trace(bar)
    figure.update_layout(layout.global_layout)
    figure.update_layout(plot_layout)
    return figure


def plot_infection_map(
        infection_data: Infections,
        kind: InfectionStatus = InfectionStatus.CONFIRMED
) -> go.Figure:
    """
    Generate a choropleth map of infections by country
    :param infection_data: a dictionary with the infection data
    :param kind: either confirmed or deaths -- used to select metric
    :return: a Plotly figure object
    """
    map_data = {country: content[-1][kind.value]
                for country, content in infection_data.items() if content}
    translated_map_data = translate_countries(map_data)
    countries = [c for c in translated_map_data.keys()]
    infections = [i for i in translated_map_data.values()]
    world_map = go.Choropleth(
        locations=countries, text=countries, locationmode="country names",
        z=np.log10([i+1 for i in infections]), hovertemplate=layout.map_hover_template,
        hovertext=infections, hoverlabel={"bgcolor": layout.styles.default.background_color},
        showscale=False, colorscale=[layout.styles.default.color, layout.styles.default.base_color])
    figure = go.Figure()
    figure.add_trace(world_map)
    figure.update_layout(layout.global_layout)
    return figure


@dataclass
class FigureSet:

    data: Infections
    kind: InfectionStatus

    def __post_init__(self):
        self.curve = FigureInstance("infection_curve",
                                    plot_infection_curve(self.data, self.kind),
                                    cb.reset_lines,
                                    cb.highlight_lines)
        self.trend = FigureInstance("infection_trend",
                                    plot_infection_trends(self.data, self.kind),
                                    cb.reset_lines,
                                    cb.highlight_lines)
        self.bars = FigureInstance("infected_countries",
                                   plot_infected_countries(self.data, self.kind),
                                   cb.reset_bars,
                                   cb.highlight_bars)
        self.map = FigureInstance("infection_map",
                                  plot_infection_map(self.data, self.kind),
                                  cb.reset_map,
                                  cb.highlight_map)


@dataclass
class Graphic:

    data: Infections

    def __post_init__(self):
        self.figures = {
            InfectionStatus.CONFIRMED.value: FigureSet(self.data, InfectionStatus.CONFIRMED),
            InfectionStatus.DEATHS.value: FigureSet(self.data, InfectionStatus.DEATHS),
        }
