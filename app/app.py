import numpy as np
import pandas as pd
from flask import Flask, render_template
import plotly.express as px
import plotly.io as pio

# Extract excel data into a numpy array
xlData = pd.read_excel("../data/NIHMS1635539-supplement-1635539_Sup_tab_4.xlsx", sheet_name="S4B limma results")
xlDataArray = xlData.values[2:]

# Take the fold change and adjusted p values
# For the sake of the volcano plot, the p values are mapped to their corresponding negative log10 values, the FC values are unchanged as they are already in log 2
FCValues = pd.to_numeric(xlDataArray[:, 1])
adjPVal = pd.to_numeric(xlDataArray[:, 5])

neg_log10_pval = -np.log10(adjPVal)

# Initialize Flask app
app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_data():
    # Creating the graph
    fig = px.scatter(
        x=FCValues,
        y=neg_log10_pval,
        labels={"x": "Log2 Fold Change", "y": "-Log10 Adjusted P-Value"},
    ).update_layout(
        # xaxis=dict(range=[-2, 2]),
        xaxis_title="Log2 Fold Change",
        yaxis_title="-Log10 Adjusted P-Value",
        title="Volcano Plot",
        template="plotly_white",
        showlegend=False
    )

    # Rendering graph with HTML
    graph_html = pio.to_html(fig, full_html=False)

    return render_template('index.html', graph_html=graph_html)

if __name__ == "__main__":
    app.run(debug=True)