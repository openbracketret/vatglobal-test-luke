import pytest
from django.test import TestCase

# Create your tests here.
from fileproc.tools import check_date_column_formatting

pytestmark = pytest.mark.django_db

class TestTools:
    """
    Testing class for all the functions inside of tools.py
    """

    def test_check_date_column(self):
        assert check_date_column_formatting("2020/01/03") == False
        assert check_date_column_formatting("12-12/12") == True