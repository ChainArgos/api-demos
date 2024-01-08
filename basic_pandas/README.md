# Largest Senders of USDC on Base

This is a simple demo that extracts the largest senders of USDC on Base.

A Google Sheet [here](https://docs.google.com/spreadsheets/d/1ZCqciEB89y5TF1j6BrthgMGUTc62CVa0vMp97dJKCPY/)
pulls data from the back end.
And this code extracts data from there.

The sheet is configured to update hourly, look at the last 90 calendar days and
only return wallets with a total flow over US$ 1 million.
Those parameters are all visible within the sheet.

GitHub code [here](https://github.com/ChainArgos/api-demos/blob/main/basic_pandas/basic_pandas.py) on GitHub.
