from django.db import migrations

def clear_profiles(apps, schema_editor):
    Profile = apps.get_model('core', 'Profile')
    Profile.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0018_alter_profile_image'),  # Make sure this matches your last migration
    ]

    operations = [
        migrations.RunPython(clear_profiles),
    ] 