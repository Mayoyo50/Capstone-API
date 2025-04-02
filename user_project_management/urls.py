from django.urls import path
from .views import (
    DashboardAPIView,
    ProjectCreateView,
    ProjectDetailView,
    TicketCreateView,
    TicketDetailView,
    UserProfileView,
    StudentListView,
    SupervisorListView,
    ClientListView
)

urlpatterns = [
    # Dashboard
    path('dashboard/', DashboardAPIView.as_view(), name='dashboard'),
    
    # Projects
    path('projects/', ProjectCreateView.as_view(), name='project-create'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    
    # Tickets
    path('tickets/', TicketCreateView.as_view(), name='ticket-create'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    
    # User Profile
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    
    # Lists
    path('students/', StudentListView.as_view(), name='student-list'),
    path('supervisors/', SupervisorListView.as_view(), name='supervisor-list'),
    path('clients/', ClientListView.as_view(), name='client-list'),
]