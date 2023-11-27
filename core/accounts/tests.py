from django.test import TestCase
from django.contrib.auth import get_user_model

class CustomUserTest(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create(email='test@test.com', password='testpass123')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_super_user(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email='testsuper@testsuper.com', password='supertestpass123')
        self.assertEqual(admin_user.email, 'testsuper@testsuper.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)