from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from userauthapp.models import User


class UserAuthAppModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='johndoe', password='password123')

    def test_user_str(self):
        self.assertEqual(str(self.user), "johndoe")

class UserAuthAppViewTest(TestCase):
    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'userauthapp/login.html')

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'userauthapp/register.html')
