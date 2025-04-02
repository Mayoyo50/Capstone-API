from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('cron/', include('cron.urls')),
    path('api/', include('user_project_management.urls')),
    path('', include('test_temp.urls')),
] + debug_toolbar_urls()