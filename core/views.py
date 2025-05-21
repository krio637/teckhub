from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.db.models import Q, Count
from django.db import transaction
from .models import Course, Category, Comment, Like, Profile, Video, Review, Bookmark, PasswordReset
from uuid import UUID
import uuid
from django.urls import reverse
import os
from collections import Counter
import re
from django.core.files.storage import default_storage

# ---------------------- Home & Auth Views ----------------------

@login_required
def home(request):
    total_likes = Like.objects.filter(user=request.user).count()
    total_comments = Comment.objects.filter(user=request.user).count()
    total_bookmarks = Bookmark.objects.filter(user=request.user).count()
    courses = Course.objects.all()[:5]  # Show only 5 latest courses

    # Get top 5 categories with their course counts
    categories = []
    for category in Category.objects.all():
        course_count = Course.objects.filter(category=category).count()
        categories.append({
            'name': category.name,
            'course_count': course_count,
            'id': category.id
        })
    # Sort categories by course count and get top 5
    categories = sorted(categories, key=lambda x: x['course_count'], reverse=True)[:5]

    # Find popular topics by analyzing course titles and descriptions
    # Get all course titles and descriptions
    course_texts = Course.objects.values_list('title', 'description')
    
    # Common programming topics to look for
    topic_patterns = {
        'python': {'pattern': r'python', 'icon': 'bi-filetype-py', 'name': 'Python'},
        'javascript': {'pattern': r'javascript|js', 'icon': 'bi-filetype-js', 'name': 'JavaScript'},
        'java': {'pattern': r'\bjava\b', 'icon': 'bi-file-earmark-code', 'name': 'Java'},
        'html': {'pattern': r'html', 'icon': 'bi-code', 'name': 'HTML'},
        'css': {'pattern': r'css', 'icon': 'bi-brush', 'name': 'CSS'},
        'react': {'pattern': r'react', 'icon': 'bi-code-square', 'name': 'React'},
        'angular': {'pattern': r'angular', 'icon': 'bi-code-slash', 'name': 'Angular'},
        'vue': {'pattern': r'vue', 'icon': 'bi-code-square', 'name': 'Vue.js'},
        'node': {'pattern': r'node\.?js', 'icon': 'bi-server', 'name': 'Node.js'},
        'php': {'pattern': r'php', 'icon': 'bi-file-earmark-code', 'name': 'PHP'},
        'sql': {'pattern': r'sql|mysql|postgresql', 'icon': 'bi-database', 'name': 'SQL'},
        'django': {'pattern': r'django', 'icon': 'bi-code-slash', 'name': 'Django'},
        'flutter': {'pattern': r'flutter', 'icon': 'bi-phone', 'name': 'Flutter'},
        'android': {'pattern': r'android', 'icon': 'bi-android2', 'name': 'Android'},
        'ios': {'pattern': r'ios|swift', 'icon': 'bi-apple', 'name': 'iOS'},
    }

    # Count topic occurrences
    topic_counts = {topic: 0 for topic in topic_patterns}
    
    for title, description in course_texts:
        text = f"{title} {description}".lower()
        for topic, info in topic_patterns.items():
            if re.search(info['pattern'], text):
                topic_counts[topic] += 1

    # Get top 5 topics
    popular_topics = {}
    for topic, count in sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        if count > 0:  # Only include topics that have courses
            popular_topics[topic] = {
                'name': topic_patterns[topic]['name'],
                'icon': topic_patterns[topic]['icon'],
                'count': count
            }

    return render(request, 'index.html', {
        'total_likes': total_likes,
        'total_comments': total_comments,
        'total_bookmarks': total_bookmarks,
        'courses': courses,
        'categories': categories,
        'topics': popular_topics,
    })

