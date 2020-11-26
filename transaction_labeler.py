"""This will label transaction types based on vendor."""

import pandas as pd
import pandasql as ps
import logging

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


def update_column_headers(logger: object, filename: str):
    """
    This will update the first line of the CSV file and replace spaces in the column headers with '_'
    :param filename:
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


def category_sum_by_date(logger: object, dataframe: object, start_date: str, end_date: str):
    """This will return the sum of amount between a range of dates"""
    logger.info(f'start_date: {start_date}\n'
          f'end_date: {end_date}')


    category_group_by_sum_sql = '''
    select 
    category,
    sum(amount) as Amount
    from df
    group by category 
    order by sum(amount) desc
    '''

    print(ps.sqldf(category_group_by_sum_sql))

    #print( df.groupby(['Category']).sum('Amount') )


def main():
    my_logger = create_logger()
    filename = 'transactions.csv'
    # read by default 1st sheet of an excel file
    #df = pd.read_csv(filename)

    #print(df)

    update_column_headers(my_logger, filename)


    exit(0)


if __name__ == '__main__':
    main()