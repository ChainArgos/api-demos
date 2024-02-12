import datetime
from io import StringIO
import looker_sdk
import numpy as np
import pandas as pd

LOOK_ID = 732

# initialize connection
sdk = looker_sdk.init40("../looker.ini")

# look up this look
look = sdk.look(look_id=str(LOOK_ID))

# grab the query
query = look.query

start_date = datetime.datetime(2023, 12, 1)
end_date = datetime.datetime(2024, 2, 12)
df_by_date = {}
cur_date = start_date
while cur_date < end_date:
    # build the filter we want to use here
    query_filter = {"block_times.block_written_date": cur_date.strftime("%Y/%m/%d")}

    # construct a new query based on the first one
    new_query = sdk.create_query(body=looker_sdk.models40.WriteQuery(model=query.model, view=query.view,
                                                                     fields=query.fields, filters=query_filter))

    # run it
    df = pd.read_csv(StringIO(sdk.run_query(query_id=new_query.id, result_format='csv')))
    df_by_date[cur_date] = df

    cur_date += datetime.timedelta(days=1)

all_blocks = {}
max_count = 0
for dt in df_by_date:
    df = df_by_date[dt]
    rows, cols = df.shape
    all_blocks[dt] = {}
    for row in range(rows):
        block_number = df.loc[row].at["Block Times Block Number"]
        this_count = df.loc[row].at["Transactions Number of Unique Txns"]
        all_blocks[dt][block_number] = this_count
        if this_count > max_count:
            max_count = this_count

for dt in df_by_date:
    min_block = min(all_blocks[dt].keys())
    max_block = max(all_blocks[dt].keys())
    for block in range(min_block, max_block):
        if block not in all_blocks[dt]:
            all_blocks[dt][block] = 0

# histogram by date
hist_values = {}
big_edges = None
for dt in df_by_date:
    this_hist, bin_edges = np.histogram(list(all_blocks[dt].values()), bins=100, range=(0.0, float(max_count)))
    hist_values[dt] = this_hist

print(",".join([str(x) for x in list(bin_edges)]))
for dt in hist_values:
    l = [dt.strftime("%Y/%m/%d")]
    l.extend([str(x) for x in list(hist_values[dt])])
    print(",".join(l))
