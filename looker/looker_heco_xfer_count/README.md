# Heco HRC-20 transaction count histogram

This example computes a per-day histogram of the number of HRC-20 transactions per block on Heco.
We do this in 3 steps:
1. For each date run a look that gives us per-block transaction counts for non-empty blocks
2. Fill in the 0s for empty blocks.
3. Convert data into to numpy format and run the histograms.

Data is printed out in a csv format suitable for charting in a spreadsheet.

{% @github-files/github-code-block url="https://github.com/ChainArgos/api-demos/blob/main/looker/looker_heco_xfer_count/heco_histogram.py" %}
