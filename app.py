# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import dash_auth
import plotly.graph_objs as go
from plotly.subplots import make_subplots

import pandas as pd
import numpy as np

from pages import overview, commentsConclusions, predictionModel
from utils.utils_layout import Header
from utils.utils_data import data_preparation, cohort_3way
from utils.utils_figures import produce_heatmap,produce_single_heatmap



# ===== INITIALIZE =========
# ==========================

# Load data once
communities, community_payouts, customers, customer_policies, policy_transactions, df_all = data_preparation()

## DEFINE ALLOWED FILTERS HERE
# Load groupping options. Dropdown filter is updated accordingly.
allowed_groups = ['gender', 'region','crop','literacy','has_phone','community_received_premium']

# Calculate categories of each allowed group. This is used to display filters later on
possible_filters = {}
for g in allowed_groups:
    possible_filters[g] = df_all[g].unique()

# Always display a no group option
allowed_groups.append('no groupping')
possible_filters['no groupping'] = ['no groupping']



# ===== CREATE APP =========
# ==========================


# Create server instance
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server
app.config.suppress_callback_exceptions = True  # Not all ids are rendered at start
app.title = 'Worldcover customer analysis'
# Describe the layout/ UI of the app
app.layout = html.Div(
    # Here goes the layout from all pages.
    [dcc.Location(id="url", refresh=False),
     html.Div(id="page-content"),
     # Hidden div inside the app that stores the intermediate value
     html.Div(id='intermediate-value', style={'display': 'none'})
     ]

)

#auth = dash_auth.BasicAuth(app,{'admin': '1234'}) # The password should not be here but OK for now.

# Define fav icon
@server.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(server.root_path, 'static'), 'assets/favicon.ico')



# ===== MAIN LAYOUT ===========
# =============================

# Update page
@app.callback(Output("page-content", "children"),
              [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/comments-conclusions":
        return commentsConclusions.create_layout(app)
    elif pathname == "/prediction-model":
        return predictionModel.create_layout(app)
    elif pathname == "/full-view":
        return (
            overview.create_layout(app,allowed_groups),
            commentsConclusions.create_layout(app),
            predictionModel.create_layout(app)
        )
    else:
        return overview.create_layout(app, allowed_groups)


# ===== CALLBACKS =========
# ========================


# Update the choices (labels) of the filter dropdown. Happens once.
@app.callback(
    Output('overview-dropdown-filter', 'options'),
    [Input('overview-dropdown-group', 'value')])
def update_filter_options(filter_options):

    if filter_options == "no groupping":
        #print('Simple table. No filters to show.')
        return [dict(label='', value='')]

    else:
        groups_dict = [{'label': k, 'value': k} for k in possible_filters[filter_options]]
        #print('groups_dict {}'.format(groups_dict))

        return groups_dict


# Update the values of the filter dropdown accordingly.
@app.callback(
    Output('overview-dropdown-filter', 'value'),
    [Input('overview-dropdown-group', 'value')])
def update_filter_options(filter_options):

    if filter_options == "no groupping":
        return None
    else:
        subgroups_list = [k for k in possible_filters[filter_options]]
        return subgroups_list




# Calculate retention rate. Save it into hidden div.
@app.callback(
    Output('intermediate-value', 'children'),
    [Input('overview-dropdown-group', 'value'),  # Shall we skip this interaction?
     Input('overview-dropdown-filter', 'value'),
     Input('overview-radio-total', 'value'),
     Input('overview-radio-pivot', 'value')])
def update_retention_table(group_value, filter_value, total_value, pivot_value):

    if group_value ==  "no groupping" or len(filter_value) == 0:
        group_value = "no groupping"

    # Create cohort table
    df = cohort_3way(df_all, mode=total_value,  index3=group_value, pivot_value = pivot_value, show_totals=True).fillna("")

    # Round if fraction
    if total_value == "fraction":
        df = df.round(2)  # TODO: Is this really working?

    print('Updated dataframe: ')
    print(df)

    # If its another file type: json.dumps(cleaned_df)
    return df.to_json(date_format='iso', orient='table')


# Define plot/table
@app.callback(
    Output('overview-graph-table', 'children'),
    [Input('intermediate-value', 'children'), # triggered when the cohort table changes
     Input('overview-radio-graph', 'value')],
    [State('overview-dropdown-group', 'value'), #Use these states as inputs
     State('overview-dropdown-filter', 'value'),
     State('overview-radio-total', 'value'),
     State('overview-radio-pivot', 'value')])
def update_figure(input_data, display, group_value, filter_values,total_value, pivot_value):

    # Gather table from hidden div and show
    df = pd.read_json(input_data, orient='table')
    df.reset_index(inplace=True)

    ## HEATMAP
    if display == "heatmap":

        if group_value == "no groupping" or len(filter_values) == 0:
            # Single heatmap
            fig = make_subplots(rows=1, cols=1)
            fig = produce_single_heatmap(fig, df, index3="", level=None, total_value=total_value, title_text="", row=1, col=1)
            fig.update_layout(title_text="Retention rates", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

        else:
            # Filter values in table
            m = df[group_value].isin(np.array(filter_values))
            df = df.loc[m, :].reset_index(level=0, drop=True)

            # Call heatmap multiple function
            fig = produce_heatmap(df, group_value, total_value)

        return dcc.Graph(id='overview-heatmap', figure=fig)


    ## TABLE ##
    else:
        # Modify the format to display a multiindex table

        if group_value == "no groupping" or len(filter_values) == 0:
            # Print simple table
            # Format to display. Add one row on top
            df.loc[-1] = np.array([df.columns.values[0]] + ["" for i in range(df.shape[1] - 1)])  # adding a row
            df.index = df.index + 1  # shifting index
            df = df.sort_index()  # sorting by index

            # Swap col[0] name (when printed refers to the columns)
            if df.columns.values[0] == "season":
                df.rename(columns = {"season":"season_first"},inplace=True)
            else:
                df.rename(columns = {"season_first": "season"},inplace=True)

        else:

            # Filter columns
            m = df[group_value].isin(np.array(filter_values))
            df = df.loc[m, :].reset_index(level=0, drop=True)

            # Keep only the first occurrence of index3 (multiindex)
            first = ""
            for i in range(0, df.shape[0]):
                if df[group_value][i] == first:
                    df[group_value][i] = ""
                else:
                    first = df[group_value][i]

            # Add one row
            df.loc[-1] = np.array([group_value, df.columns.values[1]] + ["" for i in range(df.shape[1] - 2)])  # adding a row
            df.index = df.index + 1  # shifting index
            df = df.sort_index()  # sorting by index

            # Finally, remove extra column names
            df = df.rename({group_value: ''}, axis=1)

            # Swap col[0] name (which when printed refers to the columns)
            if df.columns.values[1] == "season":
                df.rename(columns = {"season":"season_first"},inplace=True)
            else:
                df.rename(columns = {"season_first": "season"},inplace=True)


        return dash_table.DataTable(
            id='overview-heatmap',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            style_header={
                "backgroundColor": "#ece1ac",
                'color': 'black'
            },
            style_data_conditional=[{
                'if': {'column_id': 'season'},
                'backgroundColor': '#ece1ac',
                'color': 'black'},
                {'if': {'column_id': 'season_first'},
                 'backgroundColor': '#ece1ac',
                 'color': 'black'},
                {'if': {'column_id': ''},
                 'backgroundColor': '#ece1ac',
                'color': 'black'}
            ]
        )


# ===== END ==============
# ========================

if __name__ == "__main__":
    app.run_server(debug=True)
