from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from mainapp.models import MedicalRecord, Appointment
from patientapp.models import Patient


class MainAppModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.patient = Patient.objects.create(full_name="John Doe")
        self.medical_record = MedicalRecord.objects.create(patient=self.patient)

    def test_medical_record_str(self):
        self.assertEqual(str(self.medical_record), "John Doe")

class MainAppViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.patient = Patient.objects.create(full_name="John Doe", User=self.user)
        self.medical_record = MedicalRecord.objects.create(patient=self.patient)

    def test_medical_record_str(self):
        self.assertEqual(str(self.patient), "John Doe")

    def test_medical_record_list_view(self):
        response = self.client.get(reverse('medical_record_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/medicalrecord_list.html')

class MainAppFormTest(TestCase):
    def test_valid_form(self):
        data = {
            'patient': '1',
            'date': '2024-10-18',
            'time': '14:00',
        }
        form = Appointment(data)
        self.assertTrue(form.is_valid())

class MainAppUrlTest(SimpleTestCase):
    def test_medical_record_list_url_resolves(self):
        url = reverse('medical_record_list')
        self.assertEqual(resolve(url).func.__name__, 'medical_record_list')