def RegisterView(request): 
    if request.method == "POST":
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        has_error = False
        if not username:
            has_error = True
            messages.error(request, "Username is required")
        elif User.objects.filter(username=username).exists():
            has_error = True
            messages.error(request, "Username already exists")

        if not email:
            has_error = True
            messages.error(request, "Email is required")
        elif User.objects.filter(email=email).exists():
            has_error = True
            messages.error(request, "Email already exists")

        if not first_name:
            has_error = True
            messages.error(request, "First name is required")

        if not last_name:
            has_error = True
            messages.error(request, "Last name is required")

        if not password1:
            has_error = True
            messages.error(request, "Password is required")
        elif len(password1) < 5:
            has_error = True
            messages.error(request, "Password must be at least 5 characters")
        elif password1 != password2:
            has_error = True
            messages.error(request, "Passwords do not match")

        if has_error:
            return redirect('register')

        try:
            with transaction.atomic():
                # First check if user exists
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Username already exists")
                    return redirect('register')
                
                # Create user first
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    first_name=first_name,
                    last_name=last_name
                )
                
                # Update the profile that was automatically created by the signal
                profile = Profile.objects.get(user=user)
                profile.role = 'student'
                profile.save()
                
                messages.success(request, "Account created. Login now")
                return redirect('login')
        except Exception as e:
            messages.error(request, f"Error creating account: {str(e)}")
            return redirect('register')

    return render(request, 'register.html')

def LoginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')

    return render(request, 'login.html')

def LogoutView(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

@login_required
def update_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        profile_pic = request.FILES.get('profile_pic')

        # Validate name
        if not name:
            messages.error(request, "Name cannot be empty.")
            return redirect('update_profile')

        # Validate email
        if not email:
            messages.error(request, "Email cannot be empty.")
            return redirect('update_profile')
        if User.objects.exclude(id=user.id).filter(email=email).exists():
            messages.error(request, "This email is already in use by another account.")
            return redirect('update_profile')

        # Handle password change if attempted
        if old_password or new_password or confirm_password:
            if not old_password:
                messages.error(request, "Please enter your current password to change it.")
                return redirect('update_profile')
            if not new_password:
                messages.error(request, "Please enter a new password.")
                return redirect('update_profile')
            if not confirm_password:
                messages.error(request, "Please confirm your new password.")
                return redirect('update_profile')
            
            if not user.check_password(old_password):
                messages.error(request, "Current password is incorrect.")
                return redirect('update_profile')
            
            if new_password != confirm_password:
                messages.error(request, "New passwords do not match.")
                return redirect('update_profile')
            
            if len(new_password) < 8:
                messages.error(request, "Password must be at least 8 characters long.")
                return redirect('update_profile')
            
            # Update password if all validations pass
            user.set_password(new_password)
            update_session_auth_hash(request, user)
            messages.success(request, "Password updated successfully.")

        # Update profile picture if provided
        if profile_pic:
            try:
                # Validate file size (max 5MB)
                if profile_pic.size > 5 * 1024 * 1024:
                    messages.error(request, "Profile picture size should not exceed 5MB.")
                    return redirect('update_profile')
                
                # Validate file type
                allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
                if profile_pic.content_type not in allowed_types:
                    messages.error(request, "Only JPEG, JPG and PNG files are allowed for profile picture.")
                    return redirect('update_profile')
                
                profile.image = profile_pic
                profile.save()
                messages.success(request, "Profile picture updated successfully.")
            except Exception as e:
                messages.error(request, f"Error uploading profile picture: {str(e)}")
                return redirect('update_profile')

        # Update user information
        try:
            user.first_name = name
            user.email = email
            user.save()
            messages.success(request, "Profile information updated successfully.")
        except Exception as e:
            messages.error(request, f"Error updating profile information: {str(e)}")
            return redirect('update_profile')

        return redirect('profile')

    return render(request, 'update_profile.html', {'user': user, 'profile': profile})


# ---------------------- Password Reset ----------------------

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        users = User.objects.filter(email=email)

        if users.exists():
            for user in users:
                reset = PasswordReset.objects.create(user=user, reset_id=uuid.uuid4())
                reset_link = request.build_absolute_uri(
                    reverse('reset-password', args=[str(reset.reset_id)])
                )

                send_mail(
                    subject='Password Reset',
                    message=f'Click the link to reset your password: {reset_link}',
                    from_email='teckhub782@email.com',
                    recipient_list=[user.email],
                    fail_silently=False,
                )

            messages.success(request, "Password reset email has been sent.")
            return redirect('login')
        else:
            messages.error(request, "No user found with this email.")
            return redirect('forgot_password')

    return render(request, 'forgot_password.html')


def ResetPassword(request, reset_id):
    # Validate that reset_id is a valid UUID
    try:
        reset_uuid = UUID(str(reset_id))  # This ensures it's a proper UUID format
        reset = PasswordReset.objects.get(reset_id=reset_uuid)
    except (ValueError, PasswordReset.DoesNotExist):
        messages.error(request, 'Invalid or expired reset link.')
        return redirect('forgot-password')

    # Check if the reset link has expired
    expiration = reset.created_when + timezone.timedelta(minutes=10)
    if timezone.now() > expiration:
        reset.delete()
        messages.error(request, 'Reset link has expired.')
        return redirect('forgot-password')

    if request.method == "POST":
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('reset-password', reset_id=reset_id)

        if len(password) < 5:
            messages.error(request, 'Password must be at least 5 characters.')
            return redirect('reset-password', reset_id=reset_id)

        # Reset the user's password
        user = reset.user
        user.set_password(password)
        user.save()

        # Delete the reset record
        reset.delete()

        messages.success(request, 'Your password has been reset. Please log in.')
        return redirect('login')

    return render(request, 'reset_password.html', {'reset_id': reset_id})


def PasswordResetSent(request, reset_id):
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'password_reset_sent.html')
    else:
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')


