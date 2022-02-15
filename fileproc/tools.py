from itertools import count
from django.db.models import Q
from datetime import datetime
from fileproc.models import Country

def check_date_column_formatting(row):
    """
    Function that will check a value and return whether of not the format of the string is
    what we are expecting

    Params
    --------
    row (String): The string to be checked.

    Returns
    --------
    bool: Whether the string matches the format required or not
    """

    form = "%Y/%m/%d"

    try:
        datetime.strptime(row, form)
        return False
    except ValueError:
        return True


def fix_purchase_sale_col(row):
    """
    Function that takes a string and determines if the value inside is supposed to say sale or purchase

    Params
    --------
    row (string): The string to be checked

    Returns
    --------
    string: The correctly formatted string
    """

    if sorted(row) == sorted("sale"):
        return "sale"
    elif sorted(row) == sorted("purchase"):
        return "purchase"
    elif len(row) > 4:
        return "purchase"
    else:
        return "sale"

def country_id_column_selector(row):
    """
    Function that takes a string and determines the country id based on the passed in value

    Params
    ------
    row (string): The string to be checked

    Returns
    -------
    country_id (int): The country id
    """

    try:
        country = Country.objects.filter(
            Q(name__icontains=row) |
            Q(alpha_code__iexact=row)
        )[0].id
    except Exception as e:
        country = Country.objects.get(name="NONE").id

    return country

def currency_id_column_selector(row):
    """
    Function that takes a string and determines the currency id based on the passed in value

    Params
    ------
    row (string): The string to be checked

    Returns
    ------
    country_id (int): The id of the country with the related currency
    """

    try:
        country = Country.objects.filter(
            currency_code__iexact=row
        )[0].id
    except Exception as e:
        country = Country.objects.get(name="NONE").id

    return country

