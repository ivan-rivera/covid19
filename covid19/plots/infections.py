"""Visualizations of infection data"""

import plotly.graph_objects as go

from covid19.data import get_filtered_infection_data
from covid19.plots.layout import global_layout, line_style
from covid19.stats import fit_infection_trend
from covid19.types import InfectionStatus
from covid19.utils import to_date


# todo: review settings and move stuff into configs


def plot_infection_curve() -> go.Figure:
    """
    Plot global infection curves by country
    :return: Figure object with the infection plot
    """

    infection_data = get_filtered_infection_data()
    figure = go.Figure()
    plot_layout = {
        "title": {"text": "Infection Curves By Country"},
        "xaxis": {"title": "Date", "linecolor": "rgba(0,0,0,0)"},
        "yaxis": {"title": "Count of Infections"},
    }

    for country, content in infection_data.items():
        dates = [to_date(day["date"]) for day in content]
        counts = [day["confirmed"] for day in content]
        if counts:
            lines = go.Scatter(
                x=dates,
                y=counts,
                name=country,
                opacity=0.25,
                mode="lines",
                showlegend=False,
                legendgroup=country,
                line=line_style,
                hovertemplate=
                f"<span style='color:black;font-size:20px'><b>{country}</b></span><br><br>" +
                "Date: %{x}<br>" +
                "Cases: %{y:,}" +
                "<extra></extra>"

            )
            figure.add_trace(lines)

    figure.update_layout(global_layout)
    figure.update_layout(plot_layout)

    return figure


def plot_infection_trends(infection_threshold: int = 100) -> go.Figure:
    """
    Plot infection trends since hitting the threshold number of infections
    :param infection_threshold: minimum number of infections to consider
    :return: a figure object
    """
    exclude_countries = [
        "China",
        "Diamond Princess"
    ]
    infection_data = get_filtered_infection_data(min_confirmed=infection_threshold)
    global_days, trend = fit_infection_trend(InfectionStatus.CONFIRMED, infection_data)

    figure = go.Figure()
    plot_layout = {
        "title": {"text": f"Days since reaching {infection_threshold} infections vs Log-scale Infection Counts"},
        "xaxis": {"title": f"Days since reaching {infection_threshold} infections"},
        "yaxis": {"title": "Count of Infections", "linecolor": "rgba(0,0,0,0)"},
        "yaxis_type": "log"
    }

    for country, content in infection_data.items():
        if country not in exclude_countries:
            counts = [day["confirmed"] for day in content]
            days = [day for day in range(len(counts))]
            if counts:
                lines = go.Scatter(
                    x=days,
                    y=counts,
                    name=country,
                    opacity=0.25,
                    mode="lines",
                    line=line_style,
                    showlegend=False,
                    hovertemplate=
                    f"<span style='color:black;font-size:20px'><b>{country}</b></span><br><br>" +
                    "Date: %{x}<br>" +
                    "Cases: %{y:,}" +
                    "<extra></extra>"
                )
                figure.add_trace(lines)

    trend_line = go.Scatter(
        x=global_days,
        y=trend,
        name="Trend",
        line={"color": "red"},
        mode="lines",
        showlegend=False,
        hovertemplate=
        "<span style='color:black;font-size:20px'><b>Trend</b></span><br><br>" +
        "Date: %{x}<br>" +
        "Cases: %{y:,}" +
        "<extra></extra>"
    )
    figure.add_trace(trend_line)
    figure.update_layout(global_layout)
    figure.update_layout(plot_layout)

    return figure
