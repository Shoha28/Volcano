from dash.dependencies import Input, Output, State
import dash
from dash import dcc, html
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from flask import Flask, render_template
from boxplot import protein_dict

# Extract excel data into a numpy array
xlData = pd.read_excel("../data/NIHMS1635539-supplement-1635539_Sup_tab_4.xlsx", sheet_name="S4B limma results")
xlDataArray = xlData.values[2:]

# Take the fold change and adjusted p values
FCValues = pd.to_numeric(xlDataArray[:, 1])
adjPVal = pd.to_numeric(xlDataArray[:, 5])
gene_names = xlDataArray[:, 9]
neg_log10_pval = -np.log10(adjPVal)

# Combine values into a DataFrame
df = pd.DataFrame({
    "Gene": gene_names,
    "FoldChange": FCValues,
    "neg_log10_pval": neg_log10_pval
})

# Initialize Flask and Dash
server = Flask(__name__)
app = dash.Dash(__name__, server=server, url_base_pathname="/dashboard/")

# Main Plot
fig = go.FigureWidget(
    data=[go.Scatter(
        x=df["FoldChange"],
        y=df["neg_log10_pval"],
        mode="markers",
        marker=dict(size=8, color="blue"),
        customdata=df["Gene"],
        hovertemplate="<b>Fold Change:</b> %{x}<br><b>-Log10 P-Value:</b> %{y}<br><b>Gene:</b> %{customdata}<extra></extra>"
    )]
)

# Layout
app.layout = html.Div([

    html.Div([
        dcc.Graph(id="volcano-plot", figure=fig, style={"width": "100%", "height": "100vh", "overflow": "visible"}),

        # Small Overlay Graph
        html.Div([
            dcc.Graph(id="selected-gene-plot"),
            html.Button("Close", id="close-button", style={"marginTop": "10px", "display": "block"})
        ], id="overlay-graph", style={"display": "none"})  # Hidden initially
    ], style={"position": "relative", "maxWidth": "60vw", "margin": "0 auto"}),


])

# Callback for Showing/Hiding Graph

@app.callback(
    [Output("selected-gene-plot", "figure"),
     Output("overlay-graph", "style")],
    [Input("volcano-plot", "clickData"),
     Input("close-button", "n_clicks")],
    [State("overlay-graph", "style")]  # Keeps track of overlay state
)
def toggle_overlay(clickData, close_clicks, current_style):
    ctx = dash.callback_context

    if ctx.triggered and ctx.triggered[0]["prop_id"].startswith("close-button"):
        return go.Figure(), {"display": "none"}

    if clickData is None:
        return go.Figure(), {"display": "none"}

    protein_name = clickData["points"][0]["customdata"]

    young_data = [float(val) for val in protein_dict[protein_name]["Young"]]
    old_data = [float(val) for val in protein_dict[protein_name]["Old"]]


    # Create a figure with two boxplots
    mini_plot = go.Figure()

    mini_plot.add_trace(go.Box(
        y=young_data,
        name="Young",
        marker_color="blue"
    ))

    mini_plot.add_trace(go.Box(
        y=old_data,
        name="Old",
        marker_color="red"
    ))

    mini_plot.update_layout(
        title=f"Expression Levels for {protein_name}",
        xaxis_title="Condition",
        yaxis_title="Expression Level",
        showlegend=True,
        xaxis=dict(
            tickmode="array",
            tickvals=[0, 1],
            ticktext=["Young", "Old"],
        ),
        height=500,  # Specify a height for the plot itself (in pixels)
        width=500,  # Specify a width for the plot itself (in pixels)
        autosize=True
    )


    return mini_plot, {
        "display": "block",
        "position": "fixed",
        "top": "50%",
        "left": "50%",
        "transform": "translate(-50%, -50%)",
        "background": "white",
        "border": "2px solid black",
        "padding": "10px",
        "boxShadow": "0 4px 10px rgba(0, 0, 0, 0.3)",
        "zIndex": 1000
    }

# Flask route
@server.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    server.run(debug=True)