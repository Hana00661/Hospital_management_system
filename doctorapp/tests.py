from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from doctorapp.models import Doctor


class DoctorAppModelTest(TestCase):
    def setUp(self):
        self.doctor = Doctor.objects.create(full_name="Dr. Smith", specialty="Cardiology")

    def test_doctor_str(self):
        self.assertEqual(str(self.doctor), "Dr. Smith")

class DoctorAppViewTest(TestCase):
    def test_doctor_dashboard_view(self):
        response = self.client.get(reverse('doctor_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'doctorapp/dashboard.html')
