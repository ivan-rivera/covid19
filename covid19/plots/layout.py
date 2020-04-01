"""Plot layout settings"""

from dataclasses import dataclass


@dataclass
class DefaultStyle:
    line_width: int
    opacity: float


@dataclass
class HighlightStyle:
    line_width: int
    opacity: float


@dataclass
class Style:
    default: DefaultStyle
    highlight: HighlightStyle


styles = Style(
    DefaultStyle(line_width=1, opacity=0.5),
    HighlightStyle(line_width=5, opacity=1),
)

global_layout = {
    "xaxis": {"showgrid": False, 'zeroline': False},
    "yaxis": {"showgrid": False, 'zeroline': False},
    "font": {"color": "darkgray", "family": "Sen"},
    "paper_bgcolor": 'rgba(0,0,0,0)',
    "plot_bgcolor": 'rgba(0,0,0,0)',
    "margin": {"r": 0, "l": 0},
}

line_style = {
    "color": "darkgray",
    "width": styles.default.line_width
}
