# Generated by Django 5.1.6 on 2025-05-10 05:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_like_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='like',
            unique_together=set(),
        ),
    ]
