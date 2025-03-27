from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class HealthCheckView(APIView):
    """
    Simple health check endpoint.
    """
    
    def get(self, request, *args, **kwargs):
        logger.info("Health check endpoint was hit - service is alive")
        return Response({
            "status": "success",
            "message": "Service is running",
            "service": "Capstone API", 
        })