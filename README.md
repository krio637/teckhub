# TeckHub - Learning Platform

TeckHub is a modern learning platform built with Django that enables users to access and manage educational content. The platform supports both students and teachers, offering a comprehensive set of features for online learning.

## Features

- **User Authentication**
  - Login/Register functionality
  - Password reset capability
  - Profile management

- **Course Management**
  - Course creation and editing
  - Video upload and management
  - Category organization
  - Course bookmarking

- **Search Functionality**
  - Search across courses, teachers, and categories
  - Advanced filtering options
  - Real-time search suggestions

- **Interactive Learning**
  - Video lessons
  - Course progress tracking
  - Like and comment system
  - Bookmarking system

- **Teacher Features**
  - Course creation dashboard
  - Student progress monitoring
  - Content management tools

- **Responsive Design**
  - Mobile-friendly interface
  - Dark/Light theme support
  - Modern UI/UX

## Technology Stack

- Django 5.2.1
- Python 3.12.6
- Bootstrap 5.3
- SQLite (Database)

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/teckhub.git
cd teckhub
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run migrations
```bash
python manage.py migrate
```

5. Create a superuser
```bash
python manage.py createsuperuser
```

6. Run the development server
```bash
python manage.py runserver
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 