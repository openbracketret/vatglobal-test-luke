from datetime import datetime


def check_date_column_formatting(row):
    """
    Function that will check a value and return whether of not the format of the string is
    what we are expecting

    Params
    --------
    row (String): The string to be checked.
    """

    form = "%Y/%m/%d"

    try:
        datetime.strptime(row, form)
        return False
    except ValueError:
        return True
