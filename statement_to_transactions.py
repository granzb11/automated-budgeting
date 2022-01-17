"""Parses through American Express Statements, standardizes the data and writes it out to all-time-transactions-<year> excel."""
# native
import sys
import warnings

# third party
import pandas as pd

transactions_workbook = "transactions-2021.xlsx"


def read_excel(file_path: str, sheet_name: str = None, header: int = 0) -> pd.DataFrame:
    """Read excel sheet and return contents in a dataframe.

    Args:
        file_path (str): Path to file.
        sheet_name (str, optional): Sheet to read in from workbook. Defaults to None.
        header (int, optional): Where to start reading from in the workbook sheet. Defaults to 0.

    Returns:
        pd.DataFrame: Dataframe with file contents.
    """
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")

        # header is set to 6 since this is the row in the spreadhseet that should act as the columns
        transaction_df = pd.read_excel(
            file_path, sheet_name=sheet_name, engine="openpyxl", header=header
        )

    return transaction_df


def write_to_excel(
    dataframe: pd.DataFrame, file_path: str, sheet_name: str = None
) -> None:
    """Write dataframe to excel.

    Args:
        dataframe (pd.DataFrame): Dataframe with contents to write to excel.
        file_path (str): Path to file.
        sheet_name (str): Sheet in workbook to write contents to.
    """
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(file_path, engine="xlsxwriter")
    # Convert the dataframe to an XlsxWriter Excel object.
    dataframe.to_excel(writer, sheet_name=sheet_name, index=False)

    # Get the xlsxwriter workbook and worksheet objects.
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    # Add some cell formats.
    digits_format = workbook.add_format({"num_format": "#,##0.00"})

    for col in range(len(dataframe.columns)):
        worksheet.set_column(col, col, 20, digits_format)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()


def update_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Drop unnecessary columns from dataframe and adds required columns.

    Args:
        dataframe (pd.DataFrame): Dataframe containing spreadsheet data.

    Returns:
        pd.DataFrame: Dataframe after removal of columns.
    """
    columns_to_drop = [
        "Extended Details",
        "Appears On Your Statement As",
        "Address",
        "City/State",
        "Zip Code",
        "Country",
        "Reference",
    ]
    columns_to_add = ["Sub-category", "Transaction Type"]
    dataframe = dataframe.drop(columns=columns_to_drop)
    # adding new columns with default values
    for column in columns_to_add:
        dataframe[column] = "NaN"

    # copying values from 'Category' to 'Sub-category'
    dataframe["Sub-category"] = dataframe["Category"]

    return dataframe


def update_categories(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Update category names and values to standard names used later for analytics.

    Currently this updates the columns:
      * Category           - Splits values from column 'Category' to pull category
      * Sub-category       - Splits values from column 'Category' to create sub-category
      * Transaction Type   - If 'Amount' is negative, value set to credit, otherwise debit.

    Args:
        dataframe (pd.DataFrame): Dataframe containing spreadsheet data.

    Returns:
        pd.DataFrame: Dataframe after column updates.
    """
    dataframe["Category"] = dataframe["Category"].map(update_category)
    dataframe["Sub-category"] = dataframe["Sub-category"].map(create_sub_category)
    dataframe["Transaction Type"] = dataframe["Amount"].map(update_transaction_type)

    return dataframe


def create_sub_category(category: str) -> str:
    """Determine sub-category values.

    At this point, we've copied over the values from "Category" to "Sub-category" columns.
    These values look like the following: Entertainment-General Attractions, "Transportation-Fuel"
    The second part of this string is the "Sub-category".
    This function will split the string and return the second part if it exists in the string.
    Otherwise, it will return the initial string.

    Args:
        category (str): Category string that will be parsed for "Sub-category"

    Returns:
        [str]: Sub-category
    """
    sub_category = category
    if isinstance(
        category, str
    ):  # check if category is a string (hit failures with nan)
        split_list = category.split("-")
        sub_category = split_list[1]
    else:
        sub_category = "Payment"

    return sub_category


def update_category(category: str) -> str:
    """Determine category value.

    The values in this column look like the following:
    "Entertainment-General Attractions", "Transportation-Fuel"
    The first part of this string is the "Category".
    This function will split the string and return the first part if it exists in the string.
    Otherwise, it will return the initial string.

    Args:
        category (str): Category string that will be parsed for "Category"

    Returns:
        [str]: Category
    """
    if isinstance(
        category, str
    ):  # check if category is a string (hit failures with nan)
        split_list = category.split("-")
        category = split_list[0]
    else:
        category = "Payment"

    return category


def update_transaction_type(amount: str) -> str:
    """Determine transaction type based on amount.

    If the amount is negative, the trans type is credit, otherwise it's debit.

    Args:
        amount (str): Amount for transaction

    Returns:
        str: Transaction type
    """
    trans_type = "Debit"
    amount = int(amount)
    if amount < 0:
        trans_type = "Credit"

    return trans_type


def merge_dataframes(
    dataframe1: pd.DataFrame, dataframe2: pd.pd.DataFrame
) -> pd.DataFrame:
    """Combine 2 dataframes into 1.

    Args:
        dataframe1 (pd.DataFrame): Dataframe with data.
        dataframe2 (pd.pd.DataFrame): Dataframe with data.

    Returns:
        pd.DataFrame: Combined dataframe.
    """
    return pd.concat([dataframe1, dataframe2]).sort_values("Date")


def main():
    """Driver function."""
    try:
        all_time_path = sys.argv[1]
        statement_path = sys.argv[2]
    except Exception as err:
        print("This script requires 2 arguments.")
        print(
            "1. Path to 'All Time Transactions' excel. This typically resides in: /Users/gustavoranz/Documents/Budget/all-time-transactions"
        )
        print(
            "2. Path to statement excel. This typicall resides in /Users/gustavoranz/Documents/Budget/statements"
        )
        exit(1)

    # read in excels into dataframes
    all_time_df = read_excel(all_time_path, sheet_name="All Time Transactions")
    statement_df = read_excel(
        statement_path, sheet_name="Transaction Details", header=6
    )

    # perform statement updates
    statement_df = update_columns(statement_df)
    statement_df = update_categories(statement_df)

    # add new statement to all time transactions by combining dataframes
    result = merge_dataframes(all_time_df, statement_df)

    # write final result to all time transactions
    write_to_excel(file_path=all_time_path, sheet_name="All Time Transactions")


if __name__ == "__main__":
    main()
