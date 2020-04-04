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


def find_selected_country(hover_context: List[Tuple[go.Figure, HoverData]]) -> str:
    """find country that is being hovered over"""
    for fig, hover in hover_context:
        if hover:
            country = [
                content["name"]
                for index, content in enumerate(fig.data)
                if index == hover["points"][0]["curveNumber"]
            ][0]
            if country not in _excluded_traces:
                return country


def highlight_lines(fig: go.Figure, country: str) -> go.Figure:
    """Highlight lines of the infection plots"""
    if index := [i for i, c in enumerate(fig.data) if c["name"] == country]:
        fig.data[index[0]]["line"]["width"] = styles.highlight.line_width
        fig.data[index[0]]["opacity"] = styles.highlight.opacity
        return fig