# ---------------------- Profile ----------------------

@login_required
def ProfileView(request):
    user = request.user
    profile = user.profile

    # Get user's bookmarked courses
    bookmarked_courses = Bookmark.objects.filter(user=user)
    
    # Get user's liked videos
    liked_videos = Like.objects.filter(user=user)
    
    # Get user's comments
    comments = Comment.objects.filter(user=user)
    
    # Get teacher's uploaded courses if user is a teacher
    uploaded_courses = None
    if profile.role == 'teacher':
        uploaded_courses = Course.objects.filter(teacher=user)

    context = {
        'user': user,
        'profile': profile,
        'bookmarked_courses': bookmarked_courses,
        'liked_videos': liked_videos,
        'comments': comments,
        'uploaded_courses': uploaded_courses,
    }

    return render(request, 'profile.html', context)


# ---------------------- Course & Video ----------------------

@login_required
def create_course(request):
    if request.user.profile.role != 'teacher':
        messages.error(request, "You must be a teacher to create courses.")
        return redirect('profile')
        
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        thumbnail = request.FILES.get('thumbnail')
        category_id = request.POST.get('category')
        
        try:
            category = Category.objects.get(id=category_id) if category_id else None
            
            Course.objects.create(
                title=title,
                description=description,
                thumbnail=thumbnail,
                teacher=request.user,
                category=category,
            )
            messages.success(request, "Course created successfully!")
            return redirect('profile')
        except Category.DoesNotExist:
            messages.error(request, "Selected category does not exist.")
            return redirect('create_course')
            
    categories = Category.objects.all()
    return render(request, 'create_course.html', {'categories': categories})

@login_required
def my_courses(request):
    courses = Course.objects.filter(teacher=request.user)
    course_data = [{'course': c, 'video_count': c.videos.count()} for c in courses]
    return render(request, 'my_courses.html', {'course_data': course_data})

@login_required
def course_list(request):
    courses = Course.objects.all()
    
    # Filter by category
    category = request.GET.get('category')
    if category:
        # Convert URL-friendly format to display format (e.g., 'web-development' to 'Web Development')
        category_name = category.replace('-', ' ').title()
        courses = courses.filter(category__name=category_name)
    
    # Filter by topic
    topic = request.GET.get('topic')
    if topic:
        # Search in course title and description
        courses = courses.filter(title__icontains=topic) | courses.filter(description__icontains=topic)
    
    user_bookmarks = Bookmark.objects.filter(user=request.user).values_list('course_id', flat=True)
    categories = Category.objects.all()
    
    context = {
        'courses': courses,
        'categories': categories,
        'user_bookmarks': user_bookmarks,
        'selected_category': category.replace('-', ' ').title() if category else None,
        'selected_topic': topic.upper() if topic else None
    }
    
    return render(request, 'course_list.html', context)

