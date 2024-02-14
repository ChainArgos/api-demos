import looker_sdk
import pandas as pd

from looker.wallet_eval.config import ADDRESS
from looker.wallet_eval.helpers import lookup_address_categories, lookup_inflows, grab_wallet_categories
from looker.wallet_eval.is_suspicious import is_suspicious_address


# work out what fraction of which flows are from suspicious or other sorts of flows

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
