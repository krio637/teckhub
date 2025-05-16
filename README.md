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

4. Set up environment variables
Create a `.env` file in the root directory with the following variables:
```
# Django Settings
DEBUG=True
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# Email Settings (Required for password reset functionality)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password

# Other Settings
TIME_ZONE=UTC
LANGUAGE_CODE=en-us
```

5. Run migrations
```bash
python manage.py migrate
```

6. Create a superuser
```bash
python manage.py createsuperuser
```

7. Run the development server
```bash
python manage.py runserver
```

## Environment Variables

The following environment variables are required to run the application:

| Variable | Description | Example Value |
|----------|-------------|---------------|
| DEBUG | Debug mode flag | True |
| SECRET_KEY | Django secret key | 'your-secret-key-here' |
| ALLOWED_HOSTS | Comma-separated list of allowed hosts | localhost,127.0.0.1 |
| DB_NAME | Database name | teckhub_db |
| DB_USER | Database username | postgres |
| DB_PASSWORD | Database password | your_password |
| DB_HOST | Database host | localhost |
| DB_PORT | Database port | 5432 |
| EMAIL_HOST | SMTP server host | smtp.gmail.com |
| EMAIL_PORT | SMTP server port | 587 |
| EMAIL_USE_TLS | Use TLS for email | True |
| EMAIL_HOST_USER | Email username | your_email@gmail.com |
| EMAIL_HOST_PASSWORD | Email password or app password | your_app_password |
| TIME_ZONE | Application timezone | UTC |
| LANGUAGE_CODE | Application language | en-us |

**Note:** Never commit the `.env` file to version control. The above values are examples only.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 