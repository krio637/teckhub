# Generated by Django 5.1.6 on 2025-05-09 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_course_playlist_video_like_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='teacher',
        ),
        migrations.RemoveField(
            model_name='playlist',
            name='course',
        ),
        migrations.RemoveField(
            model_name='like',
            name='user',
        ),
        migrations.RemoveField(
            model_name='like',
            name='video',
        ),
        migrations.RemoveField(
            model_name='video',
            name='playlist',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Course',
        ),
        migrations.DeleteModel(
            name='Like',
        ),
        migrations.DeleteModel(
            name='Playlist',
        ),
        migrations.DeleteModel(
            name='Video',
        ),
    ]
