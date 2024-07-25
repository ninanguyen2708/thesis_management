"""
URL configuration for g8_proj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView

from g8_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    
    # ----------------PROJECTS----------------
    path('home/', views.home, name="home"),
    path('projects/', views.projList, name='projList'),
    # path('add_sample_data/', views.add_sample_data, name='add_sample_data'),
    path('projects/<int:id>', views.projDetails, name='projDetails'),
    path('project/<int:project_id>/groups/', views.ProjectGroupListView.as_view(), name='project_group_list'),
    path('about/', views.about, name='about'),
    
    # ----------------AUTHENTICATION----------------
    # path('register/student/', views.StudentRegistrationView.as_view(), name='student_register'),
    # path('register/supervisor/', views.SupervisorRegistrationView.as_view(), name='supervisor_register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    
    # ----------------AUTHENTICATION TEST----------------
    # path('create_test_users/', views.create_test_users, name='create_test_users'),
    # ----------------STUDENT PERMISSION----------------
    path('projects/<int:project_id>/apply/', views.SubmitExpressionOfInterestView.as_view(), name='submit_expression_of_interest'),
    
    # ----------------DASHBOARD----------------
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/student', views.StudentDashboardView.as_view(), name='student_dashboard'),
    path('dashboard/waiting-list', views.WaitingListView.as_view(), name='waiting_list'),
    path('dashboard/approved-list', views.ApprovedListView.as_view(), name='approved_list'),
    path('dashboard/supervisor', views.SupervisorDashboardView.as_view(), name='supervisor_dashboard'),
    path('dashboard/unit-coordinator', views.UnitCoordinatorDashboardView.as_view(), name='unit_coordinator_dashboard'),
    
    # ----------------PROJECT EDIT----------------
    path('project/<int:project_id>/edit/', views.EditProjectView.as_view(), name='edit_project'),
    path('pending_project_edits/', views.PendingProjectEditListView.as_view(), name='pending_project_edit_list'),
    path('edit_request/<int:edit_request_id>/approve/', views.ApproveProjectEditView.as_view(), name='approve_project_edit'),
    path('pending_edit_requests/', views.PendingEditRequestsView.as_view(), name='pending_edit_requests'),
    path('pending_project_edit/<int:edit_request_id>/', views.PendingProjectEditDetailView.as_view(), name='pending_project_edit_detail'),
    
    # ----------------PROJECT DELETE----------------
    path('project/<int:project_id>/request_delete/', views.RequestProjectDeleteView.as_view(), name='request_project_delete'),
    path('pending_project_delete_requests/', views.PendingProjectDeleteRequestsView.as_view(), name='pending_project_delete_requests'),
    path('delete_request/<int:delete_request_id>/approve/', views.ApproveProjectDeleteRequestView.as_view(), name='approve_project_delete_request'),
]
