"""Plot layout settings. _layout variables are consumed by plotly Figure objects"""

from dataclasses import dataclass

from covid19.utils import extract_css_variables

css_vars = extract_css_variables()


@dataclass
class DefaultStyle:
    font: str
    color: str
    base_color: str
    background_color: str
    alternative_color: str
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
    DefaultStyle(
        font=css_vars["font"],
        line_width=2,
        opacity=0.25,
        color=css_vars["main"],
        base_color=css_vars["base"],
        background_color=css_vars["background"],
        alternative_color=css_vars["alternative"],
    ),
    HighlightStyle(
        line_width=5,
        opacity=1,
        map_outline_color=css_vars["highlight"],
        color=css_vars["highlight"]
    ),
)


global_layout = {
    "title": {"x": 0.1, "y": 0.95, "font": {"size": 16}},
    "xaxis": {"showgrid": False, 'zeroline': False, "linecolor": "rgba(0,0,0,0)"},
    "yaxis": {"showgrid": False, 'zeroline': False, "linecolor": "rgba(0,0,0,0)"},
    "font": {
        "color": styles.default.base_color,
        "family": styles.default.font
    },
    "paper_bgcolor": 'rgba(0,0,0,0)',
    "plot_bgcolor": 'rgba(0,0,0,0)',
    "margin": {"r": 0, "l": 0, "t": 0, "b": 0},
    "autosize": True,
    "geo": {
        "projection_type": "natural earth",
        "visible": False,
        "resolution": 110,
        "showcountries": True,
        "countrycolor": styles.default.base_color,
        "lataxis": {"range": [-55, 80]}
    },
    "dragmode": False,
}

line_style_layout = {
    "color": styles.default.color,
    "width": styles.default.line_width
}


bar_hover_template = (
    f"<span style='color:{styles.default.background_color};" +
    "font-size:20px'><b>%{x}</b></span><br><br>" +
    "Cases: %{y}<br>" +
    "Mortality rate: %{text:.2%}" +
    "<extra></extra>"
)

map_hover_template = (
    f"<span style='color:{styles.default.color};" +
    "font-size:20px'><b>%{location}</b></span><br>" +
    f"<span style='color:{styles.default.alternative_color}'>" +
    "Cases: %{hovertext:,}</span>" +
    "<extra></extra>"
)


def trace_hover_template(country: str) -> str:
    """Generate text for a traces corresponding to specific countries"""
    return (f"<span style='color:{styles.default.background_color};" +
            f"font-size:20px'><b>{country}</b></span><br><br>" +
            "Date: %{x}<br>" +
            "Cases: %{y:,}" +
            "<extra></extra>")
