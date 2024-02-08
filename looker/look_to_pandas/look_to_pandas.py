from io import StringIO
import looker_sdk
import pandas as pd

# This is the look we are going to run.
# You can get this from the URL (i.e. https://dashargos.chainargos.com/looks/722 -> 722)
LOOK_ID=722

# initialize connection
sdk = looker_sdk.init40("../looker.ini")

# run look with csv results
look_results = sdk.run_look(look_id=str(LOOK_ID), result_format="csv")

# csv to pandas
df = pd.read_csv(StringIO(look_results))

# print it out
print(str(df))
