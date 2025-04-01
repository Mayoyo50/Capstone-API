from rest_framework import serializers
from .models import Project, ProjectFile, Comment
from django.utils.timezone import now

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'deadline',  # Optional field
            'field',  # Optional field
            'categories',  # Optional field
            'created_by',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_by']

    def validate_deadline(self, value):
        if value and value < now().date():
            raise serializers.ValidationError("The deadline cannot be in the past.")
        return value


class ProjectFileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = ProjectFile
        fields = ['id', 'file', 'file_url', 'uploaded_at']

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_by', 'created_at']
        read_only_fields = ['created_by']