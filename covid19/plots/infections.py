"""Visualizations of infection data"""

import numpy as np
import plotly.graph_objects as go

from covid19.data import filter_infection_data
from covid19.plots.layout import global_layout, line_style_layout, color_scheme
from covid19.stats import fit_infection_trend
from covid19.types import Infections
from covid19.utils import to_date, translate_countries


def plot_infection_curve(infection_data: Infections, kind: str = "confirmed") -> go.Figure:
    """
    Plot global infection curves by country
    :param infection_data: a dictionary with the infection data
    :param kind: either confirmed or deaths -- used to select metric
    :return: Figure object with the infection plot
    """

    figure = go.Figure()
    plot_layout = {
        "title": {"text": "Infection Curves By Country", "x": 0.1, "y": 0.95, "font": {"size": 16}},
        "xaxis": {"title": "Date", "linecolor": "rgba(0,0,0,0)"},
        "yaxis": {"title": "Count"},
    }

    for country, content in infection_data.items():
        dates = [to_date(day["date"]) for day in content]
        counts = [day[kind] for day in content]
        if counts:
            lines = go.Scatter(
                x=dates,
                y=counts,
                name=country,
                opacity=0.25,
                mode="lines",
                showlegend=False,
                legendgroup=country,
                line=line_style_layout,
                hovertemplate=
                f"<span style='color:{color_scheme['background']};font-size:20px'><b>{country}</b></span><br><br>" +
                "Date: %{x}<br>" +
                "Cases: %{y:,}" +
                "<extra></extra>"

            )
            figure.add_trace(lines)

    figure.update_layout(global_layout)
    figure.update_layout(plot_layout)

    return figure


def plot_infection_trends(
        infection_data: Infections,
        kind: str = "confirmed",
        min_cases: int = 100
) -> go.Figure:
    """
    Plot infection trends since hitting the threshold number of infections
    :param infection_data: a dictionary with the infection data
    :param kind: either confirmed or deaths -- used to select metric
    :param min_cases: min number of cases needed to be plotted
    :return: a figure object
    """
    anchor_country = "Italy"  # used to set limit the number of days since beginning
    exclude_countries = [
        "Diamond Princess"
    ]

    # filter cases
    filtered_infection_data = filter_infection_data(infection_data, kind=kind)
    global_days, trend = fit_infection_trend(kind, filtered_infection_data)

    day_limit = len(filtered_infection_data[anchor_country])

    figure = go.Figure()
    plot_layout = {
        "title": {"text": f"Days since reaching {min_cases} cases vs Log-scale counts",
                  "x": 0.1, "y": 1, "font": {"size": 16}},
        "xaxis": {"title": f"Days since reaching {min_cases} infections", "range": [0, day_limit]},
        "yaxis": {"title": "Count", "linecolor": "rgba(0,0,0,0)"},
        "yaxis_type": "log",
    }

    for country, content in filtered_infection_data.items():
        if country not in exclude_countries:
            counts = [day[kind] for day in content]
            days = [day for day in range(len(counts))]
            if counts:
                lines = go.Scatter(
                    x=days,
                    y=counts,
                    name=country,
                    opacity=0.25,
                    mode="lines",
                    line=line_style_layout,
                    showlegend=False,
                    hovertemplate=
                    f"<span style='color:{color_scheme['background']};font-size:20px'><b>{country}</b></span><br><br>" +
                    "Date: %{x}<br>" +
                    "Cases: %{y:,}" +
                    "<extra></extra>"
                )
                figure.add_trace(lines)

    trend_line = go.Scatter(
        x=global_days,
        y=trend,
        name="Trend",
        line={"color": color_scheme["alternative"], "width": 3},
        mode="lines",
        showlegend=False,
        hovertemplate=
        f"<span style='color:{color_scheme['background']};font-size:20px'><b>Trend</b></span><br><br>" +
        "Date: %{x}<br>" +
        "Cases: %{y:,}" +
        "<extra></extra>"
    )
    figure.add_trace(trend_line)
    figure.update_layout(global_layout)
    figure.update_layout(plot_layout)

    return figure


def plot_infected_countries(infection_data: Infections, kind: str = "confirmed", top_n: int = 20) -> go.Figure:
    """
    Plot a barchart of top N countries with registered infections
    :param infection_data: a dictionary with the infection data
    :param kind: either confirmed or deaths -- used to select metric
    :param top_n: top N number of countries to plot
    :return: a plotly figure object
    """

    plot_layout = {
        "title": {"text": f"Top {top_n} Countries", "x": 0.1, "y": 0.95, "font": {"size": 16}},
        "xaxis": {"title": "", "linecolor": "rgba(0,0,0,0)"},
        "yaxis": {"title": ""},
    }

    def sort_countries(data: dict, ascending: bool = True) -> list:
        """Support function for country sorting"""
        order = 1 if ascending else -1
        return sorted(data.items(), key=lambda item: order * item[1][kind])

    latest_data = {country: {"confirmed": content[-1]["confirmed"],
                             "deaths": content[-1]["deaths"]}
                   for country, content in infection_data.items()
                   if content}

    top_countries = dict(sort_countries(latest_data, False)[0:top_n])
    sorted_countries = dict(sort_countries(top_countries))

    cases = [v[kind] for v in sorted_countries.values()]
    mortality = [v["deaths"]/v["confirmed"] for v in sorted_countries.values()]
    countries = list(sorted_countries.keys())

    bar = go.Bar(
        x=countries,
        y=cases,
        text=mortality,
        showlegend=False,
        marker={"color": color_scheme["main"]},
        hovertemplate=
        f"<span style='color:{color_scheme['background']};" +
        "font-size:20px'><b>%{x}</b></span><br><br>" +
        "Cases: %{y}<br>" +
        "Mortality rate: %{text:.2%}" +
        "<extra></extra>"
    )

    figure = go.Figure()
    figure.add_trace(bar)
    figure.update_layout(global_layout)
    figure.update_layout(plot_layout)

    return figure


def plot_infection_map(infection_data: Infections, kind: str = "confirmed") -> go.Figure:
    """
    Generate a choropleth map of infections by country
    :param infection_data: a dictionary with the infection data
    :param kind: either confirmed or deaths -- used to select metric
    :return: a Plotly figure object
    """

    plot_layout = {
        "geo": {
            "projection_type": "natural earth",
            "visible": False,
            "resolution": 110,
            "showcountries": True,
            "countrycolor": color_scheme["base"],
            "lataxis": {"range": [-55, 80]}
        },
        "dragmode": False,
        "margin": {"t": 0, "b": 0},
    }

    map_data = {country: content[-1][kind]
                for country, content in infection_data.items()
                if content}

    translated_map_data = translate_countries(map_data)

    countries = [c for c in translated_map_data.keys()]
    infections = [i for i in translated_map_data.values()]

    world_map = go.Choropleth(
        locations=countries,
        z=np.log10([i+1 for i in infections]),
        text=countries,
        hovertext=infections,
        hoverlabel={"bgcolor": color_scheme["background"]},
        locationmode="country names",
        showscale=False,
        colorscale=[color_scheme["base"], color_scheme["main"]],
        hovertemplate=
        f"<span style='color:{color_scheme['main']};" +
        "font-size:20px'><b>%{location}</b></span><br>" +
        f"<span style='color:{color_scheme['alternative']}'>" +
        "Cases: %{hovertext:,}</span>" +
        "<extra></extra>"
    )

    figure = go.Figure()
    figure.add_trace(world_map)
    figure.update_layout(global_layout)
    figure.update_layout(plot_layout)

    return figure
