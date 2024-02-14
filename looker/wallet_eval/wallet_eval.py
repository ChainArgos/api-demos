from io import StringIO
import looker_sdk
import pandas as pd

WALLET_LOOK_ID = 722
INFLOWS_LOOK_ID = 724
ADDRESS = "0x346eF244464679b031750f70D750B3FA65165443"

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
                                                                        pivots=base_query.pivots, total=base_query.total,
                                                                        row_total=base_query.row_total))
    return new_query

def run_query(sdk, query):
    return pd.read_csv(StringIO(sdk.run_query(query_id=query.id, result_format='csv')))

# now work out what fraction of which flows are from suspicious or other sorts of flows
# and generate the report
def is_suspicious_address(address, inflows, categories):
    this_categories = categories[address]
    this_label = inflows.loc[(inflows["Transactions From Address"] == address)]["From Wallet Labels"]
    if 'blacklisted' in this_categories or 'ofac' in this_categories or 'terrorists' in this_categories or 'darknet market' in categories:
        return True
    elif 'cex' in this_categories:
        # exchanges are not suspicious without one of the above tags
        return False
    elif 'suspicious' in this_categories:
        # this catches non-exchanges which don't have a specific suspicious tag
        return True
    return False

# compute total flows by token and number of flows by token
def compute_total_flows(inflows):
    addresses = inflows["Transactions From Address"].unique()
    tokens = inflows["Tokens Symbol"].unique()
    total = {}
    num = {}
    for token in tokens:
        total[token] = sum(inflows.loc[(inflows["Tokens Symbol"] == token)]["Transactions Sum of Transfer Amounts"])
        num[token] = len(inflows.loc[(inflows["Tokens Symbol"] == token)]["Transactions Sum of Transfer Amounts"])
    return total, num

def grab_wallet_categories(inflow_addresses, category_result):
    categories = {}
    for address in inflow_addresses:
        addr_rows = category_result.loc[(category_result["Wallets Address"] == address)]
        n_rows, _ = addr_rows.shape
        if n_rows > 0:
            res = " ;; ".join(addr_rows["Wallets Categories"].unique())
            categories[address] = list(set(res.split(" ;; ")))
        else:
            categories[address] = []
    return categories

def main():
    looker = looker_sdk.init40("../looker.ini")

    inflows = lookup_inflows(looker, ADDRESS)

    # grab inflow source addresses and labels
    inflow_addresses = inflows["Transactions From Address"].unique()
    tokens = inflows["Tokens Symbol"].unique()

    # now get categories for each inflow wallet
    category_result = lookup_address_categories(looker, inflow_addresses)
    categories = grab_wallet_categories(inflow_addresses, category_result)

    # we are now in a position to determine which inflows are suspicious, sanctioned or otherwise
    sus_addresses = []
    for address in inflow_addresses:
        if is_suspicious_address(address, inflows, categories):
            sus_addresses.append(address)

    total_amounts, total_xfers = compute_total_flows(inflows)
    sus_amounts, sus_xfers = compute_total_flows(inflows[inflows["Transactions From Address"].isin(sus_addresses)])

    header = ["token", "total inflow", "flagged inflow", "fraction flagged",
              "# inflows", "# flagged inflows", "fraction inflows flagged"]
    data = []
    for token in tokens:
        total_amt = total_amounts[token]
        sus_amt = sus_amounts[token]
        total_num = total_xfers[token]
        sus_num = sus_xfers[token]
        frac = sus_amt / total_amt
        frac_num = sus_num / total_num
        res_l = [token, total_amt, sus_amt, frac, total_num, sus_num, frac_num]
        data.append(res_l)

    out_dataframe = pd.DataFrame(data, columns=header)
    print(str(out_dataframe))

main()
