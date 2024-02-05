import looker_sdk
sdk = looker_sdk.init40("looker.ini")
boards = sdk.all_dashboards()
for board in boards:
    print(str(board.title) + ' , ' + str(board.id))