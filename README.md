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

Visit <http://127.0.0.1:8000/> to view the website. Media Files The project handles car images. Ensure you have a media/ directory for image uploads. If you encounter issues, adjust the MEDIA_URL and MEDIA_ROOT in your settings.py. Features to Add Search and filter functionality for car listings. User reviews and ratings for sellers. Integration with a payment gateway for online transactions.

make sure before you run the server you should create a

```bash
.env
```

file and put the following variables in it

```bash
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

- Integration with payment gateways for appointment booking fees.
- Appointment cancellation and rescheduling functionalities.
- Messaging system for communication between patients and doctors.
- Integration with medical record systems for patient data management.
- Multi-hospital support with location management.

## Deployment

To deploy this project, you can use platforms like Heroku or AWS. Follow their documentation for deployment instructions.

# Nginx Configuration for Django Application
    To serve the Django application using Nginx and Gunicorn, use the following configuration:

```bash
        server {
        listen 80;
        server_name server_ip_or_domain;  # Replace with your server's IP address or domain name
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
            root /path/to/project;  # Replace with the path to your Django project's static files
        }
        location /staticfiles/ {
            root /path/to/project;  # Same path as above
        }
        location /uploads/ {
            root /path/to/project;  # Same path as above
        }
        # Proxy configuration for Gunicorn
        location / {
            include proxy_params;
            proxy_pass http://unix:/run/gunicorn.sock;  # Adjust the path if your Gunicorn socket is located elsewhere
        }
    }
```
# Gunicorn Systemd Service Configuration
    To set up Gunicorn as a service for the Django application, use the following systemd service configuration:
```bash 
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

## Testing

Run the tests to ensure the project's functionality:

```bash
python manage.py test
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
