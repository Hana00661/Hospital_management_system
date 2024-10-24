# Hospital Management System

The Hospital Management System is designed for developing countries to simplify and enhance healthcare operations for hospitals and clinics.
In developing countries, hospital treatment costs are usually high for patients because the doctor needs many assistants to be able to follow up on all the patients.  

This application helps the doctor manage all patient follow-up processes, starting from confirming payments, through laboratory tests, and ending with treatment. This results in the hospital having to reduce the administrative staff, which leads to lower prices in hospitals, taking into account limited-income, distressed and suffering patients.  

With functionalities such as patient and doctor registration, appointment scheduling, lab test result tracking, and prescription management, it provides a user-friendly platform that simplifies patient access to medical services and improves the efficiency of healthcare professionals' workflows.  

Tailored for healthcare institutions seeking a modern, efficient solution, this system empowers patients while giving doctors powerful tools for managing appointments and patient care with lower costs.

## Target Audience

This system is designed for hospitals and clinics looking for a user-friendly platform to manage appointments, lab results, and prescriptions. It empowers patients with better accessibility and doctors with streamlined appointment management.

## Features

### Common Features

- List all services that the website provides.
- User Profiles: Customize profiles with personal information(for doctors and patients).
- User Authentication: Secure login and registration.
- User-Friendly Interface: Intuitive design for easy navigation.
- Responsive Design: Accessible on various devices.
- User Roles: Distinct interfaces for patients and doctors.
- Secure Data Handling: Protect sensitive medical information.

### For Patients

- Book Appointments: Schedule appointments with available doctors.
- View Lab Tests: Access results of lab tests.
- View Prescriptions: Check prescriptions issued by doctors.
- View Medical Records: Access medical records.
- Get his notifications.

### For Doctors

- View Patients: Access patient information.
- Submit lab tests.
- Submit Prescriptions: Check prescriptions issued to patients.
- Manage Appointments: View and manage upcoming appointments(cansel or reschedule or mark as done).

## Technologies Used

- **Backend**: Python, Django
- **Frontend**: HTML, CSS (Bootstrap)
- **Database**: SQLite (or PostgreSQL for production)
- **Image Handling**: Pillow for image uploads
- **Version Control**: Git & GitHub
- **Authentication**: Django’s built-in authentication system
- **APIs**: RESTful APIs with Django REST Framework (optional)

## Getting Started

Follow the instructions below to get a copy of the project running on your local machine.

### Prerequisites

Make sure you have Python and Django installed on your machine.

- Install Python: Python Download
- pip (package manager usually included with Python)
- Install Django:

```bash
pip install django
```

## Installation

## installation Notes

Python Version: Ensure you are using Python 3.10 or higher.
Django Version: This project is compatible with Django 4.2.2.

### 1. Clone the repository

```bash
git clone https://github.com/your-username/hospital-management-system.git

cd hospital-management-system
```

### 2. Set up a virtual environment (recommended)

```bash
python -m venv env
source env/bin/activate  # For Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

### 5. Create a superuser to access the Django admin

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Visit <http://127.0.0.1:8000/> to view the website.

make sure before you run the server you should create a

```bash
.env
```

file and put the following variables in it

```ini
# where we will putting our secrets keys

STRIPE_PUBLIC_KEY = 'your stripe-public-key'
STRIPE_SECRET_KEY = 'your stripe-secret-key'

PAYPAL_CLIENT_ID = 'your paypal-client-id'
PAYPAL_SECRET_ID = 'your paypal-secret-id'

MAILGUN_API_KEY = 'your-mailgun-api-key'
MAILGUN_SENDER_DOOMAIN = 'your-mailgun-domain'

FROM_EMAIL= 'youremail@gmail.com'
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL='youremail@gmail.com'
SERVER_EMAIL='youremail@gmail.com'
```

### Access the admin interface

Visit <http://127.0.0.1:8000/admin/> in your browser and log in using the superuser credentials.

## Further Development

This project serves as a foundation for building a comprehensive hospital management system. Potential enhancements include:

- Messaging system for communication between patients and doctors.
- Multi-hospital support with location management.
- Adding a new access for the lab technician to receives the test directly from the doctor
- Set the new user verification message.
- Transferring the doctor to a separate page showing the number of patients he has, their medical data, and their health conditions.

## Deployment

To deploy this project, you can use platforms like Heroku or AWS. Follow their documentation for deployment instructions.

## Nginx Configuration for Django Application

To serve the Django application using Nginx and Gunicorn, use the following configuration:

```bash
sudo vim /etc/nginx/sites-available/yourfile.con
```

```nginx

