"""Dash application"""
from copy import deepcopy

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from decouple import config
from flask import Flask

from covid19.data import get_infection_data, filter_infection_data
from covid19.plots.callbacks import (
    reset_lines,
    reset_bars,
    reset_map,
    find_selected_country,
    highlight_lines,
    highlight_bars,
    highlight_map
)
from covid19.plots.infections import (
    plot_infection_curve,
    plot_infection_trends,
    plot_infected_countries,
    plot_infection_map,
)
from covid19.stats import build_summary_stats
from covid19.types import Plot
from covid19.utils import get_app_dir, read_config

config_file = read_config()
app_dir = get_app_dir()

with open(str(app_dir / "assets" / "header.md")) as header_file:
    header_md = header_file.read()

radio_button_state = "confirmed"

raw_infection_data = get_infection_data()
infection_data = filter_infection_data(raw_infection_data)
summary_data = build_summary_stats(infection_data)

plots_deaths = Plot(
    curve=plot_infection_curve(infection_data, "deaths"),
    trend=plot_infection_trends(infection_data, "deaths"),
    bars=plot_infected_countries(infection_data, "deaths"),
    map=plot_infection_map(infection_data, "deaths")
)

plots_confirmed = Plot(
    curve=plot_infection_curve(infection_data),
    trend=plot_infection_trends(infection_data),
    bars=plot_infected_countries(infection_data),
    map=plot_infection_map(infection_data)
)

plot_set = {
    "confirmed": plots_confirmed,
    "deaths": plots_deaths
}

plots = deepcopy(plots_confirmed)


callbacks = {
    "lines": {"highlight": highlight_lines, "reset": reset_lines},
    "bars": {"highlight": highlight_bars, "reset": reset_bars},
    "map": {"highlight": highlight_map, "reset": reset_map},
}

server = Flask(__name__)
app = dash.Dash(__name__, server=server)
app.title = config_file["title"]
app.layout = html.Div(children=[
    html.Div(children=[
        html.P(children=config_file["title"], className="title"),
        dcc.Markdown(header_md, className="desc"),
        html.Div(children=[
            html.P("Select metric", id="selector_title"),
            dcc.RadioItems(id="radio_select",
                           labelStyle={"display": "table-row"},
                           options=[
                               {"label": "Cases", "value": "confirmed"},
                               {"label": "Deaths", "value": "deaths"},
                           ], value=radio_button_state)
        ], className="select_container"),
    ], className="top_text"),
    html.Div(children=[
        html.Div([html.H6("Last update"), html.P(summary_data["last update"])],
                 id="last_update", className="mini_container"),
        html.Div([html.H6("Global cases"), html.P(summary_data["total cases"])],
                 id="total_cases", className="mini_container"),
        html.Div([html.H6("Global deaths"), html.P(summary_data["total deaths"])],
                 id="total_deaths", className="mini_container"),
        html.Div([html.H6("Mortality rate"), html.P(summary_data["mortality rate"])],
                 id="mortality_rate", className="mini_container"),
        html.Div([html.H6("Growth yesterday"), html.P(summary_data["global growth"])],
                 id="growth_rate", className="mini_container"),
    ], className="stat_panel"),
    html.Div(children=[
        html.Div(children=[
            dcc.Graph(figure=plots.map, id="infection_map", clear_on_unhover=True),
            dcc.Graph(figure=plots.bars, id="infected_countries", clear_on_unhover=True),
        ], className="left_side"),
        html.Div(children=[
            dcc.Graph(figure=plots.curve, id="infection_curve", clear_on_unhover=True),
            html.Div(id="right_separator"),
            dcc.Graph(figure=plots.trend, id="infection_trend", clear_on_unhover=True),
        ], className="right_side"),
    ], className="infection_graphs")
])


@app.callback(
    [
        dash.dependencies.Output("infection_curve", "figure"),
        dash.dependencies.Output("infection_trend", "figure"),
        dash.dependencies.Output("infected_countries", "figure"),
        dash.dependencies.Output("infection_map", "figure"),
    ],
    [
        dash.dependencies.Input("infection_curve", "hoverData"),
        dash.dependencies.Input("infection_trend", "hoverData"),
        dash.dependencies.Input("infected_countries", "hoverData"),
        dash.dependencies.Input("infection_map", "hoverData"),
        dash.dependencies.Input("radio_select", "value"),
    ]
)
def infection_plot_actions(
        hover_curve,
        hover_trend,
        hover_bars,
        hover_map,
        radio_value,
) -> [go.Figure, go.Figure]:
    global radio_button_state
    if radio_value != radio_button_state:
        radio_button_state = radio_value
        plots.bars = plot_set[radio_value].bars
        plots.map = plot_set[radio_value].map
        plots.curve = plot_set[radio_value].curve
        plots.trend = plot_set[radio_value].trend
    hover_context = [
        (plots.curve, hover_curve, "lines"),
        (plots.trend, hover_trend, "lines"),
        (plots.bars, hover_bars, "bars"),
        (plots.map, hover_map, "map"),
    ]
    for figure, _, kind in hover_context:
        callbacks[kind]["reset"](figure)
    if any([h for _, h, _ in hover_context]):
        if country := find_selected_country(hover_context):
            for fig, _, kind in hover_context:
                callbacks[kind]["highlight"](fig, country)
    return [p for p, _, _ in hover_context]


if __name__ == '__main__':
    # TODO:
    #   - try to speed it up
    #   - fill country gaps
    #   - Validate numbers
    #   - Make it pretty
    #   - add logger statements
    #   - Refactor
    #   - test cases
    #   - QA
    #   - Add app to the list of app on https://pomber.github.io/covid19
    PORT = config("PORT", default=8000, cast=int)
    app.run_server(debug=False, host="0.0.0.0", port=PORT)
