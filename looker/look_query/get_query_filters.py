import json
import looker_sdk

# This is the look we are going to run.
# You can get this from the URL (i.e. https://dashargos.chainargos.com/looks/722 -> 722)
LOOK_ID=722

# initialize connection
sdk = looker_sdk.init40("../looker.ini")

# look up this look
look = sdk.look(look_id=str(LOOK_ID))

# and print out
print(look.query.filters)
