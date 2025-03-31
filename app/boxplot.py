import pandas as pd
import plotly.graph_objects as go

# Extract excel data into a numpy array
S4AData = pd.read_excel("../data/NIHMS1635539-supplement-1635539_Sup_tab_4.xlsx", sheet_name="S4A values")
S4ADataColumns = S4AData.values[1]
S4ADataArray = S4AData.values[2:]


def on_point_click(trace, points, state):

    # boxplot_fig = go.FigureWidget()
    # Retrieve the gene name directly from the clicked point's customdata
    clicked_gene = points.customdata[0]  # Get the gene name from customdata
    print(clicked_gene)


