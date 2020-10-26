# Django Rest Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render

# Create your views here.
from .main import keyword_extraction

# Logger
import logging
logger = logging.getLogger(__name__)

# Error Tracing
import traceback

# Create your views here.
@api_view(["POST"])
def index(request):
	content = "Link does not exist. Please contact UrbanWood UMN admin team."
	return Response(content, status=status.HTTP_501_NOT_IMPLEMENTED)

@api_view(["POST"])
def extract(request):
    try:
    	logger.info('Request received in extract service')
    	keywords = keyword_extraction(request.data)
    	content = {'keywords':keywords}
    	return Response(content, status=status.HTTP_200_OK)
    except Exception as e:
        print ('Extract Service Error >> ',e)
        logger.error('Error occured in extract service')
        content = {'msg':
                'Something went wrong. Contact UrbanWood UMN admin team.'}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)