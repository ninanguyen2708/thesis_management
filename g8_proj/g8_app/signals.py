from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command

@receiver(post_migrate)
def create_test_users(sender, **kwargs):
    if sender.name == 'g8_app':
        call_command('create_users')
        call_command('add_data')