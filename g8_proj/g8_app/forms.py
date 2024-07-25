from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Project, CustomUser, ExpressionOfInterest

class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        if commit:
            user.save()
        return user

class SupervisorRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_supervisor = True
        if commit:
            user.save()
        return user

class UnitCoordinatorRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_unit_coordinator = True
        if commit:
            user.save()
        return user
 
from .models import Supervisor

class ProjectForm(forms.ModelForm):
    supervisors = forms.ModelMultipleChoiceField(
        queryset=Supervisor.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Project
        fields = ['title', 'description', 'category', 'locations', 'departments', 'supervisors']
        widgets = {
            'category': forms.CheckboxSelectMultiple,
            'locations': forms.CheckboxSelectMultiple,
            'departments': forms.CheckboxSelectMultiple,
        }

    def save(self, commit=True):
        project = super().save(commit=False)

        if commit:
            project.save()
            self.save_m2m()  # Save many-to-many relationships

        return project
            
class ExpressionOfInterestForm(forms.ModelForm): #for student dashboard..... 
    member_names = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = ExpressionOfInterest
        fields = ['member_names']

    def clean_member_names(self):
        member_names = self.cleaned_data.get('member_names')
        names = [name.strip() for name in member_names.split(',')]
        if (len(names) < 2):
            raise forms.ValidationError("Please provide at least two member names.")
        return member_names 

from .models import ProjectEditRequest

from .models import Supervisor
from django import forms

class ProjectEditRequestForm(forms.ModelForm):
    new_supervisor = forms.ModelChoiceField(
        queryset=Supervisor.objects.all(),
        widget=forms.Select,
        required=False
    )
    
    class Meta:
        model = ProjectEditRequest
        fields = ['new_title', 'new_description', 'new_category', 'new_locations', 'new_departments', 'new_supervisor']
        widgets = {
            'new_category': forms.CheckboxSelectMultiple,
            'new_locations': forms.CheckboxSelectMultiple,
            'new_departments': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and not user.is_unit_coordinator:
            self.fields['new_supervisor'].disabled = True

    def save(self, commit=True):
        edit_request = super().save(commit=False)

        if commit:
            edit_request.save()
            self.save_m2m()  # Save many-to-many relationships

        return edit_request