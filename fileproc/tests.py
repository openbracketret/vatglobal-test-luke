import pytest
from django.test import TestCase

# Create your tests here.
from fileproc.tools import (
    check_date_column_formatting,
    fix_purchase_sale_col,
    country_id_column_selector,
    currency_id_column_selector
)

from fileproc.models import Records, Country

pytestmark = pytest.mark.django_db

class TestTools:
    """
    Testing class for all the functions inside of tools.py
    """

    def test_check_date_column(self):
        assert check_date_column_formatting("2020/01/03") == False
        assert check_date_column_formatting("12-12/12") == True

    def test_fix_purchase_sale_col(self):
        assert fix_purchase_sale_col("slea") == "sale"
        assert fix_purchase_sale_col("purasech") == "purchase"
        assert fix_purchase_sale_col("1234") == "sale"
        assert fix_purchase_sale_col("12345") == "purchase"

    def test_country_model_none(self):
        t = Country.objects.filter(name="NONE")
        assert t.exists()
        t = t[0]
        assert t.name == "NONE"

    def test_country_model_more_than_one(self):
        t = Country.objects.all()
        assert t.count() > 1

    def test_country_id_column_selecter(self):
        country_id = country_id_column_selector("ZA")
        assert country_id > 0
        country_id = country_id_column_selector("United Kingdom")
        assert country_id > 0
        country_id = country_id_column_selector("")
        assert Country.objects.get(id=country_id).name == "NONE"

    def test_currency_column_selecter(self):
        country_id = currency_id_column_selector("ZAR")
        assert country_id > 0
        country_id = currency_id_column_selector("afghanistan")
        assert country_id > 0
        country_id = country_id_column_selector("")
        assert Country.objects.get(id=country_id).name == "NONE"