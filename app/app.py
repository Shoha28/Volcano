import numpy as np
import pandas as pd
from flask import Flask, render_template
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import dash
from dash import dcc, html

# Extract excel data into a numpy array
xlData = pd.read_excel("../data/NIHMS1635539-supplement-1635539_Sup_tab_4.xlsx", sheet_name="S4B limma results")
xlDataArray = xlData.values[2:]

# Take the fold change and adjusted p values
# For the sake of the volcano plot, the p values are mapped to their corresponding negative log10 values, the FC values are unchanged as they are already in log 2
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

# Initialize Flask and connect it to Dash
server = Flask(__name__)

app = dash.Dash(__name__, server=server, url_base_pathname="/dashboard/")


# Creating the plot with FigureWidget
fig = go.FigureWidget(
    data=[
        go.Scatter(
            x=df["FoldChange"],
            y=df["neg_log10_pval"],
            mode="markers",
            marker=dict(size=8, color="blue"),
            customdata=df["Gene"],  # Pass Gene names for hover/click
            hovertemplate="<b>Fold Change:</b> %{x}<br><b>-Log10 P-Value:</b> %{y}<br><b>Gene:</b> %{customdata}<extra></extra>"
        )
    ]
)

# Rendering into html
app.layout = html.Div([
    html.H1("Interactive Volcano Plot"),
    dcc.Graph(id="volcano-plot", figure=fig),
    html.Div(id="click-output", style={"fontSize": "20px", "marginTop": "20px"})
])


# Making the plot clickable
@app.callback(
    Output("click-output", "children"),
    Input("volcano-plot", "clickData")
)
def display_click_data(clickData):
    if clickData is None:
        return "Click on a point to see details."

    gene_name = clickData["points"][0]["customdata"]

    return f" Gene name: {gene_name}"


# Flask route to serve the page
@server.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    server.run(debug=True)