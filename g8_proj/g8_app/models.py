from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    name = models.CharField(max_length=100)
    is_student = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    is_unit_coordinator = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Supervisor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='supervisor_profile')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Project(models.Model):
    topic_number = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    bullet_points = models.TextField(blank=True)
    supervisors = models.ForeignKey(Supervisor, on_delete=models.CASCADE, related_name='projects', null=True, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    locations = models.ManyToManyField(Location, blank=True)
    departments = models.ManyToManyField(Department, blank=True)
    group_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
class ExpressionOfInterest(models.Model): #student dashboard
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    member_names = models.TextField()

    def __str__(self):
        return f"{self.student.username} - {self.project.title}"
    
class ProjectEditRequest(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    new_title = models.CharField(max_length=200)
    new_description = models.TextField()
    new_supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)    
    new_category = models.ManyToManyField(Category, blank=True)
    new_locations = models.ManyToManyField(Location, blank=True)
    new_departments = models.ManyToManyField(Department, blank=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')

    def __str__(self):
        return f"Edit request for {self.project.title} by {self.created_by.username}"
    
class ProjectDeleteRequest(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')

    def __str__(self):
        return f"Delete request for {self.project.title} by {self.created_by.username}"