@login_required
def course_videos(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    videos = course.videos.all()
    return render(request, 'playlist.html', {'course': course, 'videos': videos})

@login_required
def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video.views += 1
    video.save()

    comments = video.comments.all().order_by('-created_at')
    liked = Like.objects.filter(video=video, user=request.user).exists()

    if request.method == 'POST':
        if 'like' in request.POST:
            Like.objects.get_or_create(video=video, user=request.user)
        elif 'unlike' in request.POST:
            Like.objects.filter(video=video, user=request.user).delete()
        elif 'content' in request.POST:
            content = request.POST.get('content')
            if content:
                Comment.objects.create(video=video, user=request.user, content=content)
        return redirect('video_detail', video_id=video.id)

    return render(request, 'video_detail.html', {
        'video': video,
        'comments': comments,
        'likes_count': video.likes.count(),
        'liked': liked,
    })

@login_required
def upload_course(request):
    if request.user.profile.role != 'teacher':
        return HttpResponseForbidden("Only teachers can upload courses.")

    if request.method == 'POST':
        Course.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            thumbnail=request.FILES.get('thumbnail'),
            teacher=request.user
        )
        return redirect('course_list')

    return render(request, 'upload_course.html')

@login_required
def upload_video(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user != course.teacher:
        return HttpResponseForbidden("You are not allowed to upload to this course.")

    if request.method == 'POST':
        Video.objects.create(
            course=course,
            title=request.POST.get('title'),
            video_file=request.FILES.get('video_file'),
            thumbnail=request.FILES.get('thumbnail')
        )
        return redirect('course_videos', course_id=course.id)

    return render(request, 'upload_video.html', {'course': course})

@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, teacher=request.user)

    if request.method == 'POST':
        course.title = request.POST.get('title')
        course.description = request.POST.get('description')
        category_id = request.POST.get('category')
        
        try:
            course.category = Category.objects.get(id=category_id) if category_id else None
        except Category.DoesNotExist:
            messages.error(request, "Selected category does not exist.")
            return redirect('edit_course', course_id=course_id)
            
        if 'thumbnail' in request.FILES:
            course.thumbnail = request.FILES['thumbnail']
        
        course.save()
        messages.success(request, 'Course updated successfully.')
        return redirect('profile')

    categories = Category.objects.all()
    return render(request, 'edit_course.html', {'course': course, 'categories': categories})

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    course.delete()
    messages.success(request, 'Course deleted successfully.')
    return redirect('profile')

@login_required
def toggle_bookmark(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, course=course)
    if not created:
        bookmark.delete()
        messages.info(request, 'Bookmark removed.')
    else:
        messages.success(request, 'Course bookmarked.')
    return redirect(request.META.get('HTTP_REFERER', 'course_list'))


# ---------------------- Engagement ----------------------

@login_required
def view_likes(request):
    valid_video_ids = Video.objects.values_list('id', flat=True)
    liked_videos = Like.objects.filter(user=request.user, video_id__in=valid_video_ids)
    return render(request, 'profile_likes.html', {'liked_videos': liked_videos})

@login_required
def view_comments(request):
    comments = Comment.objects.filter(user=request.user)
    return render(request, 'profile_comments.html', {'comments': comments})

@login_required
def view_bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user)
    return render(request, 'profile_bookmarks.html', {'bookmarks': bookmarks})


# ---------------------- Teacher Views ----------------------

@login_required
def teacher_list_view(request):
    teachers = User.objects.filter(profile__role='teacher')
    for teacher in teachers:
        teacher.total_courses = Course.objects.filter(teacher=teacher).count()
        teacher.total_videos = Video.objects.filter(course__teacher=teacher).count()
        teacher.total_likes = Like.objects.filter(video__course__teacher=teacher).count()
    return render(request, 'teachers.html', {'teachers': teachers})

