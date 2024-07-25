from django.core.management.base import BaseCommand
from ...models import Project, Supervisor, Category, Location, Department, CustomUser
from ...classes import thesisList
from ...views import loc, dep, cat, sup

class Command(BaseCommand):
    help = 'Populates the database with sample data'
    
    def handle(self, *args, **options):
        # Supervisors
        supervisors = {}
        for name in sup:
            user, _ = CustomUser.objects.get_or_create(
                username=name.lower().replace(" ", ""),
                defaults={
                    'email': f'{name.lower().replace(" ", "")}@cdu.edu',
                    'is_supervisor': True
                }
            )
            supervisor, _ = Supervisor.objects.update_or_create(
                user=user,
                defaults={'name': name}
            )
            supervisors[name] = supervisor

        # Categories
        categories = {}
        for name in cat:
            category, created = Category.objects.update_or_create(name=name)
            categories[name] = category

        # Locations
        locations = {}
        for name in loc:
            location, created = Location.objects.update_or_create(name=name)
            locations[name] = location

        # Departments
        departments = {}
        for name in dep:
            department, created = Department.objects.update_or_create(name=name)
            departments[name] = department

        # Projects from thesisList
        for topic in thesisList:
            project_supervisor = supervisors.get(topic.supervisor)
            if not project_supervisor:
                self.stdout.write(self.style.WARNING(f'Supervisor "{topic.supervisor}" not found. Skipping project "{topic.title}".'))
                continue

            project, created = Project.objects.update_or_create(
                topic_number=topic.id,
                defaults={
                    'title': topic.title,
                    'description': topic.des,
                    'bullet_points': '\n'.join(topic.desList) if topic.desList else '',
                    'supervisors': project_supervisor,
                }
            )
            
            project_categories = [categories[cat] for cat in topic.category if cat in categories]
            project_locations = [locations[loc] for loc in topic.loc if loc in locations]
            project_departments = [departments[dep] for dep in topic.dep if dep in departments]
            
            project.category.set(project_categories)
            project.locations.set(project_locations)
            project.departments.set(project_departments)
            project.save()

        self.stdout.write(self.style.SUCCESS('Sample data populated successfully.'))
