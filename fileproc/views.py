from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import AllowAny

import pandas as pd
from fileproc.tools import check_date_column_formatting
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
        failed_df = pd.DataFrame()
        print(df)

        # Drop the rows where the date does not match the format that we are looking for
        df["fail"] = df["Date"].apply(check_date_column_formatting)
        # temp = df[df['fail'] == True] NOTE: This is here in case of a feature for returning a CSV file with the failed rows 
        indexes_to_drop = df[df['fail'] == True].index
        df = df.drop(indexes_to_drop)
        
        # Convert the date column to a datetime format for easier processing later on
        df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d')

        print(df.dtypes)

        return Response("World")

