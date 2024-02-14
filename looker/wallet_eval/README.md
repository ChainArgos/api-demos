# Wallet evaluation example

This example shows how to do basic wallet inflows analysis.
Here we are building an entirely open-source analyzer.
You can see exactly how numbers are calculated, change the rules to your liking or add new ones.

For this demo set the address of interest here:
{% @github-files/github-code-block url="https://github.com/ChainArgos/api-demos/blob/main/looker/wallet_eval/config.py" %}
Note this file also specifies what DashArgos queries to run on top of.
You can set up new queries and point your code to them if you wish.

This file specifies our ``is this inflow source a problem?`` definition:
{% @github-files/github-code-block url="https://github.com/ChainArgos/api-demos/blob/main/looker/wallet_eval/is_suspicious.py" %}

Now we can look at the main function.
This grabs all the inflows, looks up the categories associated with inflow wallets,
computes what we want to compute and then (lightly) formats the output.
{% @github-files/github-code-block url="https://github.com/ChainArgos/api-demos/blob/main/looker/wallet_eval/wallet_eval.py" %}

A range of helper functions which wrap the underlying API are here:
{% @github-files/github-code-block url="https://github.com/ChainArgos/api-demos/blob/main/looker/wallet_eval/helpers.py" %}
