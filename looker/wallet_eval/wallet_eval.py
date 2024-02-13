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
inflow_addresses = {}
categories = {}
n_rows, _ = inflows.shape
for row in range(n_rows):
    addr = inflows.loc[row].at["Transactions From Address"]
    label = inflows.loc[row].at["From Wallet Labels"]
    inflow_addresses[addr] = label
    categories[addr] = []

# now get categories for each inflow wallet
address_q = lookup_address_categories(looker, inflow_addresses)
n_categories, _ = address_q.shape
for row in range(n_categories):
    categories[address_q.loc[row].at["Wallets Address"]] = address_q.loc[row].at["Wallets Categories"].split(" ;; ")

# we are now in a position to determine which inflows are suspicious, sanctioned or otherwise
