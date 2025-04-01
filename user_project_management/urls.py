from django.urls import path
from .views import ProjectCreateView, ProjectListView, UploadFileView, AddCommentView

urlpatterns = [
    path('', ProjectCreateView.as_view(), name='create-project'),
    path('list/', ProjectListView.as_view(), name='list-projects'),
    path('<int:project_id>/upload_file/', UploadFileView.as_view(), name='upload-file'),
    path('<int:project_id>/add_comment/', AddCommentView.as_view(), name='add-comment'),
]