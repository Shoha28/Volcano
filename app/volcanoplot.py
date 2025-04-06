import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Import excel data
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

volcano = go.FigureWidget(
    data=[go.Scatter(
        x=df["FoldChange"],
        y=df["neg_log10_pval"],
        mode="markers",
        marker=dict(size=8, color="blue"),
        customdata=df["Gene"],
        hovertemplate="<b>Fold Change:</b> %{x}<br><b>-Log10 P-Value:</b> %{y}<br><b>Gene:</b> %{customdata}<extra></extra>"
    )]
)