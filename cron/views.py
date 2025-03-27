from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class HealthCheckView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({
            "status": "success",
            "message": "Service is running",
        })