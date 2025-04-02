# user_project_management/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from datetime import date, timedelta
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status

class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        
        # Original code
        try:
            user_profile = request.user.userprofile
            role = user_profile.role
            
            if role == 'ADMIN':
                return self.admin_dashboard(request)
            elif role == 'SUPERVISOR':
                return self.supervisor_dashboard(request)
            elif role == 'CLIENT':
                return self.client_dashboard(request)
            elif role == 'STUDENT':
                return self.student_dashboard(request)
            else:
                return Response({
                    "error": "Invalid role", 
                    "debug_info": {
                        "role_found": role,
                        "user_type": getattr(user, 'user_type', 'Not Found')
                    }
                }, status=400)
        except Exception as e:
            return Response({
                "error": "Error processing request",
                "message": str(e)
            }, status=500)
    
    def admin_dashboard(self, request):
        active_page = request.query_params.get('page', 'dashboard')
        
        response_data = {
            'navItems': [
                {'id': 1, 'label': 'Dashboard', 'icon': 'House'},
                {'id': 2, 'label': 'Academic Supervisors', 'icon': 'User'},
                {'id': 3, 'label': 'Industry Clients', 'icon': 'Users'},
                {'id': 4, 'label': 'Projects', 'icon': 'FileText'},
                {'id': 5, 'label': 'Tickets', 'icon': 'Bookmark'}
            ],
            'userType': 'ADMIN'
        }
        
        if active_page == 'academic_supervisors':
            supervisors = Supervisor.objects.select_related(
                'user_profile__user', 
                'user_profile__institute'
            ).all()
            response_data.update({
                'data': AcademicSupervisorSerializer(supervisors, many=True).data,
                'columns': [
                    {'key': 'fullName', 'title': 'Full Name'},
                    {'key': 'company', 'title': 'Department'},
                    {'key': 'institute', 'title': 'Institute'},
                    {'key': 'email', 'title': 'Email'},
                    {'key': 'phone', 'title': 'Phone Number'},
                    {'key': 'account', 'title': 'Account Status'}
                ]
            })
        elif active_page == 'industry_clients':
            clients = Client.objects.select_related(
                'user_profile__user', 
                'user_profile__institute'
            ).all()
            response_data.update({
                'data': ClientSerializer(clients, many=True).data,
                'columns': [
                    {'key': 'user.first_name', 'title': 'First Name'},
                    {'key': 'user.last_name', 'title': 'Last Name'},
                    {'key': 'company', 'title': 'Company'},
                    {'key': 'user.email', 'title': 'Email'},
                    {'key': 'user.phone', 'title': 'Phone'},
                    {'key': 'user.account', 'title': 'Account Status'}
                ]
            })
        elif active_page == 'projects':
            projects = Project.objects.select_related(
                'client', 'institute', 'supervisor'
            ).prefetch_related('students').all()
            response_data.update({
                'data': DashboardProjectSerializer(projects, many=True).data,
                'columns': [
                    {'key': 'project', 'title': 'Project'},
                    {'key': 'company', 'title': 'Company'},
                    {'key': 'institute', 'title': 'Institute'},
                    {'key': 'members', 'title': 'Members'},
                    {'key': 'deadline', 'title': 'Deadline'},
                    {'key': 'completion', 'title': 'Completion'}
                ]
            })
        elif active_page == 'tickets':
            tickets = Ticket.objects.select_related(
                'created_by__user',
                'assigned_to__user'
            ).all()
            response_data.update({
                'data': TicketSerializer(tickets, many=True).data,
                'columns': [
                    {'key': 'created_by.user.first_name', 'title': 'Created By'},
                    {'key': 'assigned_to.user.first_name', 'title': 'Assigned To'},
                    {'key': 'title', 'title': 'Title'},
                    {'key': 'created_at', 'title': 'Created Date'},
                    {'key': 'due_date', 'title': 'Due Date'},
                    {'key': 'ticket_type', 'title': 'Type'}
                ]
            })
        else:  # Admin dashboard
            response_data.update({
                'data': {
                    'stats': {
                        'total_users': User.objects.count(),
                        'active_projects': Project.objects.filter(status='IN_PROGRESS').count(),
                        'pending_tickets': Ticket.objects.filter(resolved=False).count(),
                        'overdue_projects': Project.objects.filter(
                            deadline__lt=date.today(), 
                            status__in=['PLANNING', 'IN_PROGRESS']
                        ).count()
                    }
                },
                'columns': []
            })
        
        return Response(response_data)
    
    def supervisor_dashboard(self, request):
        active_page = request.query_params.get('page', 'track_progress')
        supervisor = request.user.userprofile.supervisor
        
        response_data = {
            'navItems': [
                {'id': 1, 'label': 'Track Progress', 'icon': 'ChartBar'},
                {'id': 2, 'label': 'Monitor Students', 'icon': 'Users'},
                {'id': 3, 'label': 'Pending Approvals', 'icon': 'CheckCircle'}
            ],
            'userType': 'SUPERVISOR'
        }
        
        if active_page == 'track_progress':
            projects = Project.objects.filter(
                supervisor=supervisor
            ).select_related(
                'client', 'institute'
            ).prefetch_related('students')
            
            response_data.update({
                'data': DashboardProjectSerializer(projects, many=True).data,
                'columns': [
                    {'key': 'project', 'title': 'Project'},
                    {'key': 'company', 'title': 'Company'},
                    {'key': 'institute', 'title': 'Institute'},
                    {'key': 'members', 'title': 'Members'},
                    {'key': 'deadline', 'title': 'Deadline'},
                    {'key': 'completion', 'title': 'Completion'}
                ]
            })
        elif active_page == 'monitor_students':
            students = Student.objects.filter(
                project__supervisor=supervisor
            ).distinct().select_related(
                'user_profile__user',
                'user_profile__institute'
            )
            
            response_data.update({
                'data': [{
                    'student': f"{s.user_profile.user.first_name} {s.user_profile.user.last_name}",
                    'institute': s.user_profile.institute.name if s.user_profile.institute else '',
                    'project': ', '.join([p.title for p in s.project_set.all()]),
                    'performance': 'Excellent',  # This would come from actual evaluations
                    'industry': ', '.join(list(set([p.client.company for p in s.project_set.all()]))),
                    'action': 'Review'
                } for s in students],
                'columns': [
                    {'key': 'student', 'title': 'Student'},
                    {'key': 'institute', 'title': 'Institute'},
                    {'key': 'project', 'title': 'Project'},
                    {'key': 'performance', 'title': 'Performance'},
                    {'key': 'industry', 'title': 'Industry'},
                    {'key': 'action', 'title': 'Action'}
                ]
            })
        else:  # Pending Approvals
            projects = Project.objects.filter(
                supervisor=supervisor,
                status='PLANNING'
            ).select_related('client', 'institute')
            
            response_data.update({
                'data': [{
                    'project': p.title,
                    'team': ', '.join([s.user_profile.user.get_full_name() for s in p.students.all()]),
                    'projectManager': p.supervisor.user_profile.user.get_full_name(),
                    'viewDetails': f"/projects/{p.id}",
                    'pendingApproval': 'Project Plan'  # This would be more specific in real implementation
                } for p in projects],
                'columns': [
                    {'key': 'project', 'title': 'Project'},
                    {'key': 'team', 'title': 'Team'},
                    {'key': 'projectManager', 'title': 'Project Manager'},
                    {'key': 'viewDetails', 'title': 'View Details'},
                    {'key': 'pendingApproval', 'title': 'Pending Approval'}
                ]
            })
        
        return Response(response_data)
    
    def client_dashboard(self, request):
        active_page = request.query_params.get('page', 'dashboard')
        client = request.user.userprofile.client
        
        response_data = {
            'navItems': [
                {'id': 1, 'label': 'Dashboard', 'icon': 'House'},
                {'id': 2, 'label': 'Track Progress', 'icon': 'ChartBar'},
                {'id': 3, 'label': 'Pending Approvals', 'icon': 'Clock'}
            ],
            'userType': 'CLIENT',
            'showNewProjectButton': True
        }
        
        projects = Project.objects.filter(client=client)
        
        if active_page == 'track_progress':
            response_data.update({
                'data': [{
                    'project': p.title,
                    'projectManager': p.supervisor.user_profile.user.get_full_name() if p.supervisor else '',
                    'startDate': p.start_date,
                    'endDate': p.deadline,
                    'status': p.get_status_display(),
                    'progress': f"{p.completion_percentage}%"
                } for p in projects],
                'columns': [
                    {'key': 'project', 'title': 'Project'},
                    {'key': 'projectManager', 'title': 'Project Manager'},
                    {'key': 'startDate', 'title': 'Start Date'},
                    {'key': 'endDate', 'title': 'End Date'},
                    {'key': 'status', 'title': 'Project Status'},
                    {'key': 'progress', 'title': 'Progress'}
                ]
            })
        elif active_page == 'pending_approvals':
            pending_projects = projects.filter(status='PLANNING')
            
            response_data.update({
                'data': [{
                    'project': p.title,
                    'team': ', '.join([s.user_profile.user.get_full_name() for s in p.students.all()]),
                    'projectManager': p.supervisor.user_profile.user.get_full_name() if p.supervisor else '',
                    'viewDetails': f"/projects/{p.id}",
                    'pendingApproval': 'Initial Approval'
                } for p in pending_projects],
                'columns': [
                    {'key': 'project', 'title': 'Project'},
                    {'key': 'team', 'title': 'Team'},
                    {'key': 'projectManager', 'title': 'Project Manager'},
                    {'key': 'viewDetails', 'title': 'View Details'},
                    {'key': 'pendingApproval', 'title': 'Pending Approval'}
                ]
            })
        else:  # Client dashboard
            response_data.update({
                'data': [{
                    'project': p.title,
                    'status': p.get_status_display(),
                    'projectManager': p.supervisor.user_profile.user.get_full_name() if p.supervisor else '',
                    'startDate': p.start_date,
                    'endDate': p.deadline,
                    'viewDetails': f"/projects/{p.id}"
                } for p in projects],
                'columns': [
                    {'key': 'project', 'title': 'Project'},
                    {'key': 'status', 'title': 'Project Status'},
                    {'key': 'projectManager', 'title': 'Project Manager'},
                    {'key': 'startDate', 'title': 'Start Date'},
                    {'key': 'endDate', 'title': 'End Date'},
                    {'key': 'viewDetails', 'title': 'View Details'}
                ]
            })
        
        return Response(response_data)
    
    def student_dashboard(self, request):
        active_page = request.query_params.get('page', 'dashboard')
        student = request.user.userprofile.student
        
        response_data = {
            'navItems': [
                {'id': 1, 'label': 'Dashboard', 'icon': 'House'},
                {'id': 2, 'label': 'Projects', 'icon': 'FileText'},
                {'id': 3, 'label': 'Mail', 'icon': 'Mail'},
                {'id': 4, 'label': 'Track Project', 'icon': 'ChartBar'}
            ],
            'userType': 'STUDENT'
        }
        
        projects = student.project_set.all()
        
        if active_page == 'projects':
            response_data.update({
                'data': [{
                    'project': p.title,
                    'projectClient': p.client.company,
                    'projectCategory': 'Software Development',  # This would come from project data
                    'dueDate': p.deadline,
                    'status': p.get_status_display()
                } for p in projects],
                'columns': [
                    {'key': 'project', 'title': 'Project'},
                    {'key': 'projectClient', 'title': 'Project Client'},
                    {'key': 'projectCategory', 'title': 'Project Category'},
                    {'key': 'dueDate', 'title': 'Due Date'},
                    {'key': 'status', 'title': 'Project Status'}
                ]
            })
        elif active_page == 'track_project':
            response_data.update({
                'data': [{
                    'project': p.title,
                    'company': p.client.company,
                    'institute': p.institute.name,
                    'members': ', '.join([
                        s.user_profile.user.get_full_name() 
                        for s in p.students.exclude(id=student.id)
                    ]),
                    'deadline': p.deadline,
                    'status': p.get_status_display()
                } for p in projects],
                'columns': [
                    {'key': 'project', 'title': 'Project'},
                    {'key': 'company', 'title': 'Company'},
                    {'key': 'institute', 'title': 'Institute'},
                    {'key': 'members', 'title': 'Members'},
                    {'key': 'deadline', 'title': 'Deadline'},
                    {'key': 'status', 'title': 'Status'}
                ]
            })
        elif active_page == 'mail':
            response_data.update({
                'data': [],  # Would come from messaging system
                'columns': []
            })
        else:  # Student dashboard
            response_data.update({
                'data': {
                    'stats': {
                        'active_projects': projects.filter(status='IN_PROGRESS').count(),
                        'upcoming_deadlines': projects.filter(
                            deadline__gte=date.today(),
                            deadline__lte=date.today() + timedelta(days=7)
                        ).count()
                    }
                },
                'columns': []
            })
        
        return Response(response_data)

class ProjectCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        # For clients creating projects
        if hasattr(self.request.user.userprofile, 'client'):
            serializer.save(client=self.request.user.userprofile.client)
        else:
            serializer.save()

class ProjectDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        # Filter based on user role
        user_profile = self.request.user.userprofile
        if user_profile.role == 'CLIENT':
            return self.queryset.filter(client=user_profile.client)
        elif user_profile.role == 'SUPERVISOR':
            return self.queryset.filter(supervisor=user_profile.supervisor)
        elif user_profile.role == 'STUDENT':
            return self.queryset.filter(students=user_profile.student)
        return self.queryset

class TicketCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.userprofile)

class TicketDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class UserProfileView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user.userprofile

class StudentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        students = Student.objects.select_related(
            'user_profile__user',
            'user_profile__institute'
        ).all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

class SupervisorListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        supervisors = Supervisor.objects.select_related(
            'user_profile__user',
            'user_profile__institute'
        ).all()
        serializer = SupervisorSerializer(supervisors, many=True)
        return Response(serializer.data)

class ClientListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        clients = Client.objects.select_related(
            'user_profile__user',
            'user_profile__institute'
        ).all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)