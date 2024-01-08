This brief example will demonstrate how easy it is to extract ChainArgos data out of DashArgos queries into a pandas DataFrame for analysis.

## Start with your DashArgos Query
First, set up your DashArgos query. DashArgos automatically displays 500 rows of data, up to a maximum of 5,000 rows and if your data exceeds 5,000 rows, it will be truncated in the DashArgos user interface because of browser limitations. 

However, users with API access can extract all the data relevant to their queries, and user interface limitations are not as relevant.

## Google Sheets
Having set up your DashArgos query, now we are going to pull those query results into Google Sheets.

Google gives simple instructions [here](https://cloud.google.com/looker/docs/connected-sheets).

Set up whatever pivot tables you want from your looker queries.[Here](https://docs.google.com/spreadsheets/d/10_Urfe_U-LuvydpxWozPtkEdh7tUNFFtMlmYitNapV0/) is an example sheet.

Note the Google Sheets document ID -- the long random-looking string of characters near the end of the URL -- and the names of the sheets you want to extract.

## Pandas

Here is a single-sheet example:
```python
import pandas as pd

# the document ID
DOC_ID = '10_Urfe_U-LuvydpxWozPtkEdh7tUNFFtMlmYitNapV0'
# turn this in to a URL that dumps a csv file
SHEET_URI = 'https://docs.google.com/spreadsheets/d/' + DOC_ID + '/gviz/tq?tqx=out:csv&sheet=some_sheet'

# thats it. pandas does the rest.
from_df = pd.read_csv(SHEET_URI)

```

If you want to work with data from several sheets that is not much more work:
```python
import pandas as pd

# the document ID
DOC_ID = '10_Urfe_U-LuvydpxWozPtkEdh7tUNFFtMlmYitNapV0'
# turn this in to a URL that dumps a csv file
SHEET_URI = 'https://docs.google.com/spreadsheets/d/' + DOC_ID + '/gviz/tq?tqx=out:csv&sheet='

# one uri per sheet
FROM_URI = SHEET_URI + 'from_table'
TO_URI = SHEET_URI + 'to_table'

# grab both results
from_df = pd.read_csv(FROM_URI)
to_df = pd.read_csv(TO_URI)

# merge the two separate pivot tables
merged_df = pd.merge(from_df, to_df, left_on='From Address', right_on='To Address')
```

## Periodic Updates

You can configure the Google doc to automatically update the query results by following Google's simple instructions [here](https://cloud.google.com/looker/docs/connected-sheets#scheduling_regular_refresh_times).

That's it. 

It'd be no-code except you *wanted* to use pandas.
