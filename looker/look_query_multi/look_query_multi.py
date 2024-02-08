from io import StringIO
import looker_sdk
import pandas as pd

LOOK_ID = 729
TOKEN = "USDT"
ADDRESS_LIST = [
    "TKo62ywGRK7vYXcpBavvmUmwKWgrPtw2Mx",
    "TFWry4G122VJdZNn9uX3HFZ64FeZR4WB13",
    "TRUzWMZnRseD3cZSKLGHvQ8yaiEyQtR2n5",
    "TGm1Kz7W5mWrKp6ibJQvGdG7pXwMg1K1k1",
    "TPXPXxf2rkXTBg1cJw4JfajmHNV8cPJ8B4",
]

# initialize connection
sdk = looker_sdk.init40("../looker.ini")

# look up this look
look = sdk.look(look_id=str(LOOK_ID))

# grab the query
query = look.query

# build the filter we want to use here
query_filter = {
    "tron_txns.to_address": ",".join(ADDRESS_LIST),
    "tokens.symbol": TOKEN,
}

# construct a new query based on the first one
new_query = sdk.create_query(
    body=looker_sdk.models40.WriteQuery(model=query.model,
                                        view=query.view,
                                        fields=query.fields,
                                        filters=query_filter)
)

# run it
df = pd.read_csv(StringIO(sdk.run_query(query_id=new_query.id, result_format='csv')))

print(str(df))
