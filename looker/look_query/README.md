# Running a Look/Query via API

Here we are going to run a look with modified filter values and retrieve the results.
This demo uses [this Look](https://dashargos.chainargos.com/looks/722).

The demo is a simple look which retrieves info for a single given wallet address.
This finds the look, extracts the query, updates the parameters and then runs it.
Finally results are printed out.
{% @github-files/github-code-block url="https://github.com/ChainArgos/api-demos/blob/main/looker/look_query/look_query_demo.py" %}

Note this code involves manipulating the query filters.
If you want to look at the filters on a given look via the API here is a code snippet to do that:
{% @github-files/github-code-block url="https://github.com/ChainArgos/api-demos/blob/main/looker/look_query/get_query_filters.py" %}
