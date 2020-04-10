"""Callback support methods"""

from typing import List, Tuple

import plotly.graph_objects as go

from covid19.layout import styles, map_hover_template
from covid19.types import HoverData, FigureInstance
from covid19.utils import read_config

config = read_config()


def reset_lines(fig: go.Figure) -> go.Figure:
    """Reset lines of the infection plots"""
    for trace in fig.data:
        if trace["name"] not in config["exclude"]["trace"]:
            trace["line"]["color"] = styles.default.color
            trace["line"]["width"] = styles.default.line_width
            trace["opacity"] = styles.default.opacity
    return fig


def reset_bars(fig: go.Figure) -> go.Figure:
    """Reset bar plots"""
    fig.data[0].marker.color = styles.default.color
    return fig


def reset_map(fig: go.Figure) -> go.Figure:
    """Reset world map"""
    if fig.data[0]:
        fig.data = [fig.data[0]]
    return fig


def highlight_lines(fig: go.Figure, country: str) -> go.Figure:
    """Highlight lines of the infection plots"""
    if index := [i for i, c in enumerate(fig.data) if c["name"] == country]:
        fig.data[index[0]]["line"]["color"] = styles.highlight.color
        fig.data[index[0]]["line"]["width"] = styles.highlight.line_width
        fig.data[index[0]]["opacity"] = styles.highlight.opacity
        return fig


def highlight_map(fig: go.Figure, country: str) -> go.Figure:
    """Highlight a country on the map"""
    country_index = [i for i, c in enumerate(fig.data[0]["locations"]) if c == country][0]
    highlighted_country = go.Choropleth(
        locations=[country], z=[fig.data[0]["z"][country_index]],
        locationmode="country names", text="Highlight",
        hoverlabel={"bgcolor": styles.default.background_color},
        hovertext=[int(fig.data[0]["hovertext"][country_index])],
        marker_line_color=styles.highlight.map_outline_color,
        colorscale=[styles.highlight.color, styles.highlight.color],
        showscale=False, hovertemplate=map_hover_template)
    fig.add_trace(highlighted_country)
    return fig


def highlight_bars(fig: go.Figure, country: str) -> go.Figure:
    """Highlight an individual bar"""
    bar_countries = fig.data[0].x
    cols = [styles.default.color] * len(bar_countries)
    country_position = [index for index, bar_country in enumerate(bar_countries)
                        if bar_country == country]
    for highlight_country in country_position:
        cols[highlight_country] = styles.highlight.color
        fig.data[0].marker.color = cols
        return fig


def find_selected_country(hover_context: List[Tuple[FigureInstance, HoverData]]) -> str:
    """find country that is being hovered over"""
    for fig, hover in hover_context:
        if hover:
            hover_data = hover["points"][0]
            if fig.id_str in ["infected_countries"]:
                return hover_data["x"]
            elif fig.id_str in ["infection_map"]:
                return hover_data["location"]
            else:
                country = [content["name"]
                           for index, content in enumerate(fig.figure.data)
                           if index == hover_data["curveNumber"]][0]
                if country not in config["exclude"]["trace"]:
                    return country
