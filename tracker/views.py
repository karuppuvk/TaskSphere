from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from rest_framework import viewsets, permissions
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from accounts.models import User
from django.db.models import Prefetch

# --- DRF API VIEWS (With Custom Role Enforcement) ---
class IsAdminOrManagerOrReadOnly(permissions.BasePermission):
    """
    Custom permission: Only Admins or Managers can create/delete Projects/Tasks.
    Members can view and PATCH (update task status) elements assigned to them.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role in [
            "ADMIN",
            "MANAGER",
        ]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by("-created_at")
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminOrManagerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by("-created_at")
    serializer_class = TaskSerializer

    def get_permissions(self):
        # Allow any authenticated user to update task status (e.g., move to Done)
        if self.action in ["update", "partial_update"]:
            return [permissions.IsAuthenticated()]
        return [IsAdminOrManagerOrReadOnly()]


# --- FRONTEND HTML TEMPLATE VIEWS ---
@login_required(login_url='/login/')
def dashboard_view(request):
    try:
        if request.user.role == 'MEMBER':
            # Team members only see projects with their tasks, and only their assigned tasks
            projects = Project.objects.filter(tasks__assigned_to=request.user).distinct().prefetch_related(
                Prefetch('tasks', queryset=Task.objects.filter(assigned_to=request.user))
            )
        else:
            # Admins and Managers see all projects and all tasks
            projects = Project.objects.prefetch_related('tasks__assigned_to').all()
            
        return render(request, 'dashboard.html', {'projects': projects})
    except Exception as e:
        return render(request, 'dashboard.html', {'error': f"Database error: {str(e)}"})

    
@login_required(login_url='/login/')
def create_project_view(request):
    if request.user.role not in ['ADMIN', 'MANAGER']:
        return redirect('dashboard')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        try:
            if not title:
                raise ValidationError("Project title cannot be empty.")
            Project.objects.create(title=title, description=description, created_by=request.user)
            return redirect('dashboard')
        except Exception as e:
            return render(request, 'create_project.html', {'error': str(e)})
            
    return render(request, 'create_project.html')

@login_required(login_url='/login/')
def delete_project_view(request, project_id):
    if request.user.role not in ['ADMIN', 'MANAGER']:
        return redirect('dashboard')
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    return redirect('dashboard')

@login_required(login_url='/login/')
def create_task_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    # Fetch team members (or all users) so managers can choose who to assign
    team_members = User.objects.all()  # Or User.objects.filter(role='MEMBER')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        assigned_to_id = request.POST.get('assigned_to')
        
        try:
            if not title:
                raise ValidationError("Task title cannot be empty.")
            
            assigned_user = None
            if assigned_to_id:
                assigned_user = User.objects.get(id=assigned_to_id)
                
            Task.objects.create(
                title=title, 
                description=description, 
                project=project,
                assigned_to=assigned_user
            )
            return redirect('dashboard')
        except Exception as e:
            return render(request, 'create_task.html', {
                'project': project, 
                'team_members': team_members, 
                'error': str(e)
            })
            
    return render(request, 'create_task.html', {
        'project': project, 
        'team_members': team_members
    })
@login_required(login_url='/login/')
def update_task_view(request, task_id):
    if request.user.role not in ['ADMIN', 'MANAGER']:
        return redirect('dashboard')
    
    task = get_object_or_404(Task, id=task_id)
    team_members = User.objects.all()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        assigned_to_id = request.POST.get('assigned_to')
        status = request.POST.get('status')
        
        try:
            if not title:
                raise ValidationError("Task title cannot be empty.")
            
            task.title = title
            task.description = description
            task.status = status
            
            if assigned_to_id:
                task.assigned_to = User.objects.get(id=assigned_to_id)
            else:
                task.assigned_to = None
                
            task.save()
            return redirect('dashboard')
        except Exception as e:
            return render(request, 'update_task.html', {
                'task': task,
                'team_members': team_members,
                'error': str(e)
            })
            
    return render(request, 'update_task.html', {
        'task': task,
        'team_members': team_members
    })
@login_required(login_url='/login/')
def delete_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('dashboard')