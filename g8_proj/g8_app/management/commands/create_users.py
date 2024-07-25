from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from ...classes import mem
from ...views import sup
from ...models import Supervisor

class Command(BaseCommand):
    help = 'Creates test users for students, supervisors, and unit coordinators'

    def handle(self, *args, **options):
        User = get_user_model()

        # test user details
        test_users = [
            {
                'username': 'student',
                'email': 'student@example.com',
                'password': 'studentpassword',
                'is_student': True,
            },
            {
                'username': 'supervisor',
                'email': 'supervisor@example.com',
                'password': 'supervisorpassword',
                'is_supervisor': True,
            },
            {
                'username': 'coordinator',
                'email': 'coordinator@example.com',
                'password': 'coordinatorpassword',
                'is_unit_coordinator': True,
            },
        ]

        for name in sup:
            username = name.lower().replace(" ", "")
            email = username + '@cdu.edu'
            user, created = User.objects.update_or_create(
                username=username,
                defaults={
                    'email': email,
                    'is_student': False,
                    'is_supervisor': True,
                    'is_unit_coordinator': False,
                }
            )
            if created:
                user.set_password('supervisorpassword')
                user.save()
            Supervisor.objects.update_or_create(
                user=user,
                defaults={'name': name}
            )

        for user_data in mem:
            user, created = User.objects.update_or_create(
                username=user_data.name.lower().replace(" ", ""),
                defaults={
                    'email': str(user_data.id) + '@cdu.edu',
                    'is_student': True,
                }
            )
            if created:
                user.set_password('studentpassword')
                user.save()
        
        for user_data in test_users:
            user, created = User.objects.update_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'is_student': user_data.get('is_student', False),
                    'is_supervisor': user_data.get('is_supervisor', False),
                    'is_unit_coordinator': user_data.get('is_unit_coordinator', False),
                }
            )
            if created:
                user.set_password(user_data['password'])
                user.save()

        self.stdout.write(self.style.SUCCESS('Account created or updated successfully.'))