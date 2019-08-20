import numpy as np
import pandas as pd


def data_preparation_simulated():
    """
    Load and pre-process the simulated data.
    The data has been simulated to preserve the privacy of the users and Worldcover.
    Any simmilarity with the real data is not intended at all
    """

    df_all = pd.read_csv('data/simulated_data_input.csv')

    return df_all




def data_preparation():
    """
    Load and pre-process the data
    """

    # Load provided datasets
    communities = pd.read_csv('data/wc_communities.csv')
    community_payouts = pd.read_csv('data/wc_community_payouts.csv')
    customers = pd.read_csv('data/wc_customers.csv')
    customer_policies = pd.read_csv('data/wc_customer_policies.csv')
    policy_transactions = pd.read_csv('data/wc_policy_transactions.csv')

    ## Create Cohort groups, i.e. indicate season of first purchase
    # Create dictionary with season to index
    seasons = customer_policies.season.unique()[::-1]
    map_season = dict(zip(seasons, range(0, len(seasons))))
    map_season_inv = dict(zip(range(0, len(seasons)), seasons))

    # Assign season to index
    customer_policies['season_index'] = customer_policies['season'].map(map_season)

    # Now get the season_index where that customer purchased for the first time
    customer_policies['season_index_first'] = customer_policies.groupby('customer_id')['season_index'].transform(
        'min')  # Note that transform does not modify shape
    customer_policies['season_first'] = customer_policies['season_index_first'].map(map_season_inv)

    ## Merge datasets that will be needed later on
    custom_comm = pd.merge(communities, customers, how='inner', on='community_id')
    # print('Communities shape:{} customer shape:{} merged custom_comm shape:{}'.format(communities.shape, customers.shape, custom_comm.shape))

    merged_ccc = pd.merge(customer_policies, custom_comm, how='inner', on='customer_id')
    # print('customer_policies shape:{} custom_comm shape:{} merged_ccc dataset shape:{}'.format(customer_policies.shape, custom_comm.shape, merged_ccc.shape))

    ## Which communities have received a payment?
    community_paid = pd.merge(community_payouts, communities, how='left', on='community_id')
    # print('community_payouts shape: {} communities shape: {} community_paid merged dataset shape: {}'.format(community_payouts.shape, communities.shape,
    # community_paid.shape))
    merged_ccc['community_received_premium'] = np.where(merged_ccc['community_id'].isin(community_paid.community_id), 'premium_paid', 'not_premium_paid')

    ## has_phone is a True/False column. Convert to string
    merged_ccc.has_phone[merged_ccc.has_phone] = "yes_phone"
    merged_ccc.has_phone[merged_ccc.has_phone == False] = "no_phone"

    ## nan gender to undefined
    merged_ccc.gender = merged_ccc.gender.fillna('undefined')

    ## Lets add the transacion amount information. Start by linking policy transaction amount with policy_id
    df_revenue = pd.merge(customer_policies, policy_transactions, how="right", on='customer_policy_id')
    # print('customer_policies shape:{} policy_transactions shape:{} merged df_revenue shape:{}'.format(customer_policies.shape, policy_transactions.shape,
    # df_revenue.shape))

    # Group by customer_policy_id and avg/sum transaction_amount
    # Note that a policy can have more than 1 transaction.
    df_group = df_revenue.groupby('customer_policy_id')['transaction_amount'].agg(
        [("sum_customer_transaction", "sum"),
         ('mean_customer_transaction', 'mean'),
         ('count_customer_transaction', 'count')], axis="columns")

    # Now we are ready to merge with the full dataset
    df_trans = pd.merge(df_group, merged_ccc, how="right", on='customer_policy_id')
    # print('df_group shape:{} merged_ccc shape:{} merged df_trans shape:{}'.format(df_group.shape, merged_ccc.shape,df_trans.shape))

    #return communities, community_payouts, customers, customer_policies, policy_transactions, df_trans
    return df_trans


