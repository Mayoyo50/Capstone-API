from rest_framework import serializers
from .models import Project, ProjectFile
from django.utils import timezone

class ProjectFileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProjectFile
        fields = ['id', 'original_filename', 'file_url', 'file_type', 'file_size', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']
    
    def get_file_url(self, obj):
        return obj.file.url if obj.file else None

class ProjectSerializer(serializers.ModelSerializer):
    files = ProjectFileSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'deadline', 'created_by', 'files', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_by', 'files', 'created_at', 'updated_at']
    
    def validate_deadline(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Deadline cannot be in the past.")
        return value