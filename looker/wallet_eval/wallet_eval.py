from io import StringIO
import looker_sdk
import pandas as pd

WALLET_LOOK_ID = 722
LOOK_ID = 724

#ADDRESS = "0x1b4423364623A4DEffA335413343122194f967F7"
ADDRESS = "0x346eF244464679b031750f70D750B3FA65165443"


def lookup_address_categories(looker, address_list: str):
    look = looker.look(look_id=str(WALLET_LOOK_ID))
    query = look.query
    query_filter = {"wallets.address": ",".join(address_list)}
    q = create_query(looker, query, query_filter)
    return run_query(looker, q)


def lookup_inflows(looker, address: str):
    look = looker.look(look_id=str(LOOK_ID))
    query = look.query
    query_filter = {"ethereum_txns.to_address": address}
    q = create_query(looker, query, query_filter)
    return run_query(looker, q)


def create_query(looker, base_query, query_filter):
    new_query = looker.create_query(body=looker_sdk.models40.WriteQuery(model=base_query.model, view=base_query.view,
                                                                     fields=base_query.fields, filters=query_filter,
                                                                     pivots=base_query.pivots, total=base_query.total,
                                                                     row_total=base_query.row_total))
    return new_query


def run_query(sdk, q):
    return pd.read_csv(StringIO(sdk.run_query(query_id=q.id, result_format='csv')))


looker = looker_sdk.init40("../looker.ini")

inflows = lookup_inflows(looker, ADDRESS)

# grab inflow source addresses and labels
inflow_addresses = inflows["Transactions From Address"].unique()
tokens = inflows["Tokens Symbol"].unique()

# compute total inflow by token
inflow_totals = {}
for token in tokens:
    inflow_totals[token] = sum(inflows.loc[(inflows["Tokens Symbol"] == token)]["Transactions Sum of Transfer Amounts"])

# now get categories for each inflow wallet
category_result = lookup_address_categories(looker, inflow_addresses)
categories = {}
for address in inflow_addresses:
    addr_rows = category_result.loc[(category_result["Wallets Address"] == address)]
    n_rows, _ = addr_rows.shape
    if n_rows > 0:
        res = " ;; ".join(addr_rows["Wallets Categories"].unique())
        categories[address] = list(set(res.split(" ;; ")))
    else:
        categories[address] = []

# we are now in a position to determine which inflows are suspicious, sanctioned or otherwise
per_address_flow_amounts = {}
for address in inflow_addresses:
    this_categories = categories[address]
    per_address_flow_amounts[address] = {}
    for token in tokens:
        this_inflows = inflows.loc[(inflows["Tokens Symbol"] == token) & (inflows["Transactions From Address"] == address)]
        n_rows, _ = this_inflows.shape
        per_address_flow_amounts[address][token] = sum(this_inflows["Transactions Sum of Transfer Amounts"])

# now work out what fraction of which flows are from suspicious or other sorts of flows
# and generate the report
