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


def update_column_names(filename: str):
    """
    This will update the first line of the CSV file and replace spaces in the column headers with '_'
    :param filename:
    """
    f = open(filename, 'r')
    line = f.readline().strip()
    f.close()
    column_headers = line.split(',')
    updated_column_headers = []
    for header in column_headers:
        updated_column_headers.append(header.replace(' ', '_').upper())


def category_sum_by_date(dataframe: object, start_date: str, end_date: str):
    """This will return the sum of amount between a range of dates"""


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
    df = pd.read_csv(filename)

    #print(df)

    update_column_names(filename)


    exit(0)


if __name__ == '__main__':
    main()