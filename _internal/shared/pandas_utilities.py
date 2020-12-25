"""Custom Pandas utilities."""

import pandas as pd
import pandasql as ps
import logging
from tabulate import tabulate

LOGGER = logging.getLogger(f"{__name__}")

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


def get_row_count(dataframe: object):
    """
    Function will return number of rows in a dataframe.
    :param object dataframe: Dataframe to count.
    :return integer: Number of rows in dataframe.
    """
    return len(dataframe.index)

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


def update_column_headers(filename: str):
    """
    This will update the first line of the CSV file and replace spaces in the column headers with '_'
    :param logger: Logger object
    :param filename: Name of file to read
    :return:
    """
    LOGGER.info("filename = %s", filename)
    LOGGER.info(f'Starting column header updates...')

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
    LOGGER.info(f'File: {filename} has been updated with new column headers.')


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
    try:
        dataframe = pd.DataFrame(data, columns=column_headers)
    except ValueError as e:
        print(f'Error: {e}')
        print(f'Column headers: {column_headers}')
        print(f'Data Row: {data[0]}')
        exit(1)

    return dataframe


def run_query(dataframe: object, query: str) -> object:
    """
    Function will run query passed in and return the result set as a dataframe
    :param object dataframe: Dataframe to query.
    :param str query: Query to run.
    :return object dataframe: Result set as a dataframe
    """
    LOGGER.info("query = %s", query)

    results_df = ps.sqldf(query)

    return results_df

def category_sum_by_date(dataframe: object, start_date: str, end_date: str) -> object:
    """
    This will return the sum of amount between a range of dates.

    :param dataframe: Dataframe object
    :param start_date: Start date for query
    :param end_date: End data for query
    :return dataframe: Dataframe object with query results
    """
    LOGGER.info("start_date = %s", start_date)
    LOGGER.info("end_date = %s", end_date)


    category_group_by_sum_sql = f'''
    SELECT 
    CATEGORY,
    SUM(CASE When TRANSACTION_TYPE = 'debit' Then AMOUNT*-1 Else AMOUNT End ) AS SUM_AMOUNT
    FROM dataframe
    WHERE DATE >= '{start_date}' and DATE <= '{end_date}' 
    GROUP BY CATEGORY
    ORDER BY CATEGORY
    '''

    LOGGER.info(f'Query running: {category_group_by_sum_sql}')
    category_sum_df = ps.sqldf(category_group_by_sum_sql)

    return category_sum_df