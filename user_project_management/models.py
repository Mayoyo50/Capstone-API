from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField(null=True, blank=True)  # Optional field
    field = models.CharField(max_length=255, null=True, blank=True)  # Optional field
    categories = models.CharField(max_length=255, null=True, blank=True)  # Optional field
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.deadline and self.deadline < timezone.now().date():
            raise ValidationError({'deadline': 'The deadline cannot be in the past.'})

    def save(self, *args, **kwargs):
        # Call the clean method to validate before saving
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProjectFile(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='project_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for {self.project.title}"


class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.created_by.username} on {self.project.title}"