from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import AllowAny

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

        # NOTE: For the sake of time saving I am going to assume the file sctructures of all of the csvs will always be the same


        return Response("World")

