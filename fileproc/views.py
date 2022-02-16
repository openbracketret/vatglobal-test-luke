
from django.shortcuts import render
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import AllowAny

from sqlalchemy import create_engine
import datetime

import pandas as pd
from fileproc.tools import (
    check_date_column_formatting,
    fix_purchase_sale_col,
    country_id_column_selector,
    currency_id_column_selector
)
from fileproc.models import Country, Records, ExchangeRateHolder
# Create your views here.

class ProccessView(APIView):
    """
    The view class for processing files, we will only be using the "POST" method here.
    POST
    -----
    Upload a file to be processed and added into the system
    """

    def post(self, request, format=None):
        """
        Params
        ------
        request.file (file): The file to be processed

        Returns
        ---------
        response (rest_framework.Response): A response object indiciting success of failuer in processing of the file
        """

        df = pd.read_csv(request.FILES['file'])

        # Drop the rows where the date does not match the format that we are looking for
        df["fail"] = df["Date"].apply(check_date_column_formatting)
        # temp = df[df['fail'] == True] NOTE: This is here in case of a feature for returning a CSV file with the failed rows 
        indexes_to_drop = df[df['fail'] == True].index
        df = df.drop(indexes_to_drop)
        
        # Convert the date column to a datetime format for easier processing later on
        df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d')


        # This will fix the purchase/sale column to match what we want to save
        df['Purchase/Sale'] = df['Purchase/Sale'].apply(fix_purchase_sale_col)
        df = df.drop(columns=['fail'])
        # NOTE: These lines have many DB transactions
        # Possibly optimize by making a single query to the database that retrieves all and then
        # subsequently do the matching
        df['Country'] = df['Country'].apply(country_id_column_selector)
        df['Currency'] = df['Currency'].apply(currency_id_column_selector)

        # Filter the DF down to only the 2020 objects
        start_date = datetime.datetime(year=2020, day=1, month=1)
        end_date = datetime.datetime(year=2021, day=1, month=1)
        mask = (df["Date"] >= start_date) & (df["Date"] < end_date)

        df = df.loc[mask]

        df = df.rename(columns={
            "Date": "date",
            "Purchase/Sale": "type",
            "Country": "country_id",
            "Currency": "currency_id",
            "Net": "net",
            "VAT": "vat"
        })

        # NOTE: This seems to be the fastest way to mass create entries inside of the database table

        database_info = settings.DATABASES['default']

        user = database_info['USER']
        password = database_info['PASSWORD']
        database_name = database_info['NAME']

        database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format(
            user=user,
            password=password,
            database_name=database_name,
        )

        engine = create_engine(database_url, echo=False)
        df.to_sql(Records._meta.db_table, con=engine, if_exists='append', index=False)

        # NOTE: A really gross and inefficient way to do this
        # for index, row in df.iterrows():

        #     if row["Date"].year != 2020:
        #         continue

        #     date = row["Date"]
        #     type = row["Purchase/Sale"]
        #     net = row["Net"]
        #     vat = row["VAT"]

        #     # NOTE: For both country and currency here if there is more than one result
        #     # I am just going to select the first one in the list for time saving
        #     # In the case I do not have the country saved it will simply be blank
        #     try:
        #         country = Country.objects.filter(
        #             Q(name__icontains=row["Country"]) |
        #             Q(alpha_code__iexact=row["Country"])
        #         )[0]
        #     except Exception as e:
        #         country = None
            
        #     try:
        #         currency = Country.objects.filter(
        #             currency_code__iexact=row["Currency"]
        #         )[0]
        #     except Exception as e:
        #         currency = None

        #     Records.objects.create(
        #         date=date,
        #         type=type,
        #         country=country,
        #         currency=currency,
        #         net=net,
        #         vat=vat
        #     )
            


        return Response({"success": True})

class RetrieveView(APIView):
    """
    APIView class used to retrieve records from the database.

    GET
    ---------
    Retrieve records based on passed in parameters
    params: country, date, currency
    """

    def get(self, request, format=None):
        """
        Params
        -------
        country (string): The country to be retrieved from in ISO 3166 format
        date (string): The date of the record to be retrieved in YYYY/MM/DD format
        *currency (string): A currency code to convert the values to in ISO 4217 format
        """
        
        return Response("hedge")