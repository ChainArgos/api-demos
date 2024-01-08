import pandas as pd

# the document ID and which sheet
DOC_ID = '1ZCqciEB89y5TF1j6BrthgMGUTc62CVa0vMp97dJKCPY'
DOC_SHEET = 'Table'

# turn this in to a URL that dumps a csv file
SHEET_URI = 'https://docs.google.com/spreadsheets/d/' + DOC_ID + '/gviz/tq?tqx=out:csv&sheet=' + DOC_SHEET

df = pd.read_csv(SHEET_URI, low_memory=False).fillna(0)

columns = df.columns
for i in df.index:
    this_tag = str(df.loc[i, "Sum of Transfer Amounts Labels"])[0:50]
    print("flow out of addresses tagged as " + this_tag + " totalled " + str(df.loc[i, "Symbol USDC"]))
