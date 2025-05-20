# Django Authentication Service

A RESTful authentication service built with Django REST Framework, featuring JWT authentication, Swagger documentation, and PostgreSQL database.

## Features

- User Registration and Login
- JWT Token Authentication
- Profile Management
- API Documentation with Swagger UI
- PostgreSQL Database Integration
- Logging System with Loguru

## Prerequisites

- Python 3.11 or higher
- PostgreSQL
- pip (Python package manager)

## Installation Steps

1. Clone the repository:

```bash
git clone https://github.com/emkr-13/lat_auth_django.git
cd lat_auth_django
```

2. Create and activate virtual environment:

```bash
python -m venv env
source env/bin/activate  # For Linux/Mac
# or
.\env\Scripts\activate  # For Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create PostgreSQL database:

```sql
CREATE DATABASE lat_auth_django;
```

5. Configure environment variables:
   Create a `.env` file in the root directory with the following content:

```env
DEBUG=True
SECRET_KEY=your-secret-key

# Database settings
DB_NAME=lat_auth_django
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Application settings
APP_PORT=3080
```

6. Create static files directory and collect static files:

```bash
mkdir logs
python manage.py collectstatic --noinput
```

7. Run database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Running the Service

1. Start the development server:

```bash
python manage.py runserver_with_env
```

The server will start at http://localhost:3080

## API Endpoints

- Swagger Documentation: http://localhost:3080/swagger/
- ReDoc Documentation: http://localhost:3080/redoc/

### Available Endpoints:

- POST `/api/register/` - Register new user
- POST `/api/login/` - Login and get JWT tokens
- GET/PUT `/api/profile/` - Get/Update user profile
- POST `/api/token/refresh/` - Refresh JWT token

## Authentication

The API uses JWT (JSON Web Token) authentication. To access protected endpoints:

1. Login using `/api/login/` to get the access token
2. Include the token in the Authorization header:

```
Authorization: Bearer <your-access-token>
```

## API Documentation

Detailed API documentation is available through Swagger UI at http://localhost:3080/swagger/

## Logging

Logs are stored in the `logs` directory and are automatically rotated:

- Maximum log file size: 500MB
- Log retention period: 10 days
- Log levels: DEBUG (console) and INFO (file)

## Development

To create a superuser for admin access:

```bash
python manage.py createsuperuser
```

Access the admin interface at: http://localhost:3080/admin/
