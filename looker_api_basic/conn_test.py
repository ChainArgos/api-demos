import looker_sdk
sdk = looker_sdk.init40("../looker_dashboard/looker.ini")
#conn = sdk.connection("test")
res = sdk.all_boards()
print(str(res))
print(str(len(res)))