def set_diag2(df, axis_input=0, inplace=True):
    """
    Takes a two dimensional squared dataFrame and replaces its diagional by the sum of its rows/cols

    df: two dimensional squared pandas with common index and columns names
    value_diag: values to add to the diagonal. Must share indexes with df
    make_copy: opertions inplace (True) or on a copy (False)
    """
    # Checks. ToDo: some asserts() here.
    # print('shape df:{}  len diag set: {}'.format(df.shape,len(value_diag)))
    # print(value_diag)

    # Get the total per column(0) or row (1)
    value_diag = df.sum(axis_input)

    if inplace == True:
        df_return = df
    else:
        df_return = df.copy()

    # Do the modification.
    for l in df.index:  # must be the same as columns
        df_return.loc[l, l] = value_diag[l]

    return df_return


# Insert the total in the diagonal of each level
def set_diag3(df, axis_input=0):
    """
    dataframe, Multiindex
    axis_input 0: sum per column inside each first level, 1 per row

    TODO: find a way of doing this without iteration (use .apply?)
    """
    df_return = df.copy()

    # Iterate over each index
    for r in df.index.levels[0]:
        set_diag2(df_return.loc[r, :], axis_input, inplace=True)

    return df_return


def cohort_3way(df, mode="", index3='region', show_totals=True, pivot_value='customer_id'):
    """
    Returns a cohort table

    df: pandas dataFrame. Need to contain at least two columns named 'season_first' and 'season'.
    mode: "totals" or "fraction"
    index3: third index to include in the cohort table. Could be an empty string '' or None.
    show_totals: True then a TOTAL column is appended with the sum of rows.
    pivot_table: Variable of interest to be shown in the table cells. By default 'customer_id'. 'sum_customer_transaction' is also supported.
    """

    # The slicing changes in case no groupping is flagged. define here.
    if index3 == "no groupping" or index3 is None:
        groupby_array = ['season', 'season_first']
        index_pivot = ['season_first']
    else:
        groupby_array = ['season', 'season_first', index3]
        index_pivot = [index3, 'season_first']

    # Group by seasons. Calculate either unique number of customers or sum of transacion.
    if pivot_value == 'customer_id':
        cohort_data = df.groupby(groupby_array)[pivot_value].nunique().reset_index()

    elif pivot_value == 'sum_customer_transaction':
        cohort_data = df.groupby(groupby_array)[pivot_value].sum().reset_index()

    else:
        raise ValueError('Pivot_value not found')

    # Get the pivot table per index and season.
    cohort_count_ccc_a = cohort_data.pivot_table(index=index_pivot, columns='season', values=pivot_value)


    # Calculate totals.
    # Set the totals in the diagonal. If multiiindex, then its a 2-index matrix.
    if isinstance(cohort_count_ccc_a.index, pd.core.index.MultiIndex):  # (equivalent to if index3 == "no groupping" or index3 is None: but safer I think)
        total_customers_ccc = cohort_data.pivot_table(index=[index3, 'season'], columns='season_first', values=pivot_value).sum(axis=1)
        cohort_ret_ccc = set_diag3(cohort_count_ccc_a, axis_input=0)

    else:
        total_customers_ccc = np.sum(cohort_count_ccc_a, axis=0)
        cohort_ret_ccc = set_diag2(cohort_count_ccc_a, axis_input=0)

    # TOTALS VS FRACTION
    if mode == "totals":

        if show_totals == False:
            return cohort_ret_ccc
        else:
            aux_display = cohort_ret_ccc.copy()
            aux_display['TOTAL'] = total_customers_ccc
            return aux_display

    elif mode == "fraction":

        # Do the fraction
        cohort_ret_f_ccc = round(cohort_ret_ccc.T / total_customers_ccc, 2).T
        cohort_ret_f_ccc.fillna("")

        if show_totals == False:
            return cohort_ret_f_ccc
        else:
            # Display nicely
            aux_display = cohort_ret_f_ccc.copy()
            aux_display['TOTAL'] = total_customers_ccc

            return aux_display

    else:
        raise ValueError('Mode not found')
