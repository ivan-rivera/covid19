"""Callback support methods"""

from typing import List, Tuple

import plotly.graph_objects as go

from covid19.plots.layout import styles
from covid19.types import HoverData

_excluded_traces = ["Trend"]


def reset_lines(fig: go.Figure) -> go.Figure:
    """Reset lines of the infection plots"""
    for trace in fig.data:
        if trace["name"] not in _excluded_traces:
            trace["line"]["width"] = styles.default.line_width
            trace["opacity"] = styles.default.opacity
    return fig


def reset_bars(fig: go.Figure) -> go.Figure:
    """Reset bar plots"""
    fig.data[0].marker.color = styles.default.color
    return fig


def reset_map(fig: go.Figure) -> go.Figure:
    """Reset world map"""
    fig.data = [fig.data[0]]
    return fig


def highlight_lines(fig: go.Figure, country: str) -> go.Figure:
    """Highlight lines of the infection plots"""
    if index := [i for i, c in enumerate(fig.data) if c["name"] == country]:
        fig.data[index[0]]["line"]["width"] = styles.highlight.line_width
        fig.data[index[0]]["opacity"] = styles.highlight.opacity
        return fig


def highlight_map(fig: go.Figure, country: str) -> go.Figure:
    """Highlight a country on the map"""
    country_index = [i for i, c in enumerate(fig.data[0]["locations"]) if c == country][0]
    highlighted_country = go.Choropleth(
        locations=[country],
        z=[fig.data[0]["z"][country_index]],
        locationmode="country names",
        text="Highlight",
        hovertext=[int(fig.data[0]["hovertext"][country_index])],
        marker_line_color=styles.highlight.map_outline_color,
        colorscale="reds", showscale=False,
        hovertemplate=
        "<span style='color:darkgrey;font-size:20px'><b>%{location}</b></span><br>" +
        "Cases: %{hovertext:,}" +
        "<extra></extra>"
    )
    fig.add_trace(highlighted_country)
    return fig


def highlight_bars(fig: go.Figure, country: str) -> go.Figure:
    """Highlight an individual bar"""
    bar_countries = fig.data[0].x
    cols = [fig.data[0].marker.color] * len(bar_countries)
    country_position = [
        index for index, bar_country in enumerate(bar_countries)
        if bar_country == country
    ]
    for highlight_country in country_position:
        cols[highlight_country] = styles.highlight.color
        fig.data[0].marker.color = cols
        return fig


def find_selected_country(hover_context: List[Tuple[go.Figure, HoverData, str]]) -> str:
    """find country that is being hovered over"""
    for fig, hover, kind in hover_context:
        if hover:
            hover_data = hover["points"][0]
            if kind == "bars":
                return hover_data["x"]
            elif kind == "map":
                return hover_data["location"]
            else:
                country = [
                    content["name"]
                    for index, content in enumerate(fig.data)
                    if index == hover_data["curveNumber"]
                ][0]
                if country not in _excluded_traces:
                    return country
