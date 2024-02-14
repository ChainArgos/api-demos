import datetime
import looker_sdk

from looker.common.wrappers import create_query, run_query
from looker.tether_minting_vs_price.config import HISTORICAL_PRICES_LOOK_ID, TRON_MINTING_LOOK_ID, LOOKER_INI

looker = looker_sdk.init40(LOOKER_INI)

# get historical prices
look = looker.look(look_id=str(HISTORICAL_PRICES_LOOK_ID))
query_filter = {'google_sheet_tokens_to_import.symbol': 'WBTC'}
prices_q = create_query(looker, look.query, query_filter)
prices_df = run_query(looker, prices_q)

# find the earliest and latest dates in the series
# truncate to ensure list isn't too long for this demo
start_date = datetime.datetime.strptime(min(prices_df["Prices Trade Date Date"]), "%Y-%m-%d")
start_date = max(start_date, datetime.datetime(2023, 1, 1))
end_date = datetime.datetime.strptime(max(prices_df["Prices Trade Date Date"]), "%Y-%m-%d")

# now retrieve USDT minting on Tron for that time frame
look2 = looker.look(look_id=str(TRON_MINTING_LOOK_ID))
query_filter2 = {
    'tokens.symbol': 'USDT',
    'block_times.block_written_date': start_date.strftime("%Y/%m/%d") + ' to ' + end_date.strftime("%Y/%m/%d")
}
minting_q = create_query(looker, look2.query, query_filter2)
minting_df = run_query(looker, minting_q)

# now you can analyze these as usual...
