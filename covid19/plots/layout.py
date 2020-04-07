"""Plot layout settings. _layout variables are consumed by plotly Figure objects"""

from dataclasses import dataclass


@dataclass
class DefaultStyle:
    color: str
    line_width: int
    opacity: float


@dataclass
class HighlightStyle:
    color: str
    line_width: int
    opacity: float
    map_outline_color: str


@dataclass
class Style:
    default: DefaultStyle
    highlight: HighlightStyle


styles = Style(
    DefaultStyle(line_width=1, opacity=0.5, color="darkgrey"),
    HighlightStyle(line_width=5, opacity=1, map_outline_color="red", color="red"),
)

global_layout = {
    "xaxis": {"showgrid": False, 'zeroline': False},
    "yaxis": {"showgrid": False, 'zeroline': False},
    "font": {"color": "darkgray", "family": "Sen"},
    "paper_bgcolor": 'rgba(0,0,0,0)',
    "plot_bgcolor": 'rgba(0,0,0,0)',
    "margin": {"r": 0, "l": 0, "t": 0, "b": 0},
    "autosize": True,
}

line_style_layout = {
    "color": "darkgray",
    "width": styles.default.line_width
}