@login_required
def teacher_profile_view(request, teacher_id):
    teacher = get_object_or_404(User, id=teacher_id, profile__role='teacher')
    courses = Course.objects.filter(teacher=teacher)
    videos = Video.objects.filter(course__in=courses)
    
    # Get teacher's stats
    total_views = sum(video.views for video in videos)
    total_likes = Like.objects.filter(video__in=videos).count()
    total_comments = Comment.objects.filter(video__in=videos).count()
    
    context = {
        'teacher': teacher,
        'courses': courses,
        'total_courses': courses.count(),
        'total_videos': videos.count(),
        'total_views': total_views,
        'total_likes': total_likes,
        'total_comments': total_comments,
    }
    return render(request, 'teacher_profile.html', context)


# ---------------------- Static Pages ----------------------

@login_required
def about(request):
    reviews = Review.objects.all()
    return render(request, 'about.html', {'reviews': reviews, 'stars': range(1, 6)})

@login_required
def add_review(request):
    if request.method == 'POST':
        text = request.POST.get('review')
        rating = request.POST.get('rating')
        if text and rating:
            Review.objects.create(user=request.user, text=text, rating=int(rating))
        return redirect('about')

@login_required
def contact_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        number = request.POST['number']
        message = request.POST['message']
        full_message = f"Name: {name}\nEmail: {email}\nPhone: {number}\nMessage: {message}"
        send_mail(
            subject='New Contact Form Submission',
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
        )
        return redirect('contact')

    return render(request, 'contact.html')

@login_required
def playlist_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    videos = course.videos.all()
    return render(request, 'playlist.html', {'course': course, 'videos': videos})

