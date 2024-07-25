from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Project, Supervisor, Category, Location, Department, CustomUser
from .forms import ProjectForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login

# classess.py 
from .classes import (
    thesisList, 
    mem,
    sup,
    loc,
    dep,
    cat,
)

# ----------------------------PROJECTS----------------------------

def home(request):
    return render(request, 'g8_app/home.html')

def projList(request):
    projects = Project.objects.all()
    
    selLoc = request.GET.get('location')  
    selDep = request.GET.get('department')
    selCat = request.GET.get('category')
    selSup = request.GET.get('supervisor')

    if (selLoc == None): 
        selLoc = ''
    if (selDep == None):
        selDep = ''
    if (selCat == None):
        selCat = ''
    if (selSup == None):
        selSup = ''  
    
    if selLoc:
        projects = projects.filter(locations__name=selLoc)
    if selDep:
        projects = projects.filter(departments__name=selDep)
    if selCat:
        projects = projects.filter(category__name=selCat)
    if selSup:
        projects = projects.filter(supervisors__name=selSup)
    page = request.GET.get('page', 1)
    paginator = Paginator(projects, 4)  

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)

    context = {
        'projects': projects,
        'dep': Department.objects.all(),
        'loc': Location.objects.all(),
        'cat': Category.objects.all(),
        'sup': CustomUser.objects.filter(is_supervisor=True),
        'selLoc': selLoc,
        'selDep': selDep,
        'selCat': selCat,
        'selSup': selSup,
        'user' : request.user,
    }
    return render(request, 'g8_app/projList.html', context)

def projDetails(request, id):
    project = get_object_or_404(Project, topic_number=id)
    locations = Location.objects.all()
    departments = Department.objects.all()
    bullet_points = [point for point in project.bullet_points.split('\n') if point.strip()]
    
    context = {
        'project': project,
        'loc': locations,
        'dep': departments,
        'bullet_points': bullet_points,
    }
    
    return render(request, 'g8_app/projDetails.html', context)

def about(request):
    context = {
        'mem': mem,
    }
    return render(request, 'g8_app/about.html', context)

# ------------ONLY WITH PERMISSIONS----------------
# >> import
    
# >> import
from .customViews import (
    SubmitExpressionOfInterestView,
    StudentDashboardView,
    SupervisorDashboardView,
    UnitCoordinatorDashboardView,
    DashboardView,
    WaitingListView,
    ApprovedListView,
    PendingEditRequestsView,
    EditProjectView,
    PendingProjectEditListView,
    ApproveProjectEditView,
    PendingProjectEditDetailView,
    RequestProjectDeleteView,
    PendingProjectDeleteRequestsView,
    ApproveProjectDeleteRequestView,
    ProjectGroupListView,
    CustomLogoutView,
    CustomLoginView,
)

from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    if request.user.is_student:
        return redirect('student_dashboard')
    elif request.user.is_supervisor:
        return redirect('supervisor_dashboard')
    elif request.user.is_unit_coordinator:
        return redirect('unit_coordinator_dashboard')
    else:
        return render(request, 'g8_app/dashboard.html')
    