from django.db import models
from users.models import User
from cloudinary.models import CloudinaryField

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    
    def __str__(self):
        return self.title

class ProjectFile(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='files')
    file = CloudinaryField('project_files', resource_type='auto')
    original_filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=50, blank=True)
    file_size = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.original_filename} ({self.project.title})"
    
    def save(self, *args, **kwargs):
        if not self.original_filename and hasattr(self.file, 'name'):
            self.original_filename = self.file.name
        super().save(*args, **kwargs)