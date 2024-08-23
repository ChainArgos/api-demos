import looker_sdk

from looker.wallet_eval.helpers import create_query, run_query

looker = looker_sdk.init40("../looker.ini")

ADDRESS = [
    "0x346eF244464679b031750f70D750B3FA65165443",
    "0x9ed891f6b3209c3f3c6906bafdd2e8d89afd45a0"
]

TOKENS = [
    "ETH",
    "USDC",
    "USDT"
]

INFLOWS_LOOK_ID = 724

look = looker.look(look_id=str(INFLOWS_LOOK_ID))
query_filter = {
    "ethereum_txns.to_address": ",".join(ADDRESS),
    "tokens.symbol": ",".join(TOKENS),
}

q = create_query(looker, look.query, query_filter)
result = run_query(looker, q)
print(result)
