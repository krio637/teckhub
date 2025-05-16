from django.core.management.base import BaseCommand
from core.models import Category

class Command(BaseCommand):
    help = 'Creates default categories for courses'

    def handle(self, *args, **kwargs):
        categories = [
            'Web Development',
            'Artificial Intelligence',
            'Data Science',
            'Cloud Computing',
            'Cybersecurity',
            'Machine Learning'
        ]

        for category_name in categories:
            Category.objects.get_or_create(name=category_name)
            self.stdout.write(self.style.SUCCESS(f'Successfully created category "{category_name}"')) 