server {
    listen 80;
    server_name your_server_ip_or_domain;  # Replace with your server's IP address or domain name

    # Security headers
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";

    # Favicon settings
    location = /favicon.ico {
        access_log off;
        log_not_found off;
    }

    # Static files configuration
    location /static/ {
        root /path/to/your/project;  # Replace with the path to your Django project's static files
    }

    location /staticfiles/ {
        root /path/to/your/project;  # Same path as above
    }

    location /uploads/ {
        root /path/to/your/project;  # Same path as above
    }

    # Proxy configuration for Gunicorn
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;  # Adjust the path if your Gunicorn socket is located elsewhere
    }
}
```

## Gunicorn Systemd Service Configuration

To set up Gunicorn as a service for the Django application, use the following systemd service configuration:

```bash
sudo vim /etc/systemd/system/gunicorn.service
```

```ini
    [Unit]
    Description=gunicorn daemon
    Requires=gunicorn.socket
    After=network.targe
    [Service]
    User=alx
    Group=www-data
    WorkingDirectory=/home/alx/Hospital_management_system
    ExecStart=/home/alx/Hospital_management_system/env/bin/gunicorn \
              --access-logfile - \
              --workers 3 \
              --bind unix:/run/gunicorn.sock \
              HMS_project.wsgi:applicatio
    [Install]
    WantedBy=multi-user.target
```

## Gunicorn Socket Configuration

To set up a socket for Gunicorn, use the following systemd socket configuration:

```bash
sudo vim /etc/systemd/system/gunicorn.soket
```

```ini
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

## Managing Services

After making changes to the Gunicorn or Nginx configurations, you need to reload the systemd daemon and restart the services to apply the changes. Use the following commands:

## Reload the systemd manager configuration

```bash
sudo systemctl daemon-reload
```

## Restart the Gunicorn service

```bash
sudo systemctl restart gunicorn
```

## Restart the Nginx service

```bash
sudo systemctl restart nginx
```

## Backup Script for Django Application

This script creates a compressed backup of your Django application files, storing it in a specified backup directory. It also maintains only the three most recent backups by deleting older backups.

## Script Overview

The script does the following:

1. Defines the backup and Django project directories.
2. Creates a timestamped backup filename.
3. Creates the backup directory if it doesn't already exist.
4. Compresses the Django project files into a `.tar.gz` file.
5. Deletes older backups, keeping only the three most recent backups.

## Backup Script

```bash
#!/bin/bash

BACKUP_DIR="/path/to/backup/directory"  # Specify the backup directory
DJANGO_PROJECT_DIR="/path/to/django/project"  # Specify your Django project directory
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="django_app_backup_$TIMESTAMP.tar.gz"

mkdir -p "$BACKUP_DIR"  # Create the backup directory if it doesn't exist
tar -czf "$BACKUP_DIR/$BACKUP_NAME" -C "$DJANGO_PROJECT_DIR" .  # Create the backup

cd "$BACKUP_DIR" || exit  # Navigate to the backup directory
ls -tp | grep -v '/$' | tail -n +4 | xargs -I {} rm -- {}  # Keep only the last 3 backups
```

## Testing

Run the tests to ensure the project's functionality:

```bash
python manage.py test
```

Running specific tests:
To run tests within a specific app or module, provide the app name or module path as an argument:

```bash
python manage.py test myapp.tests
```

## Contributing

Contributions are welcome! Please follow these steps:

### 1. Fork the Repository

### 2. Create a Feature Branch (or choose your branch name)

```bash
git checkout -b feature/your-feature-name
```

### 3. Commit Your Changes

```bash
git commit -m "Add your message"
```

### 4. Push to the Branch

```bash
git push origin feature/your-feature-name
```

### 5.  Open a Pull Request

Provide a clear description of your changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any inquiries or support, please contact:

- Ahmed Altaif [ahmedaltaif79@gmail.com](mailto:ahmedaltaif79@gmail.com)
- Hana Abdalhag [eng.hana95@gmail.com](mailto:eng.hana95@gmail.com)
- Omar Algassim [omarggg2@gmail.com](mailto:omarggg2@gmail.com)

Thank you for using the Hospital Management System (VClinic)! We hope it helps streamline healthcare management effectively.
