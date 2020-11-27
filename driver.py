"""This will label transaction types based on vendor."""

from api.google.google_api import googleApiHelper
import _internal.shared.pandas_utilities as pd_utils

def main():
    # create google API services
    drive_service = googleApiHelper('drive', 'v3')
    sheets_service = googleApiHelper('sheets', 'v4')

    # get file ID for spreadsheet
    file_id = drive_service.get_file_id('All time transactions from Mint')

    # get spreadsheet data
    sheet_data = sheets_service.get_sheets_data(file_id)

    #retrieve column headers
    column_headers = sheet_data.pop(0)

    # create dataframe object from spreadsheet data
    df = pd_utils.create_df_from_list_of_lists(column_headers, sheet_data)

    # query dataframe with date range
    category_sum_df = pd_utils.category_sum_by_date(df, '11/01/2020', '11/30/2020')

    print(pd_utils.get_tabulate_str_from_df(category_sum_df))

    exit(0)


if __name__ == '__main__':
    main()