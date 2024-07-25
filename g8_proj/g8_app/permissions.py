from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser

# permissions
supervisor_permissions = [
    'add_project',
    'change_project',
    'delete_project',
]

student_permissions = [
    'view_project',
    'apply_project',
]

unit_coordinator_permissions = [
    'approve_project',
    'publish_project',
]

# Create groups and assign permissions
@receiver(post_save, sender=CustomUser)
def create_user_groups(sender, instance, created, **kwargs):
    if created:
        if instance.is_supervisor:
            supervisor_group, _ = Group.objects.get_or_create(name='Supervisors')
            for perm_name in supervisor_permissions:
                perm_codename = f'g8_app.{perm_name}'
                perm = Permission.objects.get(codename=perm_codename)
                supervisor_group.permissions.add(perm)
            instance.groups.add(supervisor_group)

        elif instance.is_student:
            student_group, _ = Group.objects.get_or_create(name='Students')
            for perm_name in student_permissions:
                perm_codename = f'g8_app.{perm_name}'
                perm = Permission.objects.get(codename=perm_codename)
                student_group.permissions.add(perm)
            instance.groups.add(student_group)

        elif instance.is_unit_coordinator:
            unit_coordinator_group, _ = Group.objects.get_or_create(name='Unit Coordinators')
            for perm_name in unit_coordinator_permissions:
                perm_codename = f'g8_app.{perm_name}'
                perm = Permission.objects.get(codename=perm_codename)
                unit_coordinator_group.permissions.add(perm)
            instance.groups.add(unit_coordinator_group)