import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px
import plotly
import json



def produce_single_heatmap(fig, df_fig, index3="", level=None, total_value = "",title_text="", row=1, col=1):
    """
    Returns a plotly figure with a heatmsap
    """
    # TODO: Make some simple asserts here

    # If index3 is provided, filter df_fig to get a single level
    if index3 != "":
        df_fig = df_fig.loc[df_fig[index3] == level, :]  # Data here
        df_fig.drop([index3], axis=1, inplace=True)

    # Get row and column names out of indexes and colnames
    if 'season' in df_fig.columns:
        idx_index = "season"
    else:
        idx_index = "season_first"

    levels = df_fig[idx_index].unique()  # unique not necessary.
    df_fig.set_index(idx_index, inplace=True) # re-index in order
    df_fig.drop([ 'TOTAL'], axis=1, inplace=True)

    ## HACK to force same number of rows and columns. Otherwise dash-js complains....
    # todo: find out why.
    # Fill up with empty cells to make it a squared df
    row_names = np.array(df_fig.index)
    for l in levels:
        if l not in row_names:
            print('-{} is missing'.format(l))
            df_fig = df_fig.append(pd.Series(name=l))
    # Keep same order as columns
    df_fig = df_fig.loc[df_fig.columns, :].fillna("")
    ## END of hack

    # Create matrices to display in plot
    Z = df_fig.values.tolist()
    X = df_fig.columns.values.tolist()
    Y = df_fig.columns.values.tolist()

    # Add trace
    fig.add_trace(
        go.Heatmap(
            z=Z, x=X,y=Y,
            type='heatmap',
            colorscale=px.colors.cmocean.algae,
            showscale=False,
            hovertemplate = 'First season purchase: %{y}<br>Current purchase season: %{x}<br>Value: %{z}<extra></extra>'
        ),
        row=row, col=col
    )
    fig.update_yaxes(title_text=title_text, row=row, col=col,tickfont=dict(size=9),autorange = "reversed")
    fig.update_xaxes( row=row, col=col, tickfont=dict(size=9))



    return fig


def produce_heatmap(df, index3,total_value):

    # Get unique levels
    levels = df[index3].unique()

    # Decide on the number of plotting rows
    N = len(levels)
    nrows = int(np.ceil(N / 2))

    # Subplot definition
    fig = make_subplots(rows=nrows, cols=2,  vertical_spacing=0.22,subplot_titles=tuple(levels))

    for i in range(1, nrows + 1):
        # Left plot
        fig = produce_single_heatmap(fig, df, index3=index3, level=levels[2 * (i - 1)], title_text="",
                                     total_value=total_value, row=i, col=1)

        # Right plot
        if i == nrows and N % 2 > 0:
            # Skip subplot if uneven and last one (bottom right)
            continue
        else:
            fig = produce_single_heatmap(fig, df, index3=index3, level=levels[2 * (i - 1) + 1], total_value=total_value,
                                         title_text="", row=i,
                                         col=2)

    fig.update_layout(height=300 * nrows,  # width=1000,
                      title_text="Retention rate over {}".format(index3),
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    return fig
