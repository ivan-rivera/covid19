"""Dash application"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from decouple import config
from flask import Flask

from covid19.plots.infections import plot_infection_curve, plot_infection_trends
from covid19.plots.layout import styles
from covid19.utils import get_app_dir, read_config

config_file = read_config()
app_dir = get_app_dir()

with open(str(app_dir / "assets" / "header.md")) as header_file:
    header_md = header_file.read()

infection_curve = plot_infection_curve()
infection_trend = plot_infection_trends()

server = Flask(__name__)
app = dash.Dash(__name__, server=server)
app.title = config_file["title"]
app.layout = html.Div(children=[
    html.H1(children=config_file["title"], className="title"),
    dcc.Markdown(header_md, className="desc"),
    html.Section(children=[
        dcc.Graph(figure=infection_curve, id="left_infection_plot", className="left_plot", clear_on_unhover=True),
        dcc.Graph(figure=infection_trend, id="right_infection_plot", className="right_plot", clear_on_unhover=True),
    ], className="plots")
])


@app.callback(
    [
        dash.dependencies.Output("left_infection_plot", "figure"),
        dash.dependencies.Output("right_infection_plot", "figure"),
    ],
    [
        dash.dependencies.Input("left_infection_plot", "hoverData"),
        dash.dependencies.Input("right_infection_plot", "hoverData")
    ]
)
def highlight_trace(hover_curve, hover_trend):
    reset_infection_plots()
    if hover_curve:
        country_index = hover_curve["points"][0]["curveNumber"]
        country_name = [content["name"]
                        for index, content in enumerate(infection_curve.data)
                        if index == country_index][0]
        highlight_infection_plots(country_name)
    if hover_trend:
        country_index = hover_trend["points"][0]["curveNumber"]
        country_name = [content["name"]
                        for index, content in enumerate(infection_trend.data)
                        if index == country_index][0]
        highlight_infection_plots(country_name)
    return [infection_curve, infection_trend]


def reset_infection_plots():
    global infection_curve
    global infection_trend
    for country in infection_curve.data:
        country["line"]["width"] = styles.default.line_width
        country["opacity"] = styles.default.opacity
    for country in infection_trend.data:
        country["line"]["width"] = styles.default.line_width
        country["opacity"] = styles.default.opacity


def highlight_infection_plots(country: str):
    global infection_curve
    global infection_trend
    curve_index = [i for i, c in enumerate(infection_curve.data) if c["name"] == country]
    if curve_index:
        infection_curve.data[curve_index[0]]["line"]["width"] = styles.highlight.line_width
        infection_curve.data[curve_index[0]]["opacity"] = styles.highlight.opacity
    trend_index = [i for i, c in enumerate(infection_trend.data) if c["name"] == country]
    if trend_index:
        infection_trend.data[trend_index[0]]["line"]["width"] = styles.highlight.line_width
        infection_trend.data[trend_index[0]]["opacity"] = styles.highlight.opacity


if __name__ == '__main__':
    # TODO:
    #   - Refactor
    #   - Make trend line bolder
    #   - Add switches for deaths, confirmed cases
    #   - Add plot of latest country totals (+ mortality rates as text)
    #   - Add a world map with infections (should have animate button)
    #   - Add a switch to all plots to view confirmed cases or deaths
    #   - Link all plots (hover over a country shows it on other plots)
    #   - Create a new page for financial impact (to expand)
    #   - create a new page for travel impact (to expand)
    #   - Add lockdown annotations
    #   - Add device specific width settings
    #   - Look into free hosting options
    #   - Add app to the list of app on https://pomber.github.io/covid19
    PORT = config("PORT", default=8000, cast=int)
    app.run_server(debug=True, host="0.0.0.0", port=PORT)
