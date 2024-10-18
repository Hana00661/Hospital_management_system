from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from patientapp.models import Patient


class PatientAppModelTest(TestCase):
    def setUp(self):
        self.patient_profile = PatientProfile.objects.create(full_name="Jane Doe")

    def test_patient_profile_str(self):
        self.assertEqual(str(self.patient_profile), "Jane Doe")

class PatientAppViewTest(TestCase):
    def test_patient_dashboard_view(self):
        response = self.client.get(reverse('patient_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'patientapp/dashboard.html')

class PatientAppUrlTest(SimpleTestCase):
    def test_patient_dashboard_url_resolves(self):
        url = reverse('patient_dashboard')
        self.assertEqual(resolve(url).func.__name__, 'patient_dashboard')
