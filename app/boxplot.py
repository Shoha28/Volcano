import pandas as pd

# Extract excel data into a numpy array
S4AData = pd.read_excel("../data/NIHMS1635539-supplement-1635539_Sup_tab_4.xlsx", sheet_name="S4A values")

donor_info = S4AData.values[1, 18:]
data_values = S4AData.values[2:, :]

YD_columns = []
OD_columns = []
for i in range(len(donor_info)):
    if "YD" in donor_info[i]:  # Check if "YD" is in the string
        YD_columns.append(i)
    elif "OD" in donor_info[i]:
        OD_columns.append(i)

protein_dict = {}

# Iterate over rows to populate the dictionary
for i in range(len(data_values)):
    protein_name = data_values[i][7]

    young_donors = []
    old_donors = []
    for j in YD_columns:
        young_donors.append(data_values[i][j+18])
    for j in OD_columns:
        old_donors.append(data_values[i][j+18])

    protein_dict[protein_name] = {"Young": young_donors, "Old": old_donors}







