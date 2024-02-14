from io import StringIO

import looker_sdk
import pandas as pd


def create_query(looker, base_query, query_filter):
    new_query = looker.create_query(body=looker_sdk.models40.WriteQuery(model=base_query.model, view=base_query.view,
                                                                        fields=base_query.fields, filters=query_filter,
                                                                        pivots=base_query.pivots,
                                                                        total=base_query.total,
                                                                        row_total=base_query.row_total))
    return new_query


def run_query(sdk, query):
    return pd.read_csv(StringIO(sdk.run_query(query_id=query.id, result_format='csv')))
