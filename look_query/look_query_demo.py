import json
import looker_sdk

## CONFIG

# This is the address to look up
BLACKLISTED_ADDRESS = '0x3b76a3699b563ad1af98ad581714c72315c83607'

# This is the look we are going to run.
# You can get this from the URL (i.e. https://dashargos.chainargos.com/looks/722 -> 722)
LOOK_ID=722

# This is the filter we want to set.
# While editing the look if you hover over the circled-i next to the relevant dimension
# this is given under "NAME"
FILTER_TITLE='address'

## BEGIN DEMO CODE

# initialize connection
sdk = looker_sdk.init40("looker.ini")

# look up this look
look = sdk.look(look_id=str(LOOK_ID))

# grab the query
query = look.query

# build the filter we want to use here
query_filter = {
    query.view + "." + FILTER_TITLE: BLACKLISTED_ADDRESS
}

# construct a new query based on the first one
new_query = sdk.create_query(
    body=looker_sdk.models40.WriteQuery(model=query.model,
                                        view=query.view,
                                        fields=query.fields,
                                        filters=query_filter)
)

# run it
result_raw = sdk.run_query(query_id=new_query.id, result_format='json')
result = json.loads(result_raw)

# print results
assert len(result) == 1
for k, v in result[0].items():
    print(str(k) + " : " + str(v))
