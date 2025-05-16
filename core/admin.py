from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.db.models import Count
from .models import (
    PasswordReset, Profile, Review, Course,
    Video, Comment, Like, Bookmark, Category
)

# Custom Admin Site Configuration
admin.site.site_header = 'TeckHub Admin'
admin.site.site_title = 'TeckHub Admin'
admin.site.index_title = 'Welcome to TeckHub Administration'

@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ('user', 'reset_id', 'created_when', 'is_active')
    search_fields = ('user__username', 'user__email')
    list_filter = ('created_when',)
    readonly_fields = ('reset_id', 'created_when')
    
    def is_active(self, obj):
        is_valid = obj.created_when + timezone.timedelta(minutes=10) > timezone.now()
        return format_html(
            '<span style="color: {};">●</span> {}',
            '#28a745' if is_valid else '#dc3545',
            'Active' if is_valid else 'Expired'
        )
    is_active.short_description = 'Status'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'display_image')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 30px; height: 30px; border-radius: 50%;" />', obj.image.url)
        return "No image"
    display_image.short_description = 'Profile Picture'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_rating', 'text_preview', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'text')
    
    def display_rating(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html('<span style="color: #ffc107;">{}</span>', stars)
    display_rating.short_description = 'Rating'
    
    def text_preview(self, obj):
        return obj.text[:50] + ('...' if len(obj.text) > 50 else '')
    text_preview.short_description = 'Review Text'

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'category', 'created_at', 'video_count')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'teacher__username', 'description')
    date_hierarchy = 'created_at'
    
    def video_count(self, obj):
        count = obj.videos.count()
        return format_html('<span class="badge" style="background-color: #6f42c1;">{}</span>', count)
    video_count.short_description = 'Videos'

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'created_at', 'views', 'engagement_stats')
    list_filter = ('course__category', 'created_at')
    search_fields = ('title', 'course__title')
    date_hierarchy = 'created_at'
    
    def engagement_stats(self, obj):
        likes = obj.likes.count()
        comments = obj.comments.count()
        return format_html(
            '<span title="Likes">👍 {}</span> &nbsp; <span title="Comments">💬 {}</span>',
            likes, comments
        )
    engagement_stats.short_description = 'Engagement'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'content_preview', 'created_at')
    list_filter = ('created_at', 'video__course__category')
    search_fields = ('content', 'user__username', 'video__title')
    date_hierarchy = 'created_at'
    
    def content_preview(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    content_preview.short_description = 'Comment'

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'video')
    list_filter = ('video__course__category',)
    search_fields = ('user__username', 'video__title')

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'created_at')
    list_filter = ('created_at', 'course__category')
    search_fields = ('user__username', 'course__title')
    date_hierarchy = 'created_at'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'course_count')
    search_fields = ('name',)
    
    def course_count(self, obj):
        count = Course.objects.filter(category=obj).count()
        return format_html('<span class="badge" style="background-color: #6f42c1;">{}</span>', count)
    course_count.short_description = 'Courses'
