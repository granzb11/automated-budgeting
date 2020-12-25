"""This will label transaction types based on vendor."""

from api.google.google_api import googleApiHelper
import _internal.shared.pandas_utilities as pd_utils



def data_cleanup(dataframe: object):
    """
    Function will perform customized data clean up.
    We will be updating the following:
        * transactions that have 'pending' in the description will be removed
        * transactions that have 'USAA FUNDS TRANSFER' in the description will be removed (These are internal account transfers)
        * transaction that have 'venmo' in account name will have category updated to 'VENMO'
        * category renamed to 'original_category'
        * new column creation of 'category' which will be a consolidation of original_category into a smaller set
            - i.e. original categories: 'Amusement', 'Movies & DVDs', 'Music' will be consolidated to 'Entertainment' category

    :param object dataframe: Dataframe to clean up.
    :return object cleaned_df: Cleaned up dataframe.
    """
    # remove all transfer transactions
    print('Data cleanup starting...')

    # Remove all transfer and funds transfer transactions
    cleaned_df = dataframe[~dataframe['DESCRIPTION'].str.contains("PENDING|USAA FUNDS TRANSFER")].reset_index(drop=True)
    cleaned_df = cleaned_df[~cleaned_df['CATEGORY'].str.contains("Transfer|Paycheck|Credit Card Payment")].reset_index(drop=True)
    cleaned_df = cleaned_df[~cleaned_df['TRANSACTION_TYPE'].str.contains("credit")].reset_index(drop=True)

    # update rent payments
    cleaned_df.loc[(cleaned_df['DESCRIPTION'].str.contains("Zelle: Norma Velazquez")), 'DESCRIPTION'] = 'Zelle: Norma Velazquez'

    # remove all income category transactions
    cleaned_df = cleaned_df[~cleaned_df['CATEGORY'].str.contains("Income")].reset_index(drop=True)

    # rename category column to original_category
    cleaned_df.rename(columns={'CATEGORY': 'ORIGINAL_CATEGORY'}, inplace=True)

    # Update all Venmo transactions to its own category
    cleaned_df.loc[(cleaned_df['ACCOUNT_NAME'].isin(['Venmo'])), 'ORIGINAL_CATEGORY'] = 'Venmo'

    # create new category column
    auto_list = ['Auto Payment', 'Gas & Fuel', 'Auto Insurance']
    entertainment_list = ['Amusement', 'Movies & DVDs', 'Music', 'Entertainment']
    other_list = ["Business Services", "Electronics & Software", "Financial", "Home Services", "Kids Activities",
                  "Office Supplies", "Parking", "Public Transportation", "Rental Car & Taxi", "Service & Parts",
                  "Shipping", "Shopping", "Sporting Goods", "Sports", "Television", "Pet Food & Supplies"]
    personal_care_list = ['Hair', 'Health & Fitness']
    personal_items_list = ['Clothing', 'Mobile Phone']
    restaurants_list = ['Coffee Shops','Fast Food', 'Restaurants', 'Food & Dining', 'Alcohol & Bars', 'ATM Fee']
    travel_list = ['Air Travel', 'Hotel']
    utilities_list = ['Bills & Utilities' ,'Utilities']
    mortgage_rent_list = ['Zelle: Norma Velazquez']
    investments_list = ['Investments']

    cleaned_df.loc[(cleaned_df['ORIGINAL_CATEGORY'].isin(auto_list)), 'CATEGORY'] = 'Auto'
    cleaned_df.loc[(cleaned_df['ORIGINAL_CATEGORY'].isin(entertainment_list)), 'CATEGORY'] = 'Entertainment'
    cleaned_df.loc[(cleaned_df['ORIGINAL_CATEGORY'].isin(other_list)), 'CATEGORY'] = 'Other'
    cleaned_df.loc[(cleaned_df['ORIGINAL_CATEGORY'].isin(personal_care_list)), 'CATEGORY'] = 'Personal Care'
    cleaned_df.loc[(cleaned_df['ORIGINAL_CATEGORY'].isin(personal_items_list)), 'CATEGORY'] = 'Personal Items'
    cleaned_df.loc[(cleaned_df['ORIGINAL_CATEGORY'].isin(restaurants_list)), 'CATEGORY'] = 'Restaurants'
    cleaned_df.loc[(cleaned_df['ORIGINAL_CATEGORY'].isin(travel_list)), 'CATEGORY'] = 'Travel'
    cleaned_df.loc[(cleaned_df['ORIGINAL_CATEGORY'].isin(utilities_list)), 'CATEGORY'] = 'Utilities'
    cleaned_df.loc[(cleaned_df['ORIGINAL_CATEGORY'].isin(investments_list)), 'CATEGORY'] = 'Investments'
    cleaned_df.loc[(cleaned_df['ORIGINAL_CATEGORY'].isin(['Venmo'])), 'CATEGORY'] = 'Venmo'
    cleaned_df.loc[(cleaned_df['ORIGINAL_CATEGORY'].isin(['Groceries'])), 'CATEGORY'] = 'Groceries'
    cleaned_df.loc[(cleaned_df['DESCRIPTION'].isin(mortgage_rent_list)), 'CATEGORY'] = 'Mortgage & Rent'

    return cleaned_df

    #print(pd_utils.get_markdown_str_from_df(cleaned_df))

    import plotly.express as px
    fig = px.pie(cleaned_df,
                 values='AMOUNT',
                 names='CATEGORY',
                 title='Amount Spent By Category',
                 color_discrete_sequence=px.colors.sequential.RdBu,
                 labels={'CATEGORY':'Category', 'AMOUNT': 'Amount'})

    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.show()


