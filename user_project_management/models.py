# user_project_management/models.py
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
User = get_user_model()

class Institute(models.Model):
    name = models.CharField(max_length=200)
    short_code = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('SUPERVISOR', 'Supervisor'),
        ('CLIENT', 'Client'),
        ('STUDENT', 'Student'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20)
    institute = models.ForeignKey(Institute, on_delete=models.SET_NULL, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create UserProfile with role matching user_type
        user_profile = UserProfile.objects.create(
            user=instance,
            role=instance.user_type
        )
        
        # Create related objects based on role
        if instance.user_type == 'STUDENT':
            if not hasattr(user_profile, 'student'):
                Student.objects.create(user_profile=user_profile, student_id=f"S{user_profile.id}")
        elif instance.user_type == 'SUPERVISOR':
            if not hasattr(user_profile, 'supervisor'):
                Supervisor.objects.create(user_profile=user_profile, department="Default Department")
        elif instance.user_type == 'CLIENT':
            if not hasattr(user_profile, 'client'):
                Client.objects.create(user_profile=user_profile, company="Default Company")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.role = instance.user_type
        instance.userprofile.save()

class Client(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    company = models.CharField(max_length=200)
    
    def __str__(self):
        return self.company

class Supervisor(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    department = models.CharField(max_length=200)
    
    def __str__(self):
        return self.user_profile.user.get_full_name()

class Student(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.user_profile.user.get_full_name()} ({self.student_id})"

class Project(models.Model):
    STATUS_CHOICES = [
        ('PLANNING', 'Planning'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETE', 'Complete'),
        ('OVERDUE', 'Overdue'),
        ('PUBLISHED', 'Published'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.SET_NULL, null=True, blank=True)
    students = models.ManyToManyField(Student)
    start_date = models.DateField()
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANNING')
    completion_percentage = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title

class Ticket(models.Model):
    TYPE_CHOICES = [
        ('TECHNICAL', 'Technical'),
        ('ADMINISTRATIVE', 'Administrative'),
        ('URGENT', 'Urgent'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='created_tickets')
    assigned_to = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='assigned_tickets')
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    ticket_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    resolved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title