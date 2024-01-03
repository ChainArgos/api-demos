"""
api demo for ygg flows
"""
import datetime
from functools import cmp_to_key
from locale import atof
import pandas as pd

# comparator for (wallet, outflow) tuples
def cmp(a, b):
    if a[1] < b[1]:
        return 1
    elif a[1] == b[1]:
        return 0
    else:
        return -1

# the document ID and which sheet
DOC_ID = '1ksitF87TXLb48yLZUqJrv1PwZ9UHGdGPcpAgIa5eYMw'
DOC_SHEET = 'Stats_Pivot'

# number of steps for wallet outflow tranching
N_STEPS = 100

# turn this in to a URL that dumps a csv file
SHEET_URI = 'https://docs.google.com/spreadsheets/d/' + DOC_ID + '/gviz/tq?tqx=out:csv&sheet=' + DOC_SHEET

df = pd.read_csv(SHEET_URI, low_memory=False).fillna(0)
as_np = df.to_numpy()

r, c = as_np.shape

date_column_map = {}
per_date_total = {}
per_date_amounts = {}
for i in range(c):
    if i == 0:
        assert (as_np[0][i] == "From Label or Address")
    else:
        this_date = datetime.datetime.strptime(as_np[0][i], "%m/%d/%Y")
        date_column_map[this_date] = i
        per_date_total[this_date] = 0.0
        per_date_amounts[this_date] = []
        for j in range(1, r):
            this_label = as_np[j][0]
            if as_np[j][i] != 0:
                this_amount = atof(as_np[j][i])
                per_date_total[this_date] += this_amount
                per_date_amounts[this_date].append((this_label, this_amount))

fractions = [(i+1)/float(N_STEPS) for i in range(N_STEPS)]
print(','.join(['date', 'total'] + [str(x) for x in fractions]))
for date in per_date_amounts:
    s = sorted(per_date_amounts[date], key=cmp_to_key(cmp))
    n = len(s)
    v_l = [date.strftime("%Y/%m/%d"), str(per_date_total[date])]
    values = []
    this_total = per_date_total[date]
    for f in fractions:
        v = 0
        for i in range(max(1, int(n*f))):
            v += s[i][1]/this_total
        values.append(v)
    # now values contains totals, we want incremental for a stacked bar chart
    values_stackable = []
    values_stackable.append(values[0])
    for i in range(1, len(fractions)):
        values_stackable.append(values[i] - values[i-1])
    print(','.join(v_l + [str(x) for x in values_stackable]))
