from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import (
    CustomUser, 
    Project, 
    Supervisor, 
    Category, 
    Location, 
    Department, 
    ExpressionOfInterest, 
    ProjectEditRequest,
    ProjectDeleteRequest,
)

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_student', 'is_supervisor', 'is_unit_coordinator')
    list_filter = ('is_staff', 'is_student', 'is_supervisor', 'is_unit_coordinator')
    fieldsets = (
        (None, 
         {'fields': 
             ('username', 'email', 'password')}),
        ('Personal Info', 
         {'fields': 
             ('first_name', 'last_name')}),
        ('Permissions', 
         {'fields': 
             ('is_staff', 'is_active', 'is_student', 'is_supervisor', 'is_unit_coordinator')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_student', 'is_supervisor', 'is_unit_coordinator'),
        }),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('topic_number', 'title', 'get_supervisors', 'get_categories', 'get_locations', 'get_departments', 'description', 'get_bullet_points')

    def get_supervisors(self, obj):
        return ", ".join([supervisor.name for supervisor in obj.supervisors.all()])

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.category.all()])

    def get_locations(self, obj):
        return ", ".join([location.name for location in obj.locations.all()])

    def get_departments(self, obj):
        return ", ".join([department.name for department in obj.departments.all()])

    def get_bullet_points(self, obj):
        return "\n".join(obj.bullet_points.split('\n'))

    get_supervisors.short_description = 'Supervisors'
    get_categories.short_description = 'Categories'
    get_locations.short_description = 'Locations'
    get_departments.short_description = 'Departments'
    get_bullet_points.short_description = 'Bullet Points'
    
admin.site.register(Project, ProjectAdmin)
admin.site.register(Supervisor)
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Department)
admin.site.register(ExpressionOfInterest)
admin.site.register(ProjectEditRequest)
admin.site.register(ProjectDeleteRequest)

# Unregister the default Group model
admin.site.unregister(Group)