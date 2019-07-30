import dash_core_components as dcc
import dash_html_components as html
from utils.utils_layout import Header
import pathlib


def create_layout(app, allowed_groups):
    return html.Div(
        [
            html.Div([Header(app)]),
            # page 1
            html.Div(
                [
                    #####################
                    # Row 3
                    #####################
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("Customer retention", style={'text-align': 'center'}),
                                    html.Br([]),
                                    html.P(
                                        '''Customer retention rate measures the fraction of the customers that, at a given season, decide to purchase 
                                        again a policy during the upcoming seasons. Higher retention rates indicate loyalty and satisfaction. Revenue 
                                        retention measures how much revenue comes from loyal customers.'''),
                                    html.P(
                                        '''The goal of this dashboard is to allow users to explore retention rates across seasons and exogenous factors. Some 
                                        conclusions are summarized in the tab 'Comments and Conclusions'.'''),
                                    # style={"color": "#ffffff"},

                                    ],
                                # className="row"
                                className="product",
                                )
                            ],
                        className="row",
                        ),

                    #####################
                    # Row 4
                    #####################
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(["Groupping variable selection"], className="subtitle padded"),
                                    html.Label('Group by'),
                                    dcc.Dropdown(
                                        id='overview-dropdown-group',
                                        options=[{'label': g, 'value': g} for g in allowed_groups],
                                        value='no groupping',
                                        clearable=False
                                        ),
                                    html.Label('Filter'),
                                    dcc.Dropdown(id='overview-dropdown-filter', multi=True),
                                    ],
                                className="six columns",
                                ),
                            html.Div(
                                [
                                    html.H6("Analysis options", className="subtitle padded"),

                                    dcc.RadioItems(
                                        id='overview-radio-total',
                                        options=[{'label': 'Show fraction', 'value': 'fraction'},
                                                 {'label': 'Show Totals', 'value': 'totals'}],
                                        value='fraction',
                                        labelStyle={'display': 'inline-block'}
                                        ),

                                    dcc.RadioItems(
                                        id='overview-radio-pivot',
                                        options=[
                                            {'label': 'Customer count', 'value': 'customer_id'},
                                            {'label': 'Revenue sum', 'value': 'sum_customer_transaction'},
                                            ],
                                        value='customer_id',
                                        labelStyle={'display': 'inline-block'}
                                        ),

                                    # html.Abbr("\u003F........",
                                    #          title="Hello, I am hover-enabled helpful information."),
                                    html.H6('Display options', className="subtitle padded"),
                                    dcc.RadioItems(
                                        id='overview-radio-graph',
                                        options=[
                                            {'label': 'Table', 'value': 'table'},
                                            {'label': 'Heatmap', 'value': 'heatmap'},
                                            ],
                                        value='table',
                                        labelStyle={'display': 'inline-block'}
                                        ),

                                    ],
                                className="six columns",
                                ),
                            ],
                        className="row",
                        # style={"margin-bottom": "35px"},
                        ),

                    #####################
                    ##### Row 5
                    #####################
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Retention data", className="subtitle padded"),
                                    html.Div(id='overview-graph-table'),
                                    html.P(
                                        "Note: rows represent season when customer purchased a policy for the first time. Columns represent season of interest. Totals are also represented in the diagonal matrices.",
                                        style={"color": "#000000"}),
                                    ],
                                className="twelve columns",
                                ),
                            ],
                        className="row ",
                        ),
                    ],
                className="sub_page",
                ),
            ],
        className="page",
        )
