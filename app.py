"""Dash application"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from decouple import config
from flask import Flask

from covid19.plots.callbacks import reset_lines, find_selected_country, highlight_lines
from covid19.plots.infections import plot_infection_curve, plot_infection_trends, plot_infected_countries
from covid19.utils import get_app_dir, read_config

config_file = read_config()
app_dir = get_app_dir()

with open(str(app_dir / "assets" / "header.md")) as header_file:
    header_md = header_file.read()

infection_curve = plot_infection_curve()
infection_trend = plot_infection_trends()
infected_countries = plot_infected_countries()

server = Flask(__name__)
app = dash.Dash(__name__, server=server)
app.title = config_file["title"]
app.layout = html.Div(children=[
    html.H1(children=config_file["title"], className="title"),
    dcc.Markdown(header_md, className="desc"),
    html.Section(children=[
        dcc.Graph(figure=infected_countries, id="infected_countries", className="bar"),
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
def infection_plot_actions(hover_left, hover_right) -> [go.Figure, go.Figure]:
    hover_context = [(infection_curve, hover_left), (infection_trend, hover_right)]
    for figure, _ in hover_context:
        reset_lines(figure)
    if any([hover for _, hover in hover_context]):
        if country := find_selected_country(hover_context):
            for figure, _ in hover_context:
                highlight_lines(figure, country)
    return [infection_curve, infection_trend]


if __name__ == '__main__':
    # TODO:
    #   - Add plot of latest country totals (+ mortality rates as text)
    #   - Add a world map with infections
    #   - Arrange world map and bar plot
    #   - Animate world map and bar plot
    #   - Add a switch to all plots to view confirmed cases or deaths
    #   - Link all plots (hover over a country shows it on other plots)
    #   - Look into free hosting options
    #   - Add device specific width settings
    #   - Refactor
    #   - Add app to the list of app on https://pomber.github.io/covid19
    PORT = config("PORT", default=8000, cast=int)
    app.run_server(debug=True, host="0.0.0.0", port=PORT)
