from django.urls import path
from . import views
from .views import about, add_review, contact_view

urlpatterns = [
    path('', views.home, name='home'),

    # Auth
    path('register/', views.RegisterView, name='register'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('password-reset-sent/<str:reset_id>/', views.PasswordResetSent, name='password-reset-sent'),
    path('reset-password/<uuid:reset_id>/', views.ResetPassword, name='reset-password'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),


    # Profile
    path('profile/', views.ProfileView, name='profile'),
    path('profile/bookmarks/', views.view_bookmarks, name='view_bookmarks'),
    path('profile/likes/', views.view_likes, name='view_likes'),
    path('profile/comments/', views.view_comments, name='view_comments'),
    path('profile/my-courses/', views.my_courses, name='my_courses'),
    path('courses/create/', views.create_course, name='create_course'),

    # Courses
    path('courses/', views.course_list, name='course_list'),
    path('courses/upload/', views.upload_course, name='upload_course'),
    path('courses/<int:course_id>/', views.course_detail_view, name='course_detail'),
    path('courses/<int:course_id>/playlist/', views.course_videos, name='course_videos'),
    path('courses/<int:course_id>/upload-video/', views.upload_video, name='upload_video'),
    path('course/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('course/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('courses/<int:course_id>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('course/<int:course_id>/playlist/', views.playlist_view, name='playlist'),

    # Video
    path('videos/<int:video_id>/', views.video_detail, name='video_detail'),

    # Teachers
    path('teachers/', views.teacher_list_view, name='teacher_list'),
    path('teacher/<int:teacher_id>/', views.teacher_profile_view, name='teacher_profile'),
    path('become-tutor/', views.become_tutor, name='become_tutor'),path('become-tutor/', views.become_tutor, name='become_tutor'),

    # Static
    path("about/", about, name="about"),
    path("add-review/", add_review, name="add_review"),
    path('contact/', contact_view, name='contact'),
    path('search/', views.search, name='search'),
]
