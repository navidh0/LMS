from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class AuthTests(TestCase):
    def test_signup_login_logout(self):
        # Signup (custom user)
        resp = self.client.post(reverse('signup'), {
            'username': 'u1',
            'full_name': 'User One',
            'role': 'member',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
        })
        self.assertEqual(resp.status_code, 302)
        User = get_user_model()
        self.assertTrue(User.objects.filter(username='u1').exists())

        # Login
        resp = self.client.post(reverse('login'), {
            'username': 'u1',
            'password': 'StrongPass123'
        })
        self.assertEqual(resp.status_code, 302)

        # Logout (GET allowed)
        resp = self.client.get(reverse('logout'))
        self.assertEqual(resp.status_code, 302)
