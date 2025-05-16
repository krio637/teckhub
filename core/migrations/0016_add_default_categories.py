from django.db import migrations

def create_default_categories(apps, schema_editor):
    Category = apps.get_model('core', 'Category')
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

def remove_default_categories(apps, schema_editor):
    Category = apps.get_model('core', 'Category')
    Category.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0015_category_course_category'),
    ]

    operations = [
        migrations.RunPython(create_default_categories, remove_default_categories),
    ] 