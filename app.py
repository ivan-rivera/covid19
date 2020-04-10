"""Dash application"""
from logging import getLogger
from typing import List, Tuple

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from decouple import config
from flask import Flask

from covid19 import callbacks as cb, plots as p
from covid19.data import get_infection_data, filter_infection_data
from covid19.stats import build_summary_stats
from covid19.types import InfectionStatus
from covid19.utils import get_app_dir, read_config

logger = getLogger(__name__)

default_infection_status = InfectionStatus.CONFIRMED.value
config_file = read_config()
app_dir = get_app_dir()

with open(str(app_dir / "assets" / "header.md")) as header_file:
    header_md = header_file.read()

raw_infection_data = get_infection_data()
infection_data = filter_infection_data(raw_infection_data)
summary_data = build_summary_stats(infection_data)
graphic = p.Graphic(infection_data)
plots = graphic.figures[default_infection_status]


def generate_stats_panel() -> list:
    """Build a div with top level statistics"""
    panel_list = []
    for label in summary_data.__dict__:
        attribute = getattr(summary_data, label)
        entry = html.Div([
            html.H6(attribute.title),
            html.P(attribute.value_str, className="stat")
        ], id=attribute.id_str, className="mini_container")
        panel_list.append(entry)
    return panel_list


def generate_callback_params() -> Tuple[List[dash.dependencies.Output],
                                        List[dash.dependencies.Input]]:
    """Generate a list of inputs and outputs for the callback method"""
    output_deps, input_deps = [], []
    extra_inputs = [dash.dependencies.Input("radio_select", "value")]
    for v in plots.__dict__:
        if v not in ["data", "kind"]:
            viz = getattr(plots, v)
            output_deps.append(dash.dependencies.Output(viz.id_str, "figure"))
            input_deps.append(dash.dependencies.Input(viz.id_str, "hoverData"))
    for extra in extra_inputs:
        input_deps.append(extra)
    return output_deps, input_deps


server = Flask(__name__)
app = dash.Dash(__name__, server=server)
app.title = config_file["title"]
app.layout = html.Div(children=[
    html.Div(children=[
        html.Div([html.P(children=config_file["title"])], className="title"),
        html.Div([dcc.Markdown(header_md)], className="desc"),
        html.Div(children=[
            html.P("Select metric", id="selector_title"),
            dcc.RadioItems(id="radio_select",
                           labelStyle={"display": "table-row"},
                           options=[
                               {"label": "Cases", "value": InfectionStatus.CONFIRMED.value},
                               {"label": "Deaths", "value": InfectionStatus.DEATHS.value},
                           ], value=default_infection_status)
        ], className="select_container"),
    ], className="top_text"),
    html.Div(children=generate_stats_panel(), className="stat_panel"),
    html.Div(children=[
        html.Div(children=[
            dcc.Graph(figure=plots.map.figure, id=plots.map.id_str, clear_on_unhover=True),
            dcc.Graph(figure=plots.bars.figure, id=plots.bars.id_str, clear_on_unhover=True),
        ], className="left_side"),
        html.Div(children=[
            dcc.Graph(figure=plots.curve.figure, id=plots.curve.id_str, clear_on_unhover=True),
            html.Div(id="right_separator"),
            dcc.Graph(figure=plots.trend.figure, id=plots.trend.id_str, clear_on_unhover=True),
        ], className="right_side"),
    ], className="infection_graphs")
], className="dash_container")

fig_outputs, fig_inputs = generate_callback_params()


@app.callback(fig_outputs, fig_inputs)
def infection_plot_actions(hover_curve, hover_trend, hover_bars,
                           hover_map, radio_value) -> [go.Figure, go.Figure]:
    plot = graphic.figures[radio_value]
    hover_context = [(plot.curve, hover_curve), (plot.trend, hover_trend),
                     (plot.bars, hover_bars),   (plot.map, hover_map)]
    for fig, _, in hover_context:
        fig.reset(fig.figure)
    if any([h for _, h in hover_context]):
        logger.debug("highlight action triggered")
        if country := cb.find_selected_country(hover_context):
            for fig, _ in hover_context:
                fig.highlight(fig.figure, country)
    return [f.figure for f, _ in hover_context]


if __name__ == '__main__':
    # TODO:
    #   - test cases
    #   - Add app to the list of app on https://pomber.github.io/covid19
    PORT = config("PORT", default=8000, cast=int)
    logger.info(f"Launching the service on port {PORT}")
    app.run_server(debug=False, host="0.0.0.0", port=PORT)