def become_tutor(request):
    if request.method == 'POST':
        try:
            # Personal Information
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            
            # Professional Information
            expertise = request.POST.get('expertise')
            experience = request.POST.get('experience')
            
            # Teaching Profile
            teaching_style = request.POST.get('teaching_style')
            availability = request.POST.get('availability')
            message = request.POST.get('message')
            
            # File Handling
            resume = request.FILES.get('resume')
            certificates = request.FILES.getlist('certificates')
            
            # Validation
            if not all([name, email, phone, expertise, experience, teaching_style, availability, message]):
                messages.error(request, "Please fill in all required fields.")
                return redirect('become_tutor')
            
            if not resume:
                messages.error(request, "Please upload your resume.")
                return redirect('become_tutor')
                
            if len(certificates) > 3:
                messages.error(request, "You can upload maximum 3 certificates.")
                return redirect('become_tutor')
                
            # Check file sizes
            max_size = 5 * 1024 * 1024  # 5MB
            if resume.size > max_size:
                messages.error(request, "Resume file size should be less than 5MB.")
                return redirect('become_tutor')
                
            for cert in certificates:
                if cert.size > max_size:
                    messages.error(request, "Each certificate file size should be less than 5MB.")
                    return redirect('become_tutor')

            # Create directories if they don't exist
            applicant_folder = os.path.join(settings.MEDIA_ROOT, 'tutor_applications', name.strip())
            resume_folder = os.path.join(applicant_folder, 'resume')
            cert_folder = os.path.join(applicant_folder, 'certificates')
            
            os.makedirs(resume_folder, exist_ok=True)
            os.makedirs(cert_folder, exist_ok=True)

            # Save files
            resume_name = f"{name.strip()}_resume{os.path.splitext(resume.name)[1]}"
            resume_path = default_storage.save(f'tutor_applications/{name.strip()}/resume/{resume_name}', resume)
            
            certificate_paths = []
            for i, cert in enumerate(certificates):
                ext = os.path.splitext(cert.name)[1]
                cert_name = f"{name.strip()}_certificate_{i+1}{ext}"
                cert_path = default_storage.save(f'tutor_applications/{name.strip()}/certificates/{cert_name}', cert)
                certificate_paths.append(cert_path)

            # Email to admin
            try:
                admin_subject = f"New Tutor Application from {name}"
                admin_body = f"""
                TUTOR APPLICATION DETAILS
                =======================

                Personal Information:
                -------------------
                Full Name: {name}
                Email Address: {email}
                Phone Number: {phone}

                Professional Information:
                ----------------------
                Areas of Expertise: {expertise}
                Years of Experience: {experience}

                Teaching Profile:
                ---------------
                Teaching Style: {teaching_style}
                Weekly Availability: {availability} hours

                Teaching Philosophy:
                ------------------
                {message}

                Documents Submitted:
                -----------------
                Resume: {resume_path}
                Certificates: {', '.join(certificate_paths) if certificate_paths else 'None submitted'}

                Application Status: Under Review
                """

                send_mail(
                    subject=admin_subject,
                    message=admin_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                print(f"Admin email sent successfully to {settings.CONTACT_EMAIL}")
            except Exception as e:
                print(f"Error sending admin email: {str(e)}")
                messages.warning(request, "Your application was received but there was an issue notifying the admin.")

            # Email to applicant
            try:
                applicant_subject = "Thank you for your tutor application - TeckHub"
                applicant_body = f"""
                Dear {name},

                Thank you for applying to become a tutor at TeckHub. We have received your application and all the submitted documents.

                Application Details:
                ------------------
                Name: {name}
                Email: {email}
                Phone: {phone}
                Expertise Areas: {expertise}
                Experience: {experience}
                Teaching Style: {teaching_style}
                Weekly Availability: {availability} hours

                Our team will carefully review your application and get back to you within 3-5 business days.
                If you have any questions in the meantime, please don't hesitate to contact us.

                Best regards,
                TeckHub Team
                """

                send_mail(
                    subject=applicant_subject,
                    message=applicant_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
                print(f"Applicant email sent successfully to {email}")
                messages.success(request, "Your application has been submitted successfully. Please check your email for confirmation.")
            except Exception as e:
                print(f"Error sending applicant email: {str(e)}")
                messages.warning(request, "Your application was submitted but there was an issue sending the confirmation email.")

            return redirect('become_tutor')

        except Exception as e:
            print(f"Error processing application: {str(e)}")
            messages.error(request, f"There was an error processing your application. Please try again.")
            return redirect('become_tutor')

    return render(request, 'become_tutor.html')



@login_required
def search(request):
    query = request.GET.get('q', '')
    courses = []
    teachers = []
    categories = []
    
    if query:
        # Search in courses with prefetch_related for optimization
        courses = Course.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query) |
            Q(teacher__username__icontains=query) |
            Q(teacher__first_name__icontains=query) |
            Q(teacher__last_name__icontains=query)
        ).prefetch_related('teacher', 'category', 'videos').distinct()

        # Search in teachers with select_related for optimization
        teachers = User.objects.filter(
            Q(profile__role='teacher') &
            (Q(username__icontains=query) |
             Q(first_name__icontains=query) |
             Q(last_name__icontains=query))
        ).select_related('profile').distinct()

        # Search in categories with annotated course count
        categories = Category.objects.filter(
            name__icontains=query
        ).annotate(course_count=Count('course')).distinct()

    context = {
        'query': query,
        'courses': courses,
        'teachers': teachers,
        'categories': categories,
        'total_results': len(courses) + len(teachers) + len(categories)
    }
    
    return render(request, 'search.html', context)

@login_required
def become_teacher(request):
    if request.method == 'POST':
        user = request.user
        profile = user.profile
        
        # Update profile fields
        profile.role = 'teacher'
        profile.bio = request.POST.get('message', '')
        profile.teaching_style = request.POST.get('teaching_style', '')
        profile.availability = request.POST.get('availability', '')
        profile.save()
        
        messages.success(request, "Congratulations! You are now a teacher.")
        return redirect('profile')
        
    return render(request, 'become_tutor.html')

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Check if user is already enrolled
    if course in request.user.profile.enrolled_courses.all():
        messages.info(request, 'You are already enrolled in this course.')
        return redirect('course_detail', course_id=course_id)
    
    # Add course to user's enrolled courses
    request.user.profile.enrolled_courses.add(course)
    messages.success(request, f'Successfully enrolled in {course.title}!')
    
    return redirect('course_detail', course_id=course_id)
