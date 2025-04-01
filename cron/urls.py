from django.urls import path
from .views import healthCheck

urlpatterns = [
    path('run-script/', healthCheck  , name='Check live'),
]