from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()

class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'role', 'phone', 'institute']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source='userprofile')
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'profile']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        profile_data = representation.pop('profile')
        for key, value in profile_data.items():
            representation[key] = value
        return representation

class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='user_profile.user')
    
    class Meta:
        model = Client
        fields = ['id', 'user', 'company']

class SupervisorSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='user_profile.user')
    
    class Meta:
        model = Supervisor
        fields = ['id', 'user', 'department']

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='user_profile.user')
    
    class Meta:
        model = Student
        fields = ['id', 'user', 'student_id']

class ProjectSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    institute = InstituteSerializer()
    supervisor = SupervisorSerializer()
    students = StudentSerializer(many=True)
    
    class Meta:
        model = Project
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    assigned_to = UserSerializer()
    
    class Meta:
        model = Ticket
        fields = '__all__'

# Dashboard-specific serializers
class AcademicSupervisorSerializer(serializers.Serializer):
    fullName = serializers.SerializerMethodField()
    company = serializers.CharField(source='department')
    institute = serializers.SerializerMethodField()
    email = serializers.CharField(source='user_profile.user.email')
    phone = serializers.CharField(source='user_profile.phone')
    account = serializers.SerializerMethodField()

    def get_fullName(self, obj):
        return f"{obj.user_profile.user.first_name} {obj.user_profile.user.last_name}"

    def get_institute(self, obj):
        return obj.user_profile.institute.name if obj.user_profile.institute else ""

    def get_account(self, obj):
        return "Active" if obj.user_profile.user.is_active else "Inactive"

class DashboardProjectSerializer(serializers.Serializer):
    project = serializers.CharField(source='title')
    company = serializers.CharField(source='client.company')
    institute = serializers.CharField(source='institute.name')
    members = serializers.SerializerMethodField()
    deadline = serializers.DateField()
    completion = serializers.SerializerMethodField()

    def get_members(self, obj):
        return ", ".join([s.user_profile.user.get_full_name() for s in obj.students.all()])

    def get_completion(self, obj):
        return f"{obj.completion_percentage}%"

class ClientDashboardSerializer(serializers.Serializer):
    project = serializers.CharField(source='title')
    status = serializers.CharField(source='get_status_display')
    projectManager = serializers.SerializerMethodField()
    startDate = serializers.DateField(source='start_date')
    endDate = serializers.DateField(source='deadline')
    viewDetails = serializers.SerializerMethodField()

    def get_projectManager(self, obj):
        return obj.supervisor.user_profile.user.get_full_name() if obj.supervisor else ""

    def get_viewDetails(self, obj):
        return f"/projects/{obj.id}"

class StudentProjectSerializer(serializers.Serializer):
    project = serializers.CharField(source='title')
    projectClient = serializers.CharField(source='client.company')
    projectCategory = serializers.SerializerMethodField()
    dueDate = serializers.DateField(source='deadline')
    status = serializers.CharField(source='get_status_display')

    def get_projectCategory(self, obj):
        # In a real implementation, you might have categories in your model
        return "Software Development"