def main():
    # variables
    spreadsheet_name = 'all-time-transactions'
    sheet_id = '2140363939'

    # create google API services
    drive_service = googleApiHelper('drive', 'v3')
    sheets_service = googleApiHelper('sheets', 'v4')

    # get file ID for spreadsheet
    print(f'\nGetting sheet ID for: {spreadsheet_name}...')
    spreadsheet_id = drive_service.get_file_id(spreadsheet_name)
    print(f'Sheet ID retrieved: {spreadsheet_id}')

    # get spreadsheet data
    print(f'\nGetting sheet data for: {spreadsheet_name}...')
    sheet_data = sheets_service.get_sheets_data(spreadsheet_id)
    exit(1)
    print(f'Sheet Data retrieved.')

    #retrieve column headers
    print(f'\nGetting column_headers...')
    column_headers = sheet_data.pop(0)
    print(f'Column headers retrieved.')

    # create dataframe object from spreadsheet data
    print('\nCreating dataframe from sheet data...')
    df = pd_utils.create_df_from_list_of_lists(column_headers, sheet_data)
    print('Dataframe created.')

    df = data_cleanup(df)

    """
    Example 1.b Single Bar Chart (Existing Worksheet)
    """
    request_body = {
        'requests': [
            {
                'addChart': {
                    'chart': {
                        'spec': {
                            'title': 'Amount Spent By Category',
                            'basicChart': {
                                'chartType': 'COLUMN',
                                'legendPosition': 'BOTTOM_LEGEND',
                                'axis': [
                                    # X-AXIS
                                    {
                                        'position': 'BOTTOM_AXIS',
                                        'title': 'Category'
                                    },
                                    # Y-AXIS
                                    {
                                        'position': 'LEFT_AXIS',
                                        'title': 'Amount'
                                    }
                                ],
                                # chart labels
                                'domains': [
                                    {
                                        'domain': {
                                            'sourceRange': {
                                                'sources': [
                                                    {
                                                        'sheetId': sheet_id,
                                                        'startRowIndex': 0,
                                                        'endRowIndex': 11,
                                                        'startColumnIndex': 6,
                                                        'endColumnIndex': 7
                                                    }
                                                ]
                                            }
                                        }
                                    }
                                ],
                                # chart data
                                'series': [
                                    {
                                        'series': {
                                            'sourceRange': {
                                                'sources': [
                                                    {
                                                        'sheetId': sheet_id,
                                                        'startRowIndex': 1, # Row # 1
                                                        'endRowIndex': 11, # Row # 11
                                                        'startColumnIndex': 3, # Column D
                                                        'endColumnIndex': 4 # Column E
                                                    }
                                                ]
                                            }
                                        },
                                        'targetAxis': 'LEFT_AXIS'
                                    }
                                ]
                            }
                        },
                        'position': {
                            'overlayPosition': {
                                'anchorCell': {
                                    'sheetId': '381628921',
                                    'rowIndex': 1,
                                    'columnIndex': 2
                                },
                                'offsetXPixels': 0,
                                'offsetYPixels': 0,
                                'widthPixels': 800,
                                'heightPixels': 600
                            }
                        }
                    }
                }
            }
        ]
    }

    response = sheets_service.service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=request_body
    ).execute()

    #print(pd_utils.run_query(df, sql))
    # query dataframe with date range
    #category_sum_df = pd_utils.category_sum_by_date(df, '11/01/2020', '11/30/2020')

    #print(pd_utils.get_tabulate_str_from_df(category_sum_df))

    exit(0)


if __name__ == '__main__':
    main()