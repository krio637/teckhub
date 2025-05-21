from django.db import models
from django.contrib.auth.models import User
import uuid

class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset for {self.user.username} at {self.created_when}"


class Profile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png', null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    bio = models.TextField(blank=True, null=True)
    teaching_style = models.CharField(max_length=50, blank=True, null=True)
    availability = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile" if self.user else "Unassigned Profile"

    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return '/media/profile_pics/default.png'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(choices=[(i, f"{i} ⭐") for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.rating} ⭐"


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='course_thumbnails/', null=True, blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_thumbnail_url(self):
        try:
            return self.thumbnail.url if self.thumbnail else '/static/images/default-thumbnail.jpg'
        except:
            return '/static/images/default-thumbnail.jpg'


class Video(models.Model):
    course = models.ForeignKey(Course, related_name='videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='video_thumbnails/')
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    @property
    def views_count(self):
        return self.views

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Comment(models.Model):
    video = models.ForeignKey(Video, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.video.title}"


class Like(models.Model):
    video = models.ForeignKey(Video, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_videos')

    def __str__(self):
        return f"{self.user.username} liked {self.video.title}"


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarked_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'course']

    def __str__(self):
        return f"{self.user.username} bookmarked {self.course.title}"
