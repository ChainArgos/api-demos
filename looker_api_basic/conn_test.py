import looker_sdk
sdk = looker_sdk.init40("looker.ini")
boards = sdk.all_boards()
for board in boards:
    print(str(board))