# ----------------- LOGIN -----------------
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views.generic import View
from .classes import mem, sup
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View

class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')
    
class CustomLoginView(View):
    template_name = 'registration/login.html'

    def get(self, request):
        memb = []
        supp = []
        for m in mem:
            memb.append(m.name.lower().replace(" ", ""))
            
        for s in sup:
            supp.append(s.lower().replace(" ", ""))
        context = {
            'mem' : memb,
            'sup' : supp,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            memb = []
            supp = []
            for m in mem:
                memb.append(m.name.lower().replace(" ", ""))
                
            for s in sup:
                supp.append(s.lower().replace(" ", ""))
            context = {
                'mem' : memb,
                'sup' : supp,
                'error': 'Invalid username or password.'
            }
            return render(request, self.template_name, context)
        
# ----------------- STUDENT PERMISSION -----------------


#  ----------------- DASHBOARD -----------------
# >> import
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
# <<

class DashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'g8_app/dashboard.html'

    def test_func(self):
        return self.request.user.is_student or self.request.user.is_supervisor or self.request.user.is_unit_coordinator        
        
    def handle_no_permission(self):
        return redirect('home')     
    
# student dashboard
# >> import
from django.views.generic import ListView
from django.urls import reverse
from .mixins import (
    StudentRequiredMixin, 
    SupervisorRequiredMixin, 
    UnitCoordinatorRequiredMixin,
    SupervisorOrUnitCoordinatorRequiredMixin,
)
# <<

class StudentDashboardView(LoginRequiredMixin, StudentRequiredMixin, ListView):
    template_name = 'g8_app/students/dashboard/dashboard.html'
    context_object_name = 'expressions_of_interest'

    def get_queryset(self):
        return ExpressionOfInterest.objects.filter(student=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['waiting_list_count'] = self.get_queryset().filter(status='waiting').count()
        context['approved_list_count'] = self.get_queryset().filter(status='approved').count()
        return context
    
# supervisor dashboard

# >> import
from .mixins import SupervisorRequiredMixin
from django.views.generic import UpdateView
from .forms import ProjectEditRequestForm
from .models import Project, ProjectEditRequest, Supervisor, CustomUser, ProjectDeleteRequest
# <<

class SupervisorDashboardView(LoginRequiredMixin, SupervisorRequiredMixin, ListView):
    template_name = 'g8_app/supervisor/dashboard/dashboard.html'
    context_object_name = 'projects'

    def get_queryset(self):
        supervisor = get_object_or_404(Supervisor, user=self.request.user)
        return Project.objects.filter(supervisors=supervisor)   
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        supervisor = get_object_or_404(Supervisor, user=self.request.user)
        context['waiting_list_count'] = ExpressionOfInterest.objects.filter(supervisor=supervisor, status='waiting').count()
        context['approved_list_count'] = ExpressionOfInterest.objects.filter(supervisor=supervisor, status='approved').count()
        context['pending_list_count'] = ProjectEditRequest.objects.filter(created_by=self.request.user, status='waiting').count()
        context['deleting_list_count'] = ProjectDeleteRequest.objects.filter(created_by=self.request.user, status='waiting').count()
        return context
    
# unit coordinator dashboard
class UnitCoordinatorDashboardView(LoginRequiredMixin, UnitCoordinatorRequiredMixin, ListView):
    template_name = 'g8_app/unitCoordinator/dashboard/dashboard.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending_list_count'] = ProjectEditRequest.objects.filter(status='waiting').count()
        context['deleting_list_count'] = ProjectDeleteRequest.objects.filter(status='waiting').count()
        context['approved_list_count'] = ExpressionOfInterest.objects.filter(status='approved').count()
        return context 
# ----------------- STUDENTS -----------------
# Submit expression of interest
# >> import
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .forms import ExpressionOfInterestForm
from .models import ExpressionOfInterest, Project
from .mixins import StudentRequiredMixin, SupervisorOrStudentRequiredMixin
# <<

class SubmitExpressionOfInterestView(LoginRequiredMixin, StudentRequiredMixin, CreateView):
    model = ExpressionOfInterest
    form_class = ExpressionOfInterestForm
    template_name = 'g8_app/students/applicationForm.html'

    def form_valid(self, form):
        project = get_object_or_404(Project, topic_number=self.kwargs['project_id'])
        form.instance.project = project
        form.instance.student = self.request.user
        form.instance.supervisor = project.supervisors
        form.instance.status = 'waiting'
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = get_object_or_404(Project, topic_number=self.kwargs['project_id'])
        return context

    def get_success_url(self):
        return reverse_lazy('waiting_list')
    
class WaitingListView(LoginRequiredMixin, SupervisorOrStudentRequiredMixin, ListView):
    template_name = 'g8_app/students/dashboard/waitingList.html'
    context_object_name = 'expressions_of_interest'

    def get_queryset(self):
        if self.request.user.is_supervisor:
            supervisor = get_object_or_404(Supervisor, user=self.request.user)
            return ExpressionOfInterest.objects.filter(supervisor=supervisor, status='waiting')
        return ExpressionOfInterest.objects.filter(student=self.request.user, status='waiting')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['waiting_list_count'] = self.get_queryset().count()
        context['user'] = self.request.user
        return context

    def post(self, request, *args, **kwargs):
        expression_id = request.POST.get('expression_id')
        action = request.POST.get('action')
        if expression_id:
            if request.user.is_student:
                expression = ExpressionOfInterest.objects.filter(id=expression_id, student=self.request.user)
                expression.delete()
            elif request.user.is_supervisor:
                supervisor = get_object_or_404(Supervisor, user=self.request.user)
                expression = get_object_or_404(ExpressionOfInterest, id=expression_id, supervisor=supervisor)
                project = expression.project
                approved_groups = ExpressionOfInterest.objects.filter(project=project, status='approved').count()
                # already_in = ExpressionOfInterest.objects.filter(status='approved', member_names=expression.member_names).count()
                if action == 'approve' and approved_groups < 2:
                    expression.status = 'approved'
                    project.group_count += 1
                    project.save()
                    expression.save()
                elif action == 'reject':
                    expression.status = 'rejected'
                    expression.delete()
        return redirect('waiting_list')
        
class ApprovedListView(LoginRequiredMixin, ListView):
    template_name = 'g8_app/students/dashboard/approvedList.html'
    context_object_name = 'expressions_of_interest'

    def get_queryset(self):
        if self.request.user.is_student:
            return ExpressionOfInterest.objects.filter(student=self.request.user, status='approved')
        elif self.request.user.is_supervisor:
            supervisor = get_object_or_404(Supervisor, user=self.request.user)
            return ExpressionOfInterest.objects.filter(supervisor=supervisor, status='approved')
        else:
            return ExpressionOfInterest.objects.filter(status='approved')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['approved_list_count'] = self.get_queryset().count()
        return context
    
from django.views.generic import DetailView

class ProjectGroupListView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'g8_app/projectGroupList.html'
    context_object_name = 'project'
    pk_url_kwarg = 'project_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        if self.request.user.is_supervisor:
            supervisor = self.request.user.supervisor_profile
            context['groups'] = ExpressionOfInterest.objects.filter(project=project, status='approved', supervisor=supervisor)
        return context

    
# -------------------- EDIT PROJECT --------------------

from .mixins import SupervisorOrUnitCoordinatorRequiredMixin

class EditProjectView(LoginRequiredMixin, SupervisorOrUnitCoordinatorRequiredMixin, CreateView):
    model = ProjectEditRequest
    form_class = ProjectEditRequestForm
    template_name = 'g8_app/supervisor/editProject.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        project = get_object_or_404(Project, topic_number=self.kwargs['project_id'])
        if self.has_changes(project, form.cleaned_data):
            edit_request = form.save(commit=False)
            edit_request.project = project
            edit_request.created_by = self.request.user
            edit_request.status = 'waiting'
            edit_request.new_supervisor = project.supervisors
            edit_request.save()
            form.save_m2m()  # Save many-to-many relationships
            project.pending_changes = True
            project.save()
            return redirect('projDetails', id=project.topic_number)
        else:
            context = self.get_context_data(form=form)
            context['no_changes'] = 'No changes were made to the project details.'
            return self.render_to_response(context)
        
    def get_initial(self):
        project = get_object_or_404(Project, topic_number=self.kwargs['project_id'])
        initial = super().get_initial()
        initial['new_title'] = project.title
        initial['new_description'] = project.description
        initial['new_category'] = project.category.all()
        initial['new_locations'] = project.locations.all()
        initial['new_departments'] = project.departments.all()
        if self.request.user.is_unit_coordinator:
            initial['new_supervisor'] = [project.supervisor]
        return initial
    
    def has_changes(self, project, cleaned_data):
        return (
            cleaned_data['new_title'] != project.title or
            cleaned_data['new_description'] != project.description or
            set(cleaned_data['new_category']) != set(project.category.all()) or
            set(cleaned_data['new_locations']) != set(project.locations.all()) or
            set(cleaned_data['new_departments']) != set(project.departments.all()) or
            (self.request.user.is_unit_coordinator and cleaned_data['new_supervisor'] != project.supervisors)
        )
    
class PendingProjectEditListView(LoginRequiredMixin, SupervisorOrUnitCoordinatorRequiredMixin, ListView):
    model = ProjectEditRequest
    template_name = 'g8_app/supervisor/dashboard/pendingProjectList.html'
    context_object_name = 'edit_requests'

    def get_queryset(self):
        if self.request.user.is_supervisor:
            return ProjectEditRequest.objects.filter(created_by=self.request.user, status='waiting')
        elif self.request.user.is_unit_coordinator:
            return ProjectEditRequest.objects.filter(status='waiting') 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending_list_count'] = self.get_queryset().count()
        context['edit_requests'] = self.get_queryset()
        return context

    def post(self, request, *args, **kwargs):
        edit_id = request.POST.get('edit_id')
        if edit_id:
            edit = ProjectEditRequest.objects.get(id=edit_id, created_by=request.user)
            edit.delete()
        return redirect('pending_project_edit_list')
    
from django.views.generic import DetailView
from django.shortcuts import redirect
from .models import ProjectEditRequest
from .forms import ProjectEditRequestForm
from .mixins import UnitCoordinatorRequiredMixin

class PendingProjectEditDetailView(LoginRequiredMixin, SupervisorOrUnitCoordinatorRequiredMixin, DetailView):
    model = ProjectEditRequest
    template_name = 'g8_app/supervisor/dashboard/pendingProjectDetail.html'
    context_object_name = 'edit_request'
    pk_url_kwarg = 'edit_request_id'

    def get_queryset(self):
        if self.request.user.is_supervisor:
            # supervisor = get_object_or_404(Supervisor, user=self.request.user)
            return ProjectEditRequest.objects.filter(created_by=self.request.user)
        elif self.request.user.is_unit_coordinator:
            return ProjectEditRequest.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_supervisor:
            supervisor = get_object_or_404(Supervisor, user=self.request.user)
            context['supervisors'] = [supervisor]
        else:
            edit_request = self.get_object()
            context['supervisors'] = edit_request.project.supervisors
        context['user'] = self.request.user
        return context

# Unit Coordinator views
from .mixins import UnitCoordinatorRequiredMixin

import json
from django.views.generic import UpdateView
from django.shortcuts import redirect

class ApproveProjectEditView(LoginRequiredMixin, UnitCoordinatorRequiredMixin, UpdateView):
    model = ProjectEditRequest
    form_class = ProjectEditRequestForm
    template_name = 'g8_app/supervisor/dashboard/pendingProjectDetail.html'
    pk_url_kwarg = 'edit_request_id'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        action = request.POST.get('action')
        print(f"Action: {action}")
        
        if action == 'approve':
            self.approve_request()
        elif action == 'reject':
            self.reject_request()
        
        return redirect('pending_project_edit_list')
    
    def approve_request(self):
        edit_request = self.get_object()
        project = edit_request.project

        print(f'Approving Edit Request: {edit_request}')
        print(f'Project Before Update: {project}')

        if edit_request.new_title and edit_request.new_title != project.title:
            project.title = edit_request.new_title
        if edit_request.new_description and edit_request.new_description != project.description:
            project.description = edit_request.new_description
        if self.request.user.is_unit_coordinator:
            if edit_request.new_supervisor != project.supervisors:
                project.supervisors = edit_request.new_supervisor
        else:
            supervisor = self.request.user.supervisor_profile
            if edit_request.new_supervisor != supervisor:
                project.supervisors = edit_request.new_supervisor
        if set(edit_request.new_category.all()) != set(project.category.all()):
            project.category.set(edit_request.new_category.all())
        if set(edit_request.new_locations.all()) != set(project.locations.all()):
            project.locations.set(edit_request.new_locations.all())
        if set(edit_request.new_departments.all()) != set(project.departments.all()):
            project.departments.set(edit_request.new_departments.all())

        project.pending_changes = False
        project.save()

        print(f'Project After Update: {project}')

        edit_request.status = 'approved'
        edit_request.delete()
        
    def reject_request(self):
        edit_request = self.object
        print(f'Rejecting Edit Request: {edit_request}')
        edit_request.delete()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending_list_count'] = ProjectEditRequest.objects.filter(status='waiting').count()
        context['edit_requests'] = ProjectEditRequest.objects.filter(status='waiting')
        return context

class PendingEditRequestsView(LoginRequiredMixin, UnitCoordinatorRequiredMixin, ListView):
    model = ProjectEditRequest
    template_name = 'g8_app/supervisor/dashboard/pendingProjectDetail.html'
    context_object_name = 'edit_requests'

    def get_queryset(self):
        return ProjectEditRequest.objects.filter(status='waiting')
    
# ----------------- DELETE PROJECT -----------------
# >> import
from django.views.generic import CreateView
from .models import ProjectDeleteRequest, Project
# <<

class RequestProjectDeleteView(LoginRequiredMixin, SupervisorOrUnitCoordinatorRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, topic_number=self.kwargs['project_id'])

        ProjectDeleteRequest.objects.create(
            project=project,
            created_by=request.user,
            status='waiting'
        )

        if request.user.is_unit_coordinator:
            return redirect('unit_coordinator_dashboard')
        else:
            return redirect('supervisor_dashboard')

    def get(self, request, *args, **kwargs):
        return redirect('projDetails', id=self.kwargs['project_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = get_object_or_404(Project, topic_number=self.kwargs['project_id'])
        if self.request.user.is_unit_coordinator:
            context['deleting_list_count'] = ProjectDeleteRequest.objects.filter(status='waiting')
        else: 
            context['deleting_list_count'] = ProjectDeleteRequest.objects.filter(created_by=self.request.user, status='waiting')
        return context

class PendingProjectDeleteRequestsView(LoginRequiredMixin, SupervisorOrUnitCoordinatorRequiredMixin, ListView):
    model = ProjectDeleteRequest
    template_name = 'g8_app/supervisor/dashboard/pendingProjectDeleteRequests.html'
    context_object_name = 'delete_requests'

    def get_queryset(self):
        print(f"User: {self.request.user.username}, is_supervisor: {self.request.user.is_supervisor}")
        return ProjectDeleteRequest.objects.filter(status='waiting')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deleting_list_count'] = self.get_queryset().count()
        context['user'] = self.request.user
        return context
    
    def post(self, request, *args, **kwargs):
        delete_id = request.POST.get('delete_id')
        if delete_id:
            edit = ProjectDeleteRequest.objects.get(id=delete_id, created_by=request.user)
            edit.delete()
        return redirect('pending_project_delete_requests')

class ApproveProjectDeleteRequestView(LoginRequiredMixin, UnitCoordinatorRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        delete_request = get_object_or_404(ProjectDeleteRequest, pk=kwargs['delete_request_id'])
        project = delete_request.project
        
        if 'approve' in request.POST and project.group_count == 0:
            project.save()
            project.delete()
        elif 'reject' in request.POST:
            delete_request.delete()
        return redirect('pending_project_delete_requests')
