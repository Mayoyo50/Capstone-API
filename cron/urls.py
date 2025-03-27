from django.urls import path
from .views import HealthCheckView

urlpatterns = [
    path('run-script/', HealthCheckView.as_view(), name='run_script'),
]