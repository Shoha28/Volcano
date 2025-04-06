import pandas as pd
import plotly.graph_objects as go
import requests
from flask import jsonify

# Extract excel data into a numpy array
S4AData = pd.read_excel("../data/NIHMS1635539-supplement-1635539_Sup_tab_4.xlsx", sheet_name="S4A values")

donor_info = S4AData.values[1, 18:]
data_values = S4AData.values[2:, :]

# Create a dict with protein names as keys, each of them assigned an "Old Donors" and a "Young Donors" list

YD_columns = []
OD_columns = []
for i in range(len(donor_info)):
    if "YD" in donor_info[i]:
        YD_columns.append(i)
    elif "OD" in donor_info[i]:
        OD_columns.append(i)

gene_dict = {}

for i in range(len(data_values)):
    gene_name = data_values[i][7]

    young_donors = []
    old_donors = []
    for j in YD_columns:
        young_donors.append(data_values[i][j+18])
    for j in OD_columns:
        old_donors.append(data_values[i][j+18])

    gene_dict[gene_name] = {"Young": young_donors, "Old": old_donors}

def render_boxplot(clickData):
    gene_name = clickData["points"][0]["customdata"]

    young_data = [float(val) for val in gene_dict[gene_name]["Young"]]
    old_data = [float(val) for val in gene_dict[gene_name]["Old"]]

    # Create a figure with two boxplots
    mini_plot = go.Figure()

    mini_plot.add_trace(go.Box(
        y=young_data,
        name="Young Donors",
        marker_color="blue"
    ))

    mini_plot.add_trace(go.Box(
        y=old_data,
        name="Old Donors",
        marker_color="red"
    ))

    mini_plot.update_layout(
        title=f"Expression Levels for {gene_name}",
        xaxis_title="Condition",
        yaxis_title="Expression",
        showlegend=True,
        xaxis=dict(
            tickmode="array",
            tickvals=[0, 1],
            ticktext=["Young", "Old"],
        ),
        height=500,
        width=500,
        autosize=True
    )

    title, url = fetch_gene_data(gene_name)

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
    }, title, url


def fetch_gene_data(gene_name):
    # Getting the protein ID
    url1 = f"https://mygene.info/v3/query?q=symbol:{gene_name}"
    response1 = requests.get(url1)
    gene_id = response1.json()['hits'][0]['_id']

    url2 = f"https://mygene.info/v3/gene/{gene_id}"
    response2 = requests.get(url2)
    pubmed_id = response2.json()['generif'][0]['pubmed']

    pubmed_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    params = {
        "db": "pubmed",
        "id": pubmed_id,
        "retmode": "json"
    }

    response = requests.get(pubmed_url, params=params)
    data = response.json()

    title = data["result"][str(pubmed_id)]["title"]

    return [f"Mentioned in: {title}", f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/"]



