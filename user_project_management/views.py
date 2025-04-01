from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import Project, ProjectFile, Comment
from .serializers import ProjectSerializer, ProjectFileSerializer, CommentSerializer

class ProjectCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProjectSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = Project.objects.filter(created_by=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class UploadFileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id, created_by=request.user)
        except Project.DoesNotExist:
            return Response({"error": "Project not found or you do not have permission."}, status=status.HTTP_404_NOT_FOUND)

        files = request.FILES.getlist('files')  # Handle multiple files
        if not files:
            return Response({"error": "No files uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        uploaded_files = []
        for file in files:
            file_instance = ProjectFile(project=project, file=file)
            file_instance.save()
            serializer = ProjectFileSerializer(file_instance, context={'request': request})
            uploaded_files.append(serializer.data)

        return Response(uploaded_files, status=status.HTTP_201_CREATED)


class AddCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id, created_by=request.user)
        except Project.DoesNotExist:
            return Response({"error": "Project not found or you do not have permission."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(project=project, created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)