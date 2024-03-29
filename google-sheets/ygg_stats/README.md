# Compute statistics on YGG flows

Here we compute statistics on per-day YGG outflows across all active wallets.

Generates a csv for a stacked bar chart across dates for fraction of outflows by wallet
for each date compute the fraction of on-chain outflow for each 1/steps fraction of wallets
starting from the largest.

If all the outflow is from a single wallet the stacked bar chart will have 1 value per bar
if it is evenly distributed over 1/steps wallets you will get an even stack of n_steps.

The csv can be used for a stacked bar chart in Excel, OpenOffice and the like.
You probably want to skip the first column with total outflow on that date.

The Google Sheet [here](https://docs.google.com/spreadsheets/d/1ksitF87TXLb48yLZUqJrv1PwZ9UHGdGPcpAgIa5eYMw/)
is used by the code.
That sheet is publicly viewable (as this is a demo).

## Details

### Code

{% @github-files/github-code-block url="https://github.com/ChainArgos/api-demos/blob/main/google-sheets/ygg_stats/example.py" %}

### CSV Data
An example interim csv output is [here](https://github.com/ChainArgos/api-demos/blob/37e3d1d53a7b17a8f88552b3511febcb13fb1387/ygg_stats/data.csv).

### Final Spreadsheet
And one aggregation into a spreadsheet is [here](https://github.com/ChainArgos/api-demos/blob/f81cc3d88cc6527575cc260f182790d913a4dcf8/ygg_stats/stacked_bar_ygg.ods).
