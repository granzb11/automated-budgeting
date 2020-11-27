"""This will label transaction types based on vendor."""

import pandas as pd
import pandasql as ps
import logging

from pandas import DataFrame
from tabulate import tabulate
from api.google.google_api import googleApiHelper
import json

def create_logger() -> object:
    # Gets or creates a logger
    logger = logging.getLogger(__name__)

    # set log level
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()

    # define file handler and set formatter
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    handler.setFormatter(formatter)

    # add handler to logger
    logger.addHandler(handler)

    return logger


def get_df_from_csv(filename: str) -> object:
    """
    This will return a dataframe object given a csv filename.
    :param filename: Name of file to read
    :return object: Dataframe object
    """
    return pd.read_csv(filename)


def get_csv_from_df(dataframe: object):
    """
    This will return a string that represents the dataframe as a csv string.
    :param dataframe: Dataframe object
    :return str: Markdown table string
    """
    return dataframe.to_csv(index=False)


def get_markdown_str_from_df(dataframe: object) -> str:
    """
    This will return a string that represents the dataframe as a markdown table.
    :param dataframe: Dataframe object
    :return str: Markdown table string
    """
    return dataframe.to_markdown()


def get_tabulate_str_from_df(dataframe: object) -> str:
    """
    This will return a string that represents the dataframe as a table structure using tabulate.
    :param dataframe: Dataframe object
    :return str: Table string
    """
    return tabulate(dataframe, headers='keys', tablefmt='psql')


def update_column_headers(logger: object, filename: str):
    """
    This will update the first line of the CSV file and replace spaces in the column headers with '_'
    :param logger: Logger object
    :param filename: Name of file to read
    :return:
    """
    logger.info(f'Arguments passed in:\n'
                f'filename: {filename}')

    logger.info(f'Starting column header updates...')

    # open file for reading and writing
    f = open(filename, 'r+')
    # gather full file text and first line
    full_file_text = f.read()
    # resetting file pointer
    f.seek(0)
    column_header = f.readline().strip()

    # creating new column headers in caps and replacing spaces with underscores
    column_headers = column_header.split(',')
    updated_column_headers: list = []
    for header in column_headers:
        updated_column_headers.append(header.replace(' ', '_').upper())

    # joining new headers back together and updating full file text with new headers
    new_column_headers = ','.join(updated_column_headers)
    full_file_text = full_file_text.replace(column_header, new_column_headers)

    # updating file with new file headers
    f.seek(0)
    f.write(full_file_text)
    logger.info(f'File: {filename} has been updated with new column headers.')


def column_header_formatter(header: str) -> str:
    """
    Function will format column header.
    :param str header: Header for format.
    :return str header: Formatted header.
    """
    return header.replace(' ', '_').upper()


def create_df_from_list_of_lists(column_headers: list, data: list):
    """
    Function will convert a list of lists to a dataframe with formatted column headers.
    :param list column_headers: List of column headers.
    :param list data: List of lists with a record being represented by a list.
        Example:
        [
             ['11/25/20', 'USAA CREDIT CARD PAYMENT', 'USAA CREDIT CARD PAYMENT'],
             ['11/25/20', 'USAA PAYROLL DIRECT DEPOSIT', 'USAA PAYROLL INT PENDING DIRECT DEPOSIT']
        ]
    :return object dataframe: Dataframe object
    """
    dataframe: object = None

    # Format column headers
    for i in range(len(column_headers)):
        column_headers[i] = column_header_formatter(column_headers[i])

    # Create dataframe
    dataframe = pd.DataFrame(data, columns=column_headers)

    return dataframe


def category_sum_by_date(logger: object, dataframe: object, start_date: str, end_date: str) -> object:
    """
    This will return the sum of amount between a range of dates
    :param logger: Logger object
    :param dataframe: Dataframe object
    :param start_date: Start date for query
    :param end_date: End data for query
    :return dataframe: Dataframe object with query results
    """
    logger.info(f'Arguments passed in:\n'
                f'start_date: {start_date}\n'
                f'end_date: {end_date}')


    category_group_by_sum_sql = f'''
    SELECT 
    CATEGORY,
    SUM(CASE When TRANSACTION_TYPE = 'debit' Then AMOUNT*-1 Else AMOUNT End ) AS SUM_AMOUNT
    FROM dataframe
    WHERE DATE >= '{start_date}' and DATE <= '{end_date}' 
    GROUP BY CATEGORY
    ORDER BY CATEGORY
    '''

    logger.info(f'Query running: {category_group_by_sum_sql}')
    category_sum_df = ps.sqldf(category_group_by_sum_sql)

    return category_sum_df

def main():
    my_logger = create_logger()
    drive_service = googleApiHelper('drive', 'v3')
    sheets_service = googleApiHelper('sheets', 'v4')
    file_id = drive_service.get_file_id('All time transactions from Mint')
    #print(file_id)
    sheet_data = sheets_service.get_sheets_data(file_id)
    column_headers = sheet_data.pop(0)
    print(column_headers)
    #print(sheet_data)

    df = create_df_from_list_of_lists(column_headers, sheet_data)

    category_sum_df = category_sum_by_date(my_logger, df, '11/01/2020', '11/30/2020')

    print(get_tabulate_str_from_df(category_sum_df))

    exit(0)
    # create logger

    filename = 'transactions.csv'

    # update column headers
    update_column_headers(my_logger, filename)

    # read csv content into dataframe
    df = get_df_from_csv(filename)

    # get amount sum by category


    print(get_csv_from_df(category_sum_df))




    exit(0)


if __name__ == '__main__':
    main()