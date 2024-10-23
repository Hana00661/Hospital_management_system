from django.test import TestCase
from django.contrib.auth import get_user_model  # Import custom User model
from django.utils import timezone
from doctorapp.models import Doctor
from patientapp.models import Patient
from .models import Service, Appointment, MedicalRecord, LabTest, Prescription, Billing

class HealthAppTests(TestCase):
    def setUp(self):
        # Get the custom User model
        User = get_user_model()

        # Create a User instance for the doctor
        self.user = User.objects.create_user(email="doctoruser@gmail.com", username="doctoruser", password="password123")

        # Create a Doctor instance with the associated User
        self.doctor = Doctor.objects.create(
            user=self.user,  # Associate the doctor with the created user
            full_name="Dr. John Doe",
            specializations="Cardiology"
        )

        # Create a Patient instance
        self.patient = Patient.objects.create(full_name="Jane Smith", gender="Female", user=self.user)

        # Create a Service instance
        self.service = Service.objects.create(
            name="Cardiology Consultation",
            description="Consultation with a cardiology specialist.",
            cost=150.00
        )
        self.service.available_doctors.add(self.doctor)

        # Create an Appointment instance
        self.appointment = Appointment.objects.create(
            service=self.service,
            doctor=self.doctor,
            patient=self.patient,
            appointment_date=timezone.now(),
            issues="Chest pain",
            symptoms="Shortness of breath",
            appointment_status="Scheduled"
        )

    def test_service_creation(self):
        """Test that a Service instance is created properly."""
        self.assertEqual(self.service.name, "Cardiology Consultation")
        self.assertEqual(self.service.description, "Consultation with a cardiology specialist.")
        self.assertEqual(self.service.cost, 150.00)
        self.assertIn(self.doctor, self.service.available_doctors.all())

    def test_appointment_creation(self):
        """Test that an Appointment instance is created properly."""
        self.assertEqual(self.appointment.service, self.service)
        self.assertEqual(self.appointment.doctor, self.doctor)
        self.assertEqual(self.appointment.patient, self.patient)
        self.assertEqual(self.appointment.issues, "Chest pain")
        self.assertEqual(self.appointment.symptoms, "Shortness of breath")
        self.assertEqual(self.appointment.appointment_status, "Scheduled")

    def test_medical_record_creation(self):
        """Test that a MedicalRecord instance is created properly."""
        medical_record = MedicalRecord.objects.create(
            appointment=self.appointment,
            diagnosis="Angina",
            treatment="Nitroglycerin"
        )
        self.assertEqual(medical_record.appointment, self.appointment)
        self.assertEqual(medical_record.diagnosis, "Angina")
        self.assertEqual(medical_record.treatment, "Nitroglycerin")

    def test_lab_test_creation(self):
        """Test that a LabTest instance is created properly."""
        lab_test = LabTest.objects.create(
            appointment=self.appointment,
            test_name="ECG",
            description="Electrocardiogram",
            result="Normal"
        )
        self.assertEqual(lab_test.appointment, self.appointment)
        self.assertEqual(lab_test.test_name, "ECG")
        self.assertEqual(lab_test.description, "Electrocardiogram")
        self.assertEqual(lab_test.result, "Normal")

    def test_prescription_creation(self):
        """Test that a Prescription instance is created properly."""
        prescription = Prescription.objects.create(
            appointment=self.appointment,
            medications="Aspirin 81 mg"
        )
        self.assertEqual(prescription.appointment, self.appointment)
        self.assertEqual(prescription.medications, "Aspirin 81 mg")

    def test_billing_creation(self):
        """Test that a Billing instance is created properly."""
        billing = Billing.objects.create(
            patient=self.patient,
            appointment=self.appointment,
            sub_total=150.00,
            tax=15.00,
            total=165.00,
            status="Unpaid"
        )
        self.assertEqual(billing.patient, self.patient)
        self.assertEqual(billing.appointment, self.appointment)
        self.assertEqual(billing.sub_total, 150.00)
        self.assertEqual(billing.tax, 15.00)
        self.assertEqual(billing.total, 165.00)
        self.assertEqual(billing.status, "Unpaid")
