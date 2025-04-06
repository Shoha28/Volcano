from dash.dependencies import Input, Output, State
import dash
from dash import dcc, html
import plotly.graph_objects as go
from flask import Flask, render_template
from volcanoplot import volcano
from boxplot import render_boxplot


# Initialize Flask and Dash
server = Flask(__name__)
app = dash.Dash(__name__, server=server, url_base_pathname="/dashboard/")


# Layout
app.layout = html.Div([
    html.Div([
        dcc.Graph(id="volcano-plot", figure=volcano, style={"width": "100%", "height": "100vh", "overflow": "visible"}, config={
        'displayModeBar': False
    },),

        html.Div([
            dcc.Graph(id="selected-gene-plot", config={'displayModeBar': False}),
            html.Div(id="paper-title", style={"marginTop": "10px", "fontWeight": "bold"}),
            html.A("View Paper", id="paper-link", href="", target="_blank",
                   style={"display": "block", "marginTop": "5px"}),
            html.Button("Close", id="close-button", style={"marginTop": "10px", "display": "block"})
        ], id="overlay-graph", style={"display": "none"})
    ], style={"position": "relative", "maxWidth": "60vw", "maxHeight": "80vh", "margin": "0 auto"}),
])

# Callback for Showing/Hiding Graph
@app.callback(
    [
        Output("selected-gene-plot", "figure"),
        Output("overlay-graph", "style"),
        Output("paper-title", "children"),
        Output("paper-link", "href"),
    ],
    [
        Input("volcano-plot", "clickData"),
        Input("close-button", "n_clicks"),
    ],
    [State("overlay-graph", "style")]
)

# Function for opening a Boxplot
def toggle_overlay(clickData, close_clicks, current_style):
    ctx = dash.callback_context

    if ctx.triggered and ctx.triggered[0]["prop_id"].startswith("close-button"):
        return go.Figure(), {"display": "none"}, "", ""

    if clickData is None:
        return go.Figure(), {"display": "none"}, "", ""

    return render_boxplot(clickData)


# Flask route
@server.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    server.run(debug=True)