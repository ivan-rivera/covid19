"""Plot layout settings. _layout variables are consumed by plotly Figure objects"""

from dataclasses import dataclass

from covid19.utils import extract_css_variables

# todo: this is temporary
# color_scheme = {
#     "background": "#011627",
#     "main": "#2EC4B6",
#     "highlight": "#E71D36",
#     "alternative": "#FF9F1C",
#     "base": "#FDFFFC",
# }

# color_scheme = {
#     "bg-colour": "#1E1E1E",
#     "main-colour": "#FADC6E",
#     "highlight-colour": "#F0645A",
#     "alternative-colour": "#288CB4",
#     "base-colour": "#82DCD2",
# }


color_scheme = extract_css_variables()


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
    DefaultStyle(line_width=2, opacity=0.25, color=color_scheme["main"]),
    HighlightStyle(line_width=5, opacity=1, map_outline_color=color_scheme["highlight"], color=color_scheme["highlight"]),
)



global_layout = {
    "xaxis": {"showgrid": False, 'zeroline': False},
    "yaxis": {"showgrid": False, 'zeroline': False},
    "font": {"color": color_scheme["base"], "family": "Amaranth"},
    "paper_bgcolor": 'rgba(0,0,0,0)',
    "plot_bgcolor": 'rgba(0,0,0,0)',
    "margin": {"r": 0, "l": 0, "t": 0, "b": 0},
    "autosize": True,
}

line_style_layout = {
    "color": color_scheme["main"],
    "width": styles.default.line_width
}
