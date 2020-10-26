# Django Rest Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render

# Create your views here.
from .main import doc_predict
from .main import doc_train

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
def predict(request):
    try:
    	logger.info('Request received in predict service')
    	predictions = doc_predict(request.data)
    	content = {'categories':predictions}
    	return Response(content, status=status.HTTP_200_OK)
    except Exception as e:
        print ('Predict Service Error >> ',e)
        logger.error('Error occured in predict service')
        content = {'msg':
                'Something went wrong. Contact UrbanWood UMN admin team.'}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def train(request):
    try:
        logger.info('Request received in train service')
        msg = doc_train(request.data)
        return Response({'msg': msg}, status=status.HTTP_200_OK)
    except Exception as e:
        print ('Train Service Error >> ',e)
        logger.error('Error occured in train service')
        content = {'msg':
                'Something went wrong. Contact UrbanWood UMN admin team.'}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
