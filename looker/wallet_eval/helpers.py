from io import StringIO

import looker_sdk
import pandas as pd

from looker.wallet_eval.config import WALLET_LOOK_ID, INFLOWS_LOOK_ID, WALLETS_ADDRESS, WALLETS_CATEGORIES


def lookup_address_categories(looker, address_list: str):
    look = looker.look(look_id=str(WALLET_LOOK_ID))
    query_filter = {"wallets.address": ",".join(address_list)}
    q = create_query(looker, look.query, query_filter)
    return run_query(looker, q)


def lookup_inflows(looker, address: str):
    look = looker.look(look_id=str(INFLOWS_LOOK_ID))
    query_filter = {"ethereum_txns.to_address": address}
    q = create_query(looker, look.query, query_filter)
    return run_query(looker, q)


def create_query(looker, base_query, query_filter):
    new_query = looker.create_query(body=looker_sdk.models40.WriteQuery(model=base_query.model, view=base_query.view,
                                                                        fields=base_query.fields, filters=query_filter,
                                                                        pivots=base_query.pivots,
                                                                        total=base_query.total,
                                                                        row_total=base_query.row_total))
    return new_query


def run_query(sdk, query):
    return pd.read_csv(StringIO(sdk.run_query(query_id=query.id, result_format='csv')))


def grab_wallet_categories(inflow_addresses, category_result):
    categories = {}
    for address in inflow_addresses:
        addr_rows = category_result.loc[(category_result[WALLETS_ADDRESS] == address)]
        n_rows, _ = addr_rows.shape
        if n_rows > 0:
            res = " ;; ".join(addr_rows[WALLETS_CATEGORIES].unique())
            categories[address] = list(set(res.split(" ;; ")))
        else:
            categories[address] = []
    return categories
