from django.urls import path
from .views import ProjectCreateView, ProjectFileAccessView

urlpatterns = [
    path('', ProjectCreateView.as_view(), name='project-create'),
    path('files/<int:pk>/', ProjectFileAccessView.as_view(), name='file-access'),
]