import numpy as np
import pandas as pd

# Extract excel data into a numpy array
S4AData = pd.read_excel("../data/NIHMS1635539-supplement-1635539_Sup_tab_4.xlsx", sheet_name="S4A values")
S4ADataColumns = S4AData.values[1]
S4ADataArray = S4AData.values[2:]
print(S4ADataArray[0], S4ADataArray[1], S4ADataColumns)