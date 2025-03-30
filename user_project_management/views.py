# user_project_management/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from .models import Project, ProjectFile
from .serializers import ProjectSerializer
from .permissions import CanCreateProject
import mimetypes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import ProjectFile
import urllib.parse

class ProjectCreateView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [CanCreateProject]
    parser_classes = [MultiPartParser, JSONParser]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def create(self, request, *args, **kwargs):
        data = request.data.dict()
        files = request.FILES.getlist('files')
        
        serializer_data = {
            'title': data.get('title'),
            'description': data.get('description'),
            'deadline': data.get('deadline'),
        }
        
        serializer = self.get_serializer(data=serializer_data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save()
        
        # Process and validate files
        for file in files:
            self._create_project_file(project, file)
        
        response_serializer = self.get_serializer(project)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def _create_project_file(self, project, file):
        """Helper method to create project files with validation"""
        # Get file type
        content_type = file.content_type
        if not content_type:
            content_type, _ = mimetypes.guess_type(file.name)
        
        ProjectFile.objects.create(
            project=project,
            file=file,
            original_filename=file.name,
            file_type=content_type,
            file_size=file.size
        )


class ProjectFileAccessView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            file_obj = ProjectFile.objects.get(pk=pk)
            
            # Check if user has permission to access this file
            if file_obj.project.created_by != request.user:
                raise PermissionDenied("You don't have permission to access this file")
            
            # Return the Cloudinary URL
            return Response({
                'file_url': file_obj.file.url,
                'filename': urllib.parse.quote(file_obj.original_filename),
                'file_type': file_obj.file_type,
                'file_size': file_obj.file_size
            })
        
        except ProjectFile.DoesNotExist:
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)