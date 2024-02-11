from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="Sample user", password="samplepassword1234"
        )

    def test_unique_user_username_is_enforced(self):
        """Testing that two users with same username are not allowed."""
        with self.assertRaises(IntegrityError):
            User.objects.create(username="Sample user", password="password1234")

    def test_unique_user_password_is_not_enforced(self):
        User.objects.create(
            username="Any other username", password="samplepassword1234"
